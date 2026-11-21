import re

with open('hotro.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for any occurrences of 'vxm' or 'apk' or download links
for match in re.finditer(r'(https?://[^\s"\'<>]+|\b[^\s"\'<>]+\.apk\b)', content, re.I):
    url = match.group(0)
    print(url)

