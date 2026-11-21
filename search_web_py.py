import urllib.request
import urllib.parse
import re
import sys

query = 'LaunchpadTV "android tv"'
url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        with open('search_res.html', 'w', encoding='utf-8') as f:
            f.write(html)
        snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html)
        with open('search_snippets.txt', 'w', encoding='utf-8') as f:
            for s in snippets:
                clean = re.sub(r'<[^>]+>', '', s).strip()
                f.write(clean + '\n---\n')
        print(f"Saved {len(snippets)} snippets")
except Exception as e:
    print('Error:', e)
