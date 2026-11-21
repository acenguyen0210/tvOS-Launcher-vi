import urllib.request
import re

url = 'https://www.facebook.com/share/p/19tDLZDJQA/'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'vi,en;q=0.9'
})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        final_url = resp.geturl()
        print('Final URL:', final_url)
        content = resp.read().decode('utf-8', errors='ignore')
        with open('fb.html', 'w', encoding='utf-8') as f:
            f.write(content)
        for m in re.finditer(r'<meta\s+(?:property|name)=["\'](.*?)["\']\s+content=["\'](.*?)["\']', content):
            if any(k in m.group(1).lower() for k in ['title', 'description', 'image']):
                print(f"{m.group(1)}: {m.group(2)}")
except Exception as e:
    print('Error:', e)

