#!/usr/bin/python
# cofigs.py contains project configurations.


# github connect
AUTH_TOKEN = '<your_auth_token_goes_here>'  # give necessary permissions to this token.
REPO = '<your_repo>'
REPO_OWNER = '<repo_owner>'
ISSUES_URL = 'https://api.github.com/repos/{repo_owner}/{repo}/issues'.format(repo=REPO, repo_owner=REPO_OWNER)

# email fetch
IMAP_URL = 'imap.gmail.com'
EMAIL_FOLDER = "INBOX"  # specify email folder to read emails.
EMAIL_ACCOUNT = "<secret>"
PASS = '<top_secret>'
DEFAUT_EMAIL_LIMIT = 10

DEFAULT_FETCH_INTERVAL = 5  # in seconds

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'bot.log'