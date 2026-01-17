from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.task_routes import task_bp

app = Flask(__name__)

# ✅ SINGLE, CORRECT CORS CONFIG
CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:5173"}},
    allow_headers=["Authorization", "Content-Type"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

@app.route("/")
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)