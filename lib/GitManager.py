from git import Repo, GitCommandError, InvalidGitRepositoryError
import os
from typing import Optional


class GitManager:
    def __init__(self, repo_dir: str):
        self.repo_dir = repo_dir
        os.makedirs(self.repo_dir, exist_ok=True)
        self.repo: Optional[Repo] = None
        try:
            if os.path.exists(os.path.join(repo_dir, ".git")):
                self.repo = Repo(self.repo_dir)
        except InvalidGitRepositoryError:
            print("Invalid Git repository. Please check the directory.")

    def clone_repo(self, repo_url: str) -> str:
        if self.repo is None or self.repo.bare:
            try:
                self.repo = Repo.clone_from(repo_url, self.repo_dir)
                return "Repository cloned successfully."
            except GitCommandError as e:
                return f"Failed to clone the repository: {e}"
        return "Repository already exists."

    def pull_updates(self) -> str:
        if self.repo:
            try:
                origin = self.repo.remote()
                origin.pull()
                return "Updates pulled successfully."
            except GitCommandError as e:
                return f"Failed to pull updates: {e}"
        return "Repository not initialised."

    def commit_changes(self, message: str) -> str:
        if self.repo:
            try:
                self.repo.git.add(A=True)
                self.repo.index.commit(message)
                return "Changes committed."
            except GitCommandError as e:
                return f"Failed to commit changes: {e}"
        return "Repository not initialised."

    def push_changes(self) -> str:
        if self.repo:
            try:
                origin = self.repo.remote()
                origin.push()
                return "Changes pushed to active branch in remote repository."
            except GitCommandError as e:
                return f"Failed to push changes: {e}"
        return "Repository not initialised."
