import urllib.request
import json

url = 'https://gitlab.com/dlstore/main/apps.json?code=oadcsorefsoheadsomainoadb'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Total apps:", len(data))
        for item in data:
            name = item.get('name', '')
            pkg = item.get('package', '')
            link = item.get('link', '') or item.get('url', '')
            if any(k in str(item).lower() for k in ['home', 'hometv', 'launcher']):
                print("App:", name, "| Pkg:", pkg, "| Link:", link)
except Exception as e:
    print('Error:', e)

