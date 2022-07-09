import requests

sess = requests.Session()

resp = sess.get('https://www.dicthai.com/')

print(resp.text)