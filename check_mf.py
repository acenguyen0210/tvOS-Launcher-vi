import urllib.request
import re

url = 'https://www.mediafire.com/folder/94179s6pyzpxy/AppLap'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'https?://[^\s"\'<>]+(?:hometv|\.apk)[^\s"\'<>]*', html, re.I)
        print("Matches in AppLap:", set(matches))
except Exception as e:
    print('Error:', e)

