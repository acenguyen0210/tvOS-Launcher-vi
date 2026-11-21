import urllib.request
import re

url = 'https://www.facebook.com/vietxiaomi93/posts/pfbid03esEeuoufpnrrPfUx7kFHMZFmvcZLjTNDSoqp8C41kfVjLZhtapiHtnKHUYW4AgUl'
req = urllib.request.Request(url, headers={
    'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        with open('fb_post.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Length:", len(html))
        # Look for meta tags
        for m in re.finditer(r'<meta\s+property=["\']og:(title|description|image)["\']\s+content=["\'](.*?)["\']', html):
            print(f"{m.group(1)}: {m.group(2)}")
except Exception as e:
    print('Error:', e)

