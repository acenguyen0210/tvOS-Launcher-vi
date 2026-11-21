import urllib.request
import re

url = 'https://vietmitv.id.vn/hotro/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Page fetched ({len(html)} bytes)")
        with open('hotro.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        matches = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.I | re.S)
        print(f"Found {len(matches)} anchor tags")
        for href, text in matches:
            t = re.sub(r'<[^>]+>', '', text).strip()
            if any(k in href.lower() or k in t.lower() for k in ['vxm', 'store', '.apk']):
                print(f"Link: {href} | Text: {t}")
except Exception as e:
    print('Error:', e)

