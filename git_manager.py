import os
import git
from git import Repo, InvalidGitRepositoryError

class GitManager:
    def __init__(self):
        self.found_repos = []

    def scan_for_repos(self, root_path):
        """Scans the root_path for git repositories."""
        self.found_repos = []
        try:
            for root, dirs, files in os.walk(root_path):
                if '.git' in dirs:
                    # Found a git repo
                    repo_path = root
                    try:
                        repo = Repo(repo_path)
                        # Basic info
                        repo_name = os.path.basename(repo_path)
                        # Not all repos have origin, handle gracefully
                        remote_url = ""
                        if repo.remotes and 'origin' in repo.remotes:
                             remote_url = repo.remotes.origin.url
                             # Convert SSH to HTTPS for browser opening if needed, or just let browser handle it/user handle it.
                             # Simple conversion for github: git@github.com:user/repo.git -> https://github.com/user/repo
                             if remote_url.startswith("git@"):
                                 remote_url = remote_url.replace(":", "/").replace("git@", "https://")

                        self.found_repos.append({
                            'path': repo_path,
                            'name': repo_name,
                            'obj': repo,
                            'status': 'Idle',
                            'remote_url': remote_url
                        })
                        # Don't recurse into .git or submodules inside this repo (simplification)
                        # dirs.remove('.git') # os.walk logic, already in ignored list usually or manually handled
                    except InvalidGitRepositoryError:
                        pass
        except Exception as e:
            print(f"Error scanning: {e}")
        return self.found_repos

    def commit_and_push(self, repo_path, message="commit by GitAutoSync"):
        """Commits and pushes changes for the given repo."""
        result = {"success": False, "message": ""}
        try:
            repo = Repo(repo_path)
            if repo.is_dirty(untracked_files=True):
                repo.git.add('.')
                repo.index.commit(message)
                
                # Check for remote
                if repo.remotes:
                    origin = repo.remotes.origin
                    origin.push()
                    result["success"] = True
                    result["message"] = f"Committed and pushed: {message}"
                else:
                    result["success"] = False
                    result["message"] = "No remote 'origin' found."
            else:
                result["success"] = True # Nothing to do is technically a success
                result["message"] = "No changes to commit."
        except Exception as e:
            result["success"] = False
            result["message"] = f"Error: {str(e)}"
        
        return result
