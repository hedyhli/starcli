#!/usr/bin/python3

import subprocess
import shutil
import os


def install_commit_hook():
    print("Starting the script...")

    # Get the git repository path
    try:
        print("Fetching the git directory...")
        git_repo_path = subprocess.check_output(
            ["git", "rev-parse", "--git-dir"], text=True).strip()
        print(f"Git directory found: {git_repo_path}")
    except subprocess.CalledProcessError:
        print("Failed to find git directory. Are you in a git repo?")
        return

    commit_msg_file = 'commit-msg'
    git_hooks_dir = os.path.join(git_repo_path, 'hooks')

    print(f"Checking if commit-msg file exists at {commit_msg_file}...")
    if not os.path.exists(commit_msg_file):
        print("Commit-msg file not found. Did you forget to create it?")
        return

    print(f"Copying commit-msg to {git_hooks_dir}...")
    try:
        shutil.copy(commit_msg_file, git_hooks_dir)
        print("Commit-msg hook installed successfully.")
    except Exception as e:
        print(f"Failed to install commit-msg hook: {e}")


if __name__ == "__main__":
    install_commit_hook()
