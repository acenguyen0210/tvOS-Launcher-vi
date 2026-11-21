import subprocess
import os
import re

os.environ['TV_HOST'] = '192.168.123.220'
py = 'tools/venv/Scripts/python.exe'

subprocess.run([py, 'tools/tv.py', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'])
res = subprocess.run([py, 'tools/tv.py', 'cat', '/data/local/tmp/ui.xml'], capture_output=True, text=True, errors='ignore')

texts = re.findall(r'text=["\'](.*?)["\']', res.stdout)
for t in texts:
    if t.strip():
        print("  -", t.strip())

