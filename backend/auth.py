import re

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from database import User, db


auth = Blueprint("auth", __name__)


def valid_email(email):
    return isinstance(email, str) and len(email.strip()) <= 120 and bool(
        re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip())
    )


@auth.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="A JSON object is required"), 400
    name, email, password = data.get("name"), data.get("email"), data.get("password")
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 100:
        return jsonify(error="A valid name is required"), 400
    if not valid_email(email):
        return jsonify(error="A valid email is required"), 400
    if not isinstance(password, str) or not password.strip() or len(password) > 1024:
        return jsonify(error="A password is required (maximum 1024 characters)"), 400
    email = email.strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify(error="Email already exists"), 400
    user = User(name=name.strip(), email=email, password=generate_password_hash(password))
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Email already exists"), 400
    return jsonify(message="Account created successfully"), 201


@auth.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="A JSON object is required"), 400
    email, password = data.get("email"), data.get("password")
    if not valid_email(email) or not isinstance(password, str) or len(password) > 1024:
        return jsonify(error="Invalid email or password"), 401
    user = User.query.filter_by(email=email.strip().lower()).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify(error="Invalid email or password"), 401
    return jsonify(token=create_access_token(identity=str(user.id)), name=user.name, email=user.email)
