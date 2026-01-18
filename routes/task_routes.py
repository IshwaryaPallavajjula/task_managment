from flask import Blueprint, request, jsonify
from models.task import tasks_collection
from utils.auth_middleware import auth_required
from bson import ObjectId

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# ---------------- GET ALL TASKS ----------------
@task_bp.route("", methods=["GET"])
@auth_required
def get_tasks():
    user_id = request.user["user_id"]

    tasks = list(tasks_collection.find(
        {"userId": user_id}
    ))

    # Convert ObjectId to string for frontend
    for task in tasks:
        task["_id"] = str(task["_id"])

    return jsonify(tasks), 200


# ---------------- CREATE TASK ----------------
@task_bp.route("", methods=["POST"])
@auth_required
def create_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "title": title,
        "description": description,
        "userId": request.user["user_id"]  # store as string
    }

    tasks_collection.insert_one(task)
    return jsonify({"message": "Task created successfully"}), 201


# ---------------- UPDATE TASK ----------------
@task_bp.route("/<task_id>", methods=["PUT"])
@auth_required
def update_task(task_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    result = tasks_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "userId": request.user["user_id"]
        },
        {
            "$set": {
                "title": data.get("title"),
                "description": data.get("description")
            }
        }
    )

    if result.matched_count == 0:
        return jsonify({"error": "Task not found or unauthorized"}), 404

    return jsonify({"message": "Task updated successfully"}), 200


# ---------------- DELETE TASK ----------------
@task_bp.route("/<task_id>", methods=["DELETE"])
@auth_required
def delete_task(task_id):
    result = tasks_collection.delete_one(
        {
            "_id": ObjectId(task_id),
            "userId": request.user["user_id"]
        }
    )

    if result.deleted_count == 0:
        return jsonify({"error": "Task not found or unauthorized"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200
