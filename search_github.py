import urllib.request
import urllib.parse
import json

queries = ['LaunchpadTV', 'Launchpad TV launcher', 'Launchpad android tv', 'launchpad tv']
for q in queries:
    url = 'https://api.github.com/search/repositories?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"=== Query: '{q}' (Total: {data.get('total_count', 0)}) ===")
            for item in data.get('items', [])[:4]:
                print(f"  Repo: {item['full_name']}")
                print(f"  Desc: {item.get('description')}")
                print(f"  URL:  {item['html_url']}")
    except Exception as e:
        print(f"Error for {q}:", e)
