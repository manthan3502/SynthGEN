from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from database import db, User, Generation
from auth import auth
from generator import generate_dataset
import os
import io

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///dataforge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']                 = os.getenv('SECRET_KEY', 'dataforge_secret')

db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

# ── GENERATE DATASET ──────────────────────────────────
@app.route('/api/generate', methods=['POST'])
@jwt_required()
def generate():
    try:
        user_id = int(get_jwt_identity())
        body    = request.json
        prompt  = body.get('prompt', '')
        rows    = min(int(body.get('rows', 100)), 5000)

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        df, columns = generate_dataset(prompt, rows)

        gen = Generation(
            user_id  = user_id,
            prompt   = prompt,
            rows     = len(df),
            columns  = len(columns),
            filename = f'dataset_{len(df)}rows.csv'
        )
        db.session.add(gen)
        db.session.commit()

        return jsonify({
            'columns': list(df.columns),
            'schema':  columns,
            'data':    df.head(20).values.tolist(),
            'rows':    len(df),
            'gen_id':  gen.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── DOWNLOAD CSV ──────────────────────────────────────
@app.route('/api/download', methods=['POST'])
@jwt_required()
def download():
    try:
        body   = request.json
        prompt = body.get('prompt', '')
        rows   = min(int(body.get('rows', 100)), 5000)

        df, _ = generate_dataset(prompt, rows)

        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'dataset_{rows}rows.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── GET HISTORY ───────────────────────────────────────
@app.route('/api/history', methods=['GET'])
@jwt_required()
def history():
    user_id = int(get_jwt_identity())
    gens    = Generation.query.filter_by(user_id=user_id) \
                              .order_by(Generation.created_at.desc()) \
                              .all()
    return jsonify([{
        'id':         g.id,
        'prompt':     g.prompt,
        'rows':       g.rows,
        'columns':    g.columns,
        'filename':   g.filename,
        'created_at': g.created_at.strftime('%d %b %Y, %I:%M %p')
    } for g in gens])

# ── DELETE HISTORY ITEM ───────────────────────────────
@app.route('/api/history/<int:gen_id>', methods=['DELETE'])
@jwt_required()
def delete_history(gen_id):
    user_id = int(get_jwt_identity())
    gen     = Generation.query.filter_by(id=gen_id, user_id=user_id).first()
    if not gen:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(gen)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'})

# ── GET SETTINGS ──────────────────────────────────────
@app.route('/api/settings', methods=['GET'])
@jwt_required()
def get_settings():
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)
    return jsonify({'name': user.name, 'email': user.email})

# ── UPDATE SETTINGS ───────────────────────────────────
@app.route('/api/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)
    data    = request.json
    if data.get('name'):  user.name  = data['name']
    if data.get('email'): user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Settings updated successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
