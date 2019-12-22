from bs4 import BeautifulSoup
import requests
import shutil

DOMAIN = '\u006d\u0078\u002e\u006d\u0069\u006c\u0065\u0072\u006f\u0074\u0069\u0063\u006f\u0073\u002e\u0063\u006f\u006d'
PATH = '\u002f\u0065\u0073\u0063\u006f\u0072\u0074\u0073\u002f\u006a\u0061\u006c\u0069\u0073\u0063\u006f\u002f\u0067\u0075\u0061\u0064\u0061\u006c\u0061\u006a\u0061\u0072\u0061\u002f'
BASE_URL = 'https://' + DOMAIN
r = fakereqread('p1.html')

if r.status_code != requests.codes.ok:
    raise Exception('BAD1')
soup = BeautifulSoup(r.content, "html.parser")
containers = soup.find_all('div',{'class':'info-container'})
links = []
for container in containers:
    link = container.findChildren('a', recursive=False)
    links.append(link[0]['href'])
for link in links:
    try:
        name = link.split('/')[2]
        url = BASE_URL + link
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            continue
        soup = BeautifulSoup(r.content, "html.parser")
        cel = soup.find_all('span', {'class': 'me-phone'})[0].find_next_sibling('span').contents[0]
        imgs = soup.find_all('img')
        img_urls = [i.attrs['data-src'] for i in imgs if 'alt' in i.attrs and cel in i.attrs['alt']]
        for i, url in enumerate(img_urls):
            r = requests.get(url, stream=True)
            path = name + str(i) + '.jpg'
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except IndexError as e:
        print('ERROR ' + link + ' ' + e)
