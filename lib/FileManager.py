from __future__ import annotations
import os
from lib.GitManager import GitManager


class FileManager:
    def __init__(self, git_manager: GitManager):
        self.git_manager = git_manager

    def create_file(self, file_name: str, content: str = "") -> None:
        file_path = os.path.join(self.git_manager.repo_dir, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        self.git_manager.repo.index.add([file_path])
        self.git_manager.commit_changes(f"Create {file_name}")

    def update_file(self, file_name: str, new_content: str) -> None:
        file_path = os.path.join(self.git_manager.repo_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write(new_content)
            self.git_manager.repo.index.add([file_path])
            self.git_manager.commit_changes(f"Update {file_name}")
        else:
            print(f"Error: File {file_name} does not exist.")

    def delete_file(self, file_name: str) -> None:
        file_path = os.path.join(self.git_manager.repo_dir, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            self.git_manager.repo.index.remove([file_path])
            self.git_manager.commit_changes(f"Delete {file_name}")
        else:
            print(f"Error: File .{file_name} does not exist.")

    def list_tracked_files(self) -> list[str]:
        return self.git_manager.list_tracked_files()

    def get_file_contents(self, file_name: str) -> str:
        file_path = os.path.join(self.git_manager.repo_dir, file_name)
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return f"Error: File {file_name} does not exist."
