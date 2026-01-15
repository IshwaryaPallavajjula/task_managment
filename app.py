from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp

app = Flask(__name__)
CORS(app)  # allow frontend access

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

@app.route("/")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run()
@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404

@app.errorhandler(500)
def server_error(e):
    return {"error": "Internal server error"}, 500
