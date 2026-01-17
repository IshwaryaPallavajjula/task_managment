from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp

app = Flask(__name__)

# 🔥 ENABLE CORS (THIS IS THE FIX)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

@app.route("/")
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
