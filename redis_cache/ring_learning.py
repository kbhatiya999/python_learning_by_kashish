# from random import random
#
import redis
import ring
import requests
import random

client = redis.StrictRedis(host='localhost', port=8000, db=0)

class XYZ:
    def __init__(self, url):
        self.url = url
    def __eq__(self, other):
        self is other
    def __ring_key__(self):
        return 1




# save in a new lru storage
@ring.redis(client)
# @ring.lru()
def get_url(url):
    return requests.get(url.url).content

x = XYZ('http://example.com')
y = XYZ('http://example.com')
z = XYZ('http://example.com')

data_or_none = get_url.get(x)
print(data_or_none)

data = get_url(y)
print(data)

data_or_none = get_url.get(z)
print(data_or_none)