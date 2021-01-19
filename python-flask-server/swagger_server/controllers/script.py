import requests
r = requests.get('http://localhost:3330/ds')
print(r.content.decode('utf-8'))