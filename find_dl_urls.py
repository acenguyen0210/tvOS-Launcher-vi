import subprocess, os, re

os.environ['TV_HOST'] = '192.168.123.220'
py = 'tools/venv/Scripts/python.exe'

# Pull DLstore APK to PC or read strings
subprocess.run([py, 'tools/tv.py', '--pull', '/data/app/com.dinhlap.dlstore-iJc5fBtuv3Q3_CqaYOgmkw==/base.apk', 'dlstore.apk'])

import zipfile
with zipfile.ZipFile('dlstore.apk', 'r') as z:
    for name in z.namelist():
        if name.endswith('.dex'):
            data = z.read(name)
            matches = re.findall(rb'https?://[^\s"\'<>\x00-\x1f]+', data)
            for m in set(matches):
                url = m.decode('utf-8', errors='ignore')
                if any(k in url.lower() for k in ['dinhlap', 'store', 'hometv', 'api', 'json', 'firebase', 'tv']):
                    print("Found:", url)

