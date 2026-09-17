#!/usr/bin/env python3
"""Helper script to create a private GitHub repository and push this course codebase.

Usage:
    python scripts/create_github_repo.py [--name REPO_NAME] [--token GITHUB_PAT]
"""

import argparse
import getpass
import json
import subprocess
import sys
import urllib.error
import urllib.request

DEFAULT_REPO_NAME = "micropython-embedded-course"

def check_git_status():
    """Verify git is installed and repository is initialized."""
    try:
        subprocess.run(["git", "status"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] Git repository is not initialized or git is missing.")
        sys.exit(1)

def get_token(args):
    """Retrieve GitHub Personal Access Token."""
    if args.token:
        return args.token.strip()

    print("\n--- GitHub Authentication ---")
    print("A GitHub Personal Access Token (PAT) with 'repo' scope is required.")
    print("Generate one at: https://github.com/settings/tokens (classic) or Fine-Grained Tokens.")
    token = getpass.getpass("Enter your GitHub Personal Access Token: ").strip()
    if not token:
        print("[!] Token cannot be empty.")
        sys.exit(1)
    return token

def test_token(token):
    """Test token and return authenticated username."""
    req = urllib.request.Request("https://api.github.com/user", headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "MicroPython-Lab-Creator"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"[+] Authenticated successfully as GitHub user: '{data['login']}'")
            return data['login']
    except urllib.error.HTTPError as e:
        print(f"[!] Authentication failed: HTTP {e.code} - {e.reason}")
        sys.exit(1)

def create_private_repo(token, repo_name):
    """Create private repository on user's GitHub account."""
    payload = json.dumps({
        "name": repo_name,
        "description": "Comprehensive MicroPython Embedded Systems Laboratory Course for Raspberry Pi Pico & Pico 2 W",
        "private": True,
        "auto_init": False
    }).encode("utf-8")

    req = urllib.request.Request("https://api.github.com/user/repos", data=payload, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "MicroPython-Lab-Creator"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            clone_url = data.get("clone_url")
            print(f"[+] Private repository '{repo_name}' created successfully on GitHub!")
            print(f"    Repository URL: {data.get('html_url')}")
            return clone_url
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"[*] Repository '{repo_name}' already exists on your GitHub account.")
            return None
        else:
            print(f"[!] Failed to create repository: HTTP {e.code} - {e.reason}")
            sys.exit(1)

def push_to_github(username, token, repo_name, clone_url):
    """Configure git remote and push main branch."""
    auth_remote = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    clean_remote = f"https://github.com/{username}/{repo_name}.git"

    # Ensure on main branch
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    # Add or update remote
    remotes = subprocess.run(["git", "remote"], capture_output=True, text=True).stdout.splitlines()
    if "origin" in remotes:
        subprocess.run(["git", "remote", "remove", "origin"], check=True)

    # Use authenticated remote for initial push
    subprocess.run(["git", "remote", "add", "origin", auth_remote], check=True)

    print(f"[*] Pushing main branch to GitHub ({clean_remote})...")
    try:
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("[+] Repository successfully pushed to GitHub!")
    finally:
        # Reset remote URL to clean URL so token is not stored in plaintext .git/config
        subprocess.run(["git", "remote", "set-url", "origin", clean_remote], check=True)
        print("[+] Stored remote URL sanitized for security.")

def main():
    parser = argparse.ArgumentParser(description="Create a private GitHub repository for this course.")
    parser.add_argument("--name", default=DEFAULT_REPO_NAME, help="Name of repository (default: micropython-embedded-course)")
    parser.add_argument("--token", help="GitHub Personal Access Token")
    args = parser.parse_args()

    check_git_status()
    token = get_token(args)
    username = test_token(token)
    clone_url = create_private_repo(token, args.name)
    push_to_github(username, token, args.name, clone_url)
    print("\n--- All Done! ---")
    print(f"Your private repository is live at: https://github.com/{username}/{args.name}")

if __name__ == "__main__":
    main()
