from flask import Blueprint, request, jsonify
from models.user import users_collection
from utils.password_utils import hash_password, check_password
from utils.jwt_utils import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = hash_password(password)

    users_collection.insert_one({
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully"}), 201


# ---------------- LOGIN API ----------------

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    # 1. Check user exists
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # 2. Check password
    if not check_password(password, user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # 3. Generate JWT
    token = generate_token(str(user["_id"]))

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200
