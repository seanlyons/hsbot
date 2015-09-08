from bs4 import BeautifulSoup
import requests

upper = 11
lower = 0

ob = 'http://www.'
fu = 'hea'
sc = 'rthp'
at = 'wn'
ed = '.com/cards'

for i in range(upper):
    link = ob + fu + sc + at + ed + '?display=3&page=' + str(i)
    print link
    page = requests.get(link)
    html =  page.text

    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all(class_="card-image-item")

    for card in links:
        a = card.contents[1]
        href = a.attrs[u'href']
        img = a.contents[1]
        src = img.attrs[u'src']
        print href+' => '+src
        print "--"
