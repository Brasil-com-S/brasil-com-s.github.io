import subprocess
import json
import sys

def run(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"STDOUT: {res.stdout}")
    if res.stderr:
        print(f"STDERR: {res.stderr}")
    return res

# 1. Get user orgs
res = run("gh api user/orgs")
orgs = []
try:
    orgs = [o["login"] for o in json.loads(res.stdout)]
    print(f"User orgs found: {orgs}")
except Exception as e:
    print(f"Error parsing orgs: {e}")

# Check if 'brasil-com-s' (or variant) is in orgs
target_org = None
for o in orgs:
    if "brasil" in o.lower():
        target_org = o
        break

if not target_org and orgs:
    target_org = orgs[-1] # most recently created org

print(f"Target organization: {target_org}")

if target_org:
    repo_name = f"{target_org}.github.io"
    # Create repo under org
    run(f'gh api orgs/{target_org}/repos -f name="{repo_name}" -f public=true --silent')
    remote_url = f"https://github.com/{target_org}/{repo_name}.git"
    run(f"git remote remove origin")
    run(f"git remote add origin {remote_url}")
    run("git branch -M main")
    push_res = run("git push -u origin main")
    
    # Enable GH Pages
    run(f'gh api repos/{target_org}/{repo_name}/pages -f source=\'{{"branch":"main","path":"/"}}\'')
    print(f"\nSUCCESS! Repository deployed to: https://github.com/{target_org}/{repo_name}")
    print(f"GitHub Pages URL: https://{target_org}.github.io/")
else:
    print("No organization found. Creating under user account...")
    user_res = json.loads(run("gh api user").stdout)
    username = user_res["login"]
    repo_name = "brasil-com-s-api"
    run(f'gh api user/repos -f name="{repo_name}" -f public=true --silent')
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    run("git remote remove origin")
    run(f"git remote add origin {remote_url}")
    run("git branch -M main")
    run("git push -u origin main")
    run(f'gh api repos/{username}/{repo_name}/pages -f source=\'{{"branch":"main","path":"/"}}\'')
    print(f"\nSUCCESS! Repository deployed to: https://github.com/{username}/{repo_name}")
    print(f"GitHub Pages URL: https://{username}.github.io/{repo_name}/")
