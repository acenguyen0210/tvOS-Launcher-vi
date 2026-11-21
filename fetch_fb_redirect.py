import urllib.request
import urllib.error

url = 'https://mbasic.facebook.com/share/p/19tDLZDJQA/'
req = urllib.request.Request(url, headers={
    'User-Agent': 'curl/7.68.0'
})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        print('Final URL:', resp.geturl())
        print(resp.read()[:500])
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code, e.headers)
    if 'Location' in e.headers:
        print('Location:', e.headers['Location'])
except Exception as e:
    print('Error:', e)

