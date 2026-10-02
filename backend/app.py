import io
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from auth import auth, valid_email
from database import Generation, User, db
from generator import generate_dataset


def generation_request():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise ValueError("A JSON object is required")
    prompt = body.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt is required")
    rows = body.get("rows", 100)
    if isinstance(rows, str) and rows.isdecimal():
        rows = int(rows)
    if isinstance(rows, bool) or not isinstance(rows, int) or rows < 1:
        raise ValueError("Rows must be a positive integer")
    return prompt.strip(), min(rows, 5000)


def csv_safe(value):
    # Prevent spreadsheet formulas in provider-controlled strings and headers.
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + value
    return value


def create_app(test_config=None):
    # Test configuration never reads a developer's .env or creates the local DB.
    if test_config is None:
        load_dotenv(Path(__file__).with_name(".env"))
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI="sqlite:///dataforge.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CORS_ORIGINS=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"),
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if test_config is not None:
        app.config.update(test_config)
    secret = app.config.get("SECRET_KEY")
    if not isinstance(secret, str) or len(secret.strip()) < 32:
        raise RuntimeError("Set SECRET_KEY to a random value of at least 32 characters")
    app.config["JWT_SECRET_KEY"] = secret
    origins = app.config["CORS_ORIGINS"]
    if isinstance(origins, str):
        origins = [origin.strip() for origin in origins.split(",") if origin.strip()]
    if not origins or "*" in origins:
        raise RuntimeError("CORS_ORIGINS must list explicit allowed origins")
    CORS(app, resources={r"/api/*": {"origins": origins}})
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    @app.route("/api/generate", methods=["POST"])
    @jwt_required()
    def generate():
        try:
            prompt, rows = generation_request()
        except ValueError as error:
            return jsonify(error=str(error)), 400
        try:
            df, columns = generate_dataset(prompt, rows)
            gen = Generation(
                user_id=int(get_jwt_identity()), prompt=prompt, rows=len(df),
                columns=len(columns), filename=f"dataset_{len(df)}rows.csv",
            )
            db.session.add(gen)
            db.session.commit()
            return jsonify(
                columns=list(df.columns), schema=columns,
                data=df.head(20).values.tolist(), rows=len(df), gen_id=gen.id,
            )
        except Exception:
            db.session.rollback()
            # Provider exception messages can contain credentials or request data.
            return jsonify(error="Dataset generation failed. Please try again."), 500

    @app.route("/api/download", methods=["POST"])
    @jwt_required()
    def download():
        try:
            prompt, rows = generation_request()
        except ValueError as error:
            return jsonify(error=str(error)), 400
        try:
            df, _ = generate_dataset(prompt, rows)
            output = io.StringIO()
            safe_df = df.map(csv_safe)
            safe_df.columns = [csv_safe(column) for column in df.columns]
            safe_df.to_csv(output, index=False)
            return send_file(
                io.BytesIO(output.getvalue().encode()), mimetype="text/csv",
                as_attachment=True, download_name=f"dataset_{rows}rows.csv",
            )
        except Exception:
            return jsonify(error="CSV download failed. Please try again."), 500

    @app.route("/api/history", methods=["GET"])
    @jwt_required()
    def history():
        gens = Generation.query.filter_by(user_id=int(get_jwt_identity())).order_by(
            Generation.created_at.desc()
        ).all()
        return jsonify([{
            "id": g.id, "prompt": g.prompt, "rows": g.rows, "columns": g.columns,
            "filename": g.filename, "created_at": g.created_at.strftime("%d %b %Y, %I:%M %p"),
        } for g in gens])

    @app.route("/api/history/<int:gen_id>", methods=["DELETE"])
    @jwt_required()
    def delete_history(gen_id):
        gen = Generation.query.filter_by(id=gen_id, user_id=int(get_jwt_identity())).first()
        if gen is None:
            return jsonify(error="Not found"), 404
        db.session.delete(gen)
        db.session.commit()
        return jsonify(message="Deleted successfully")

    @app.route("/api/settings", methods=["GET", "PUT"])
    @jwt_required()
    def settings():
        user = db.session.get(User, int(get_jwt_identity()))
        if user is None:
            return jsonify(error="User not found"), 404
        if request.method == "GET":
            return jsonify(name=user.name, email=user.email)
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="A JSON object is required"), 400
        name, email = data.get("name", user.name), data.get("email", user.email)
        if not isinstance(name, str) or not name.strip() or len(name.strip()) > 100:
            return jsonify(error="A valid name is required"), 400
        if not valid_email(email):
            return jsonify(error="A valid email is required"), 400
        email = email.strip().lower()
        other = User.query.filter_by(email=email).first()
        if other is not None and other.id != user.id:
            return jsonify(error="Email already exists"), 400
        user.name, user.email = name.strip(), email
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify(error="Email already exists"), 400
        return jsonify(message="Settings updated successfully")

    return app


if __name__ == "__main__":
    create_app().run(port=5000)
