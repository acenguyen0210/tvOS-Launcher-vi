import xml.etree.ElementTree as ET

tree = ET.parse('ui.xml') if False else None

# Read /data/local/tmp/ui.xml
import subprocess, os
py = 'tools/venv/Scripts/python.exe'
os.environ['TV_HOST'] = '192.168.123.220'
res = subprocess.run([py, 'tools/tv.py', 'cat', '/data/local/tmp/ui.xml'], capture_output=True, text=True, errors='ignore')

root = ET.fromstring(res.stdout)
for node in root.iter('node'):
    text = node.attrib.get('text')
    focused = node.attrib.get('focused')
    selected = node.attrib.get('selected')
    bounds = node.attrib.get('bounds')
    if text:
        print(f"Text: {text} | Focused: {focused} | Selected: {selected} | Bounds: {bounds}")

