imported = False
while not imported:
    try:
        from bs4 import BeautifulSoup
        from datetime import datetime
        import json
        from ratelimiter import RateLimiter
        import re
        import requests
        import shutil
        imported = True
    except ImportError as e:
        import pip
        pip.main(['install', 'bs4', 'requests', 'ratelimiter'])

DOMAIN = '\u006d\u0078\u002e\u006d\u0069\u006c\u0065\u0072\u006f\u0074\u0069\u0063\u006f\u0073\u002e\u0063\u006f\u006d'
PATH = '\u002f\u0065\u0073\u0063\u006f\u0072\u0074\u0073\u002f\u006a\u0061\u006c\u0069\u0073\u0063\u006f\u002f\u0067\u0075\u0061\u0064\u0061\u006c\u0061\u006a\u0061\u0072\u0061\u002f'
BASE_URL = 'https://' + DOMAIN
RE_ID = re.compile(r"\s*ID: (\d+)")
RE_AGE = re.compile(r".* (\d\d) añ\w*os .*")


@RateLimiter(max_calls=50, period=10, callback=lambda _: print('WAITING'))
def do_request(*args, **kwargs):
    return requests.get(*args, **kwargs)

r = do_request(BASE_URL + PATH)

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
        r = do_request(url)
        if r.status_code != requests.codes.ok:
            continue
        soup = BeautifulSoup(r.content, "html.parser")
        id_ = RE_ID.match(soup.find_all(text=RE_ID)[0]).group(1)
        age = int(RE_AGE.match(soup.find_all(text=RE_AGE)[0]).group(1)) if soup.find_all(text=RE_AGE) else 'n/a'
        cel = soup.find_all('span', {'class': 'me-phone'})[0].find_next_sibling('span').contents[0]
        pics = soup.find_all('picture')
        img_urls = [p.next_element.attrs['data-srcset'] for p in pics]
        with open(name + '.metadata', 'w') as meta:
            json.dump({'id': id_, 'cel': cel, 'url': url, 'imgs': img_urls, 'age': age, 'time': str(datetime.now())}, meta, indent=4)
        for i, url in enumerate(img_urls):
            r = do_request(url, stream=True)
            path = name + str(i) + '.jpg'
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except IndexError as e:
        print('ERROR ' + link + ' ' + e)
