import urllib.request

url = 'https://sites.google.com/view/dinhlaptv'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        import re
        links = set(re.findall(r'https?://[^\s"\'<>]+', html))
        for l in links:
            if any(k in l.lower() for k in ['hometv', '.apk', 'drive', 'mediafire']):
                print("Site Link:", l)
except Exception as e:
    print('Error:', e)

