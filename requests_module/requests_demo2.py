import requests
from bs4 import BeautifulSoup as bs
sess = requests.Session()

resp = sess.get('https://1800accountant.com/careers')

soup = bs(resp.text, 'lxml')

apply_a = soup.find_all('a',{'class':'apply-btn'})

links = [a['href'] for a in apply_a]

soup2.h1.text
print(soup.prettify())