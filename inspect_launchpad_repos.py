import urllib.request
import json

repos = ['nguyenphuong10102003/LaunchpadTV-Nuvio', 'launchpad2/tv', 'thebpandey/tv-simple-home']

for repo in repos:
    print(f"\n=================== {repo} ===================")
    # Check repo info
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Description:", data.get('description'))
            print("Default branch:", data.get('default_branch'))
    except Exception as e:
        print("Error getting repo:", e)
    
    # Check releases
    url_rel = f"https://api.github.com/repos/{repo}/releases"
    req_rel = urllib.request.Request(url_rel, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req_rel) as resp:
            releases = json.loads(resp.read().decode('utf-8'))
            print(f"Releases ({len(releases)}):")
            for r in releases[:3]:
                print(f"  Tag: {r.get('tag_name')} | Name: {r.get('name')}")
                for a in r.get('assets', []):
                    print(f"    Asset: {a.get('name')} | Download: {a.get('browser_download_url')}")
    except Exception as e:
        print("Error getting releases:", e)
