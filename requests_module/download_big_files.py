import requests


# resp = requests.get('https://software.download.prss.microsoft.com/pr/Win10_21H2_EnglishInternational_x64.iso?t=53106736-2faf-4d83-96c8-6687d8ac2ff3&e=1649616220&h=ef61b90fcfb18099fda7b275c520260d26a8a53ad111ca32f22eb1b39071a3ad',
#              stream=True)

url ='https://mirror2.internetdownloadmanager.com/idman640build11.exe?v=lt&filename=idman640build11.exe'

resp = requests.get(url, stream=True)
with open('idm.exe', 'wb') as f:
    for data in resp:
        f.write(data)