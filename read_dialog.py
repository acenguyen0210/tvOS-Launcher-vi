import subprocess, os, re
os.environ['TV_HOST'] = '192.168.123.220'
py = 'tools/venv/Scripts/python.exe'
subprocess.run([py, 'tools/tv.py', 'uiautomator', 'dump', '/data/local/tmp/ui_dialog.xml'])
res = subprocess.run([py, 'tools/tv.py', 'cat', '/data/local/tmp/ui_dialog.xml'], capture_output=True, text=True, errors='ignore')
import xml.etree.ElementTree as ET
try:
    root = ET.fromstring(res.stdout)
    for node in root.iter('node'):
        text = node.attrib.get('text')
        bounds = node.attrib.get('bounds')
        if text:
            print(f"Text: {text} | Bounds: {bounds}")
except Exception as e:
    print("Error:", e)
