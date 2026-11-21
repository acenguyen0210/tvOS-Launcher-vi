with open('hotro.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('apps')
with open('apps_snippet.txt', 'w', encoding='utf-8') as f:
    f.write(text[pos:pos+5000])

print("Wrote snippet")
