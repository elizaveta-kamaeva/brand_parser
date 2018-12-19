import re
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


XML = 'files\\spb.xml'
feed = ET.parse(XML)
root = feed.getroot().findall("shop")[0]

offers = root.findall("offers")[0]
urls = set()
pairs = []
n = 0

for child in offers.findall("offer"):
    for param in child:
        if param.tag == 'url':
            urls.add(param.text)
            n += 1
    if n > 50:
        break

for url in urls:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find("h1", itemprop="name")
    code = soup.find("div", class_="catalog-element-info__ru-title")
    eng_str = title.text.strip()
    trans_str = code.text.strip()

    # remove size
    eng_str = re.sub('\d+\.\d+ \w\Z', '', eng_str)
    trans_str = re.sub('\d+\.\d+ \w\Z', '', trans_str)

    # find only letters, separated by ['`-]
    eng_list = re.findall('[A-Za-zÀ-ʯ]+'
                          '(?:[\'`-][A-Za-zÀ-ʯ]+)*', eng_str)
    trans_list = re.findall('[А-Яа-яЁё]+'
                            '(?:[\'`-][А-Яа-яЁё]+)*', trans_str)

    if eng_list:
        print(url, eng_list, trans_list, sep='\n')
        if len(eng_list) == len(trans_list) == 1:
            pairs.append((eng_list[0], trans_list[0]))








print('Parsing done. {} lines have been processed.'.format(n))
