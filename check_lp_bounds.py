import xml.etree.ElementTree as ET

tree = ET.parse('ui_lp.xml') if False else None
import subprocess, os
py = 'tools/venv/Scripts/python.exe'
os.environ['TV_HOST'] = '192.168.123.220'
res = subprocess.run([py, 'tools/tv.py', 'cat', '/data/local/tmp/ui_lp.xml'], capture_output=True, text=True, errors='ignore')

root = ET.fromstring(res.stdout)
for node in root.iter('node'):
    text = node.attrib.get('text')
    bounds = node.attrib.get('bounds')
    focused = node.attrib.get('focused')
    clickable = node.attrib.get('clickable')
    if text:
        print(f"Text: {text} | Focused: {focused} | Clickable: {clickable} | Bounds: {bounds}")
