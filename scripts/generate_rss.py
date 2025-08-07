# scripts/generate_rss.py

import os
import requests
from feedgenerator import Rss201rev2Feed

OWNER = os.getenv("REPO_OWNER")
REPO = os.getenv("REPO_NAME")
BRANCH = os.getenv("REPO_BRANCH", "main")

rss = Rss201rev2Feed(
    title=f"{REPO} commit diffs",
    link=f"https://github.com/{OWNER}/{REPO}",
    description="RSS feed of latest commit diffs",
    language="en"
)

commits = requests.get(
    f"https://api.github.com/repos/{OWNER}/{REPO}/commits?sha={BRANCH}"
).json()

for commit in commits[:10]:  # Limit to 10 latest commits
    sha = commit["sha"]
    message = commit["commit"]["message"].split("\n")[0]
    url = commit["html_url"]
    diff = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{sha}",
        headers={"Accept": "application/vnd.github.v3.diff"}
    ).text

    short_diff = "\n".join(diff.splitlines()[:20])  # First 20 lines only

    rss.add_item(
        title=message,
        link=url,
        description=f"<pre>{short_diff}</pre>",
        unique_id=sha
    )

os.makedirs("public", exist_ok=True)
with open("public/feed.xml", "w", encoding="utf-8") as f:
    rss.write(f, "utf-8")
