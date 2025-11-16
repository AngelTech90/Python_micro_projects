GitHub Repository Cloner
A Python web scraper that automatically clones all repositories from a GitHub user account.
📋 Description
This script scrapes a GitHub user's profile page, extracts all repository links, and clones them to your local machine. Perfect for backing up your repositories or setting up a new development environment!
🚀 Features

✅ Automatically discovers all public repositories
✅ Handles pagination (works with any number of repos)
✅ Uses SSH clone URLs for secure authentication
✅ Skips repositories that already exist locally
✅ Colored terminal output for easy reading
✅ Confirmation prompt before cloning
✅ Detailed summary statistics
✅ Robust error handling

📦 Prerequisites
Required Software

Python 3.6 or higher
Git
SSH keys configured with GitHub (recommended)

Python Dependencies
bashpip install requests beautifulsoup4
Or install from requirements file:
bashpip install -r requirements.txt
requirements.txt:
requests>=2.31.0
beautifulsoup4>=4.12.0
🔧 Installation

Clone or download this script:

bashwget https://raw.githubusercontent.com/your-repo/github_repo_cloner.py

Install dependencies:

bashpip install requests beautifulsoup4

Make executable (optional):

bashchmod +x github_repo_cloner.py
💻 Usage
Basic Usage
Run the script from the directory where you want to clone all repositories:
bashpython3 github_repo_cloner.py
The script will:

Fetch all repositories from the GitHub user
Display the list of found repositories
Ask for confirmation
Clone all repositories to the current directory

Example Output
============================================================
GitHub Repository Cloner
============================================================
📁 Clone directory: /home/user/projects

🔍 Fetching repositories for user: AngelTech90
  ✓ Found: awesome-project
  ✓ Found: python-scripts
  ✓ Found: web-scraper
  
📊 Found 3 repositories

Do you want to proceed with cloning? (y/n): y

🚀 Starting cloning process...

  → Cloning awesome-project...
  ✓ Successfully cloned awesome-project
  → Cloning python-scripts...
  ✓ Successfully cloned python-scripts
  → Cloning web-scraper...
  ⚠ web-scraper already exists, skipping...

============================================================
📈 Summary
============================================================
Total repositories: 3
Successfully cloned: 2
Skipped (already exist): 1
Failed: 0
============================================================
🔐 Authentication
SSH (Recommended)
The script uses SSH URLs by default (git@github.com:username/repo.git). Make sure you have:

SSH keys generated
Public key added to your GitHub account
SSH agent running

See GitHub's SSH documentation for setup instructions.
HTTPS Alternative
If you prefer HTTPS, modify line 71 in the script:
python# Change from:
ssh_url = f"git@github.com:{username}/{repo_name}.git"

# To:
ssh_url = f"https://github.com/{username}/{repo_name}.git"
⚙️ Configuration
Change Target User
Edit line 104 in the script:
pythonusername = "AngelTech90"  # Change to any GitHub username
Change Clone Directory
By default, repositories are cloned to the current working directory. To specify a different location:
python# Add at line 106:
base_dir = "/path/to/your/directory"
📁 Directory Structure After Running
parent_directory/
├── github_repo_cloner.py
├── repo1/
├── repo2/
├── repo3/
└── ...
🛠️ Troubleshooting
"Git is not installed or not in PATH"
Install Git:

Ubuntu/Debian: sudo apt-get install git
macOS: brew install git
Windows: Download from git-scm.com

"Permission denied (publickey)"
Your SSH keys are not configured. Either:

Set up SSH keys (recommended)
Switch to HTTPS URLs (see Authentication section)

"Repository already exists"
The script automatically skips existing directories. Delete the directory if you want to re-clone.
Rate Limiting
GitHub may rate-limit requests if you run the script too frequently. Wait a few minutes and try again.
🔒 Privacy & Security

The script only accesses public repositories
No authentication credentials are stored
SSH keys remain on your local machine
The script does not modify any GitHub data

🤝 Contributing
Feel free to fork and modify this script! Common enhancements:

Add support for private repositories (requires authentication token)
Filter repositories by name, language, or date
Add parallel cloning for faster execution
Export repository list to JSON/CSV

📝 License
This script is provided as-is for public use. Modify freely for your needs!
🐛 Known Limitations

Only works with public repositories (unless modified to use API tokens)
Requires active internet connection
GitHub's HTML structure changes may break the scraper
Does not clone repository wikis or GitHub Pages

📚 Additional Resources

GitHub API Documentation
BeautifulSoup Documentation
Git Clone Documentation


Made with ❤️ for easier repository management
