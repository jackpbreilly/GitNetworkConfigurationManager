from flask import Flask, request, jsonify
from flask_cors import CORS

from lib.FileManager import FileManager
from lib.GitManager import GitManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

repo_dir = "/home/jreilly/jack/repo"
git_manager = GitManager(repo_dir=repo_dir)
file_manager = FileManager(git_manager=git_manager)


@app.route("/files", methods=["GET"])
def list_files():
    try:
        files = file_manager.list_tracked_files()
        return jsonify(files), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files/<path:file_name>", methods=["GET"])
def get_file(file_name):
    try:
        content = file_manager.get_file_contents(file_name)
        return jsonify({"content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files", methods=["POST"])
def create_file():
    data = request.get_json()
    file_name = data.get("file_name")
    content = data.get("content", "")
    try:
        file_manager.create_file(file_name, content)
        return jsonify({"message": f"File {file_name} created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files/<path:file_name>", methods=["PUT"])
def update_file(file_name):
    data = request.get_json()
    new_content = data.get("content")
    try:
        file_manager.update_file(file_name, new_content)
        return jsonify({"message": f"File {file_name} updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files/<path:file_name>", methods=["DELETE"])
def delete_file(file_name):
    try:
        file_manager.delete_file(file_name)
        return jsonify({"message": f"File {file_name} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/git/clone", methods=["POST"])
def clone_repo():
    data = request.get_json()
    repo_url = data.get("repo_url")
    try:
        message = git_manager.clone_repo(repo_url)
        return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/git/pull", methods=["POST"])
def pull_updates():
    try:
        message = git_manager.pull_updates()
        return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/git/commit", methods=["POST"])
def commit_changes():
    data = request.get_json()
    message = data.get("message")
    try:
        result = git_manager.commit_changes(message)
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/git/push", methods=["POST"])
def push_changes():
    try:
        message = git_manager.push_changes()
        return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
