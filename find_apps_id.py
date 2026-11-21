with open('hotro.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="apps"')
if pos != -1:
    with open('apps_section.txt', 'w', encoding='utf-8') as f:
        f.write(text[pos:pos+5000])
    print("Found id='apps' at", pos)
else:
    print("id='apps' not found")

