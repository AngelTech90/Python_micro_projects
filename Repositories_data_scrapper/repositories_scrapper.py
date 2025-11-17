#!/usr/bin/env python3
"""
GitHub Repository Cloner
Scrapes a GitHub user's repositories and clones them all locally.
"""

import requests
from bs4 import BeautifulSoup
import subprocess
import os
import sys
from pathlib import Path

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def print_colored(message, color):
    """Print colored message to console."""
    print(f"{color}{message}{NC}")


def get_repository_links(username):
    """
    Scrape GitHub user's repository page and extract all repository URLs.
    
    Args:
        username: GitHub username
        
    Returns:
        List of repository clone URLs
    """
    print_colored(f"\n🔍 Fetching repositories for user: {username}", BLUE)
    
    repos = []
    page = 1
    
    while True:
        url = f"https://github.com/{username}?page={page}&tab=repositories"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print_colored(f"❌ Error fetching page {page}: {e}", RED)
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all repository links
        repo_links = soup.find_all('a', {'itemprop': 'name codeRepository'})
        
        if not repo_links:
            # No more repositories found
            break
        
        for link in repo_links:
            repo_name = link.text.strip()
            # Use HTTPS clone URL
            https_url = f"https://github.com/{username}/{repo_name}.git"
            repos.append(https_url)
            print_colored(f"  ✓ Found: {https_url}", GREEN)
        
        page += 1
    
    return repos


def clone_repository(repo_url):
    """
    Clone a single repository.
    
    Args:
        repo_url: Git clone URL
        
    Returns:
        True if successful, False otherwise
    """
    # Extract repo name from URL
    repo_name = repo_url.rstrip('.git').split('/')[-1]
    
    # Check if directory already exists
    if os.path.exists(repo_name):
        print_colored(f"  ⚠ {repo_name} already exists, skipping...", YELLOW)
        return False
    
    print_colored(f"  → Cloning {repo_url}...", BLUE)
    
    try:
        subprocess.run(
            ['git', 'clone', repo_url],
            check=True
        )
        print_colored(f"  ✓ Successfully cloned {repo_name}", GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"  ✗ Failed to clone {repo_name}", RED)
        return False
    except FileNotFoundError:
        print_colored("  ✗ Git is not installed or not in PATH", RED)
        sys.exit(1)


def main():
    """Main function to orchestrate the cloning process."""
    username = "AngelTech90"
    
    # Get current directory
    base_dir = os.getcwd()
    
    print_colored("=" * 60, BLUE)
    print_colored("GitHub Repository Cloner", BLUE)
    print_colored("=" * 60, BLUE)
    print_colored(f"📁 Clone directory: {base_dir}\n", YELLOW)
    
    # Get all repository links
    repos = get_repository_links(username)
    
    if not repos:
        print_colored("\n❌ No repositories found!", RED)
        sys.exit(1)
    
    print_colored(f"\n📊 Found {len(repos)} repositories\n", GREEN)
    
    # Ask for confirmation
    response = input("Do you want to proceed with cloning? (y/n): ")
    if response.lower() != 'y':
        print_colored("❌ Aborted by user", YELLOW)
        sys.exit(0)
    
    # Clone all repositories
    print_colored("\n🚀 Starting cloning process...\n", BLUE)
    
    successful = 0
    failed = 0
    skipped = 0
    
    for repo_url in repos:
        result = clone_repository(repo_url)
        # Extract repo name for checking
        repo_name = repo_url.rstrip('.git').split('/')[-1]
        
        if result is True:
            successful += 1
        elif result is False and os.path.exists(repo_name):
            skipped += 1
        else:
            failed += 1
    
    # Print summary
    print_colored("\n" + "=" * 60, BLUE)
    print_colored("📈 Summary", BLUE)
    print_colored("=" * 60, BLUE)
    print_colored(f"Total repositories: {len(repos)}", BLUE)
    print_colored(f"Successfully cloned: {successful}", GREEN)
    print_colored(f"Skipped (already exist): {skipped}", YELLOW)
    print_colored(f"Failed: {failed}", RED)
    print_colored("=" * 60 + "\n", BLUE)


if __name__ == "__main__":
    main()
