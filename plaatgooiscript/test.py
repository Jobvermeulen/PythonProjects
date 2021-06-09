import requests

url = 'https://haarstudiotamara.nl/contact.php'
myobj = {'name': 'test', 'email':'a@a.nl', 'comments':'abcdefghijklmnopqrstuvwxy'}

for x in range(5000):
    x = requests.post(url, data = myobj)
    print(x.text)