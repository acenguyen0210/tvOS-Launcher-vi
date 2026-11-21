with open('fb_post.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Look for text inside post
paragraphs = re.findall(r'<div[^>]*dir=["\']auto["\'][^>]*>(.*?)</div>', html)
for p in paragraphs[:10]:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if clean:
        print("P:", clean)

