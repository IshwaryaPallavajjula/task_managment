from flask import request, jsonify
from utils.jwt_utils import verify_token

def auth_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid authorization format"}), 401

        decoded = verify_token(token)
        if not decoded:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user = decoded
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
