import subprocess, os, re
py = 'tools/venv/Scripts/python.exe'
os.environ['TV_HOST'] = '192.168.123.220'
subprocess.run([py, 'tools/tv.py', 'uiautomator', 'dump', '/data/local/tmp/ui_v22.xml'])
res = subprocess.run([py, 'tools/tv.py', 'cat', '/data/local/tmp/ui_v22.xml'], capture_output=True, text=True, errors='ignore')
texts = re.findall(r'text=["\'](.*?)["\']', res.stdout)
for t in set(texts):
    if t.strip():
        print(' -', t.strip())

