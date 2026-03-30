from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from database import db, User

auth = Blueprint('auth', __name__)

# ── REGISTER ──────────────────────────────────────────
@auth.route('/api/register', methods=['POST'])
def register():
    data     = request.json
    name     = data.get('name')
    email    = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed = generate_password_hash(password)
    user   = User(name=name, email=email, password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'}), 201

# ── LOGIN ─────────────────────────────────────────────
@auth.route('/api/login', methods=['POST'])
def login():
    data     = request.json
    email    = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        'token': token,
        'name':  user.name,
        'email': user.email
    }), 200
