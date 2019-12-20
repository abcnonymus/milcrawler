import requests
from bs4 import BeautifulSoup

DOMAIN = '\u006d\u0078\u002e\u006d\u0069\u006c\u0065\u0072\u006f\u0074\u0069\u0063\u006f\u0073\u002e\u0063\u006f\u006d'
PATH = '\u002f\u0065\u0073\u0063\u006f\u0072\u0074\u0073\u002f\u006a\u0061\u006c\u0069\u0073\u0063\u006f\u002f\u0067\u0075\u0061\u0064\u0061\u006c\u0061\u006a\u0061\u0072\u0061\u002f'
BASE_URL = 'https://' + DOMAIN
result = requests.get(BASE_URL + PATH)

# if successful parse the download into a BeautifulSoup object, which allows easy manipulation 
if result.status_code == 200:
    soup = BeautifulSoup(result.content, "html.parser")
containers = soup.find_all('div',{'class':'info-container'})
links = []
for container in containers:
    link = container.findChildren('a', recursive=False)
    links.append(link[0]['href'])
for link in links:
    url = BASE_URL + link
    print(url)
    result = requests.get(url)
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        imgs = soup.find_all('img')
        print(imgs)
        cel = soup.find_all('span', {'class': 'me-phone'})[0].find_next_sibling('span').contents[0]
        print(cel)
