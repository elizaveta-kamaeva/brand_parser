import re
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from jellyfish import levenshtein_distance as levenshtein

import translitor


def find_alike(trans_word, rus_list):
    dist_dict = {}
    en_word = translitor.process(trans_word.lower())
    for ru_word in rus_list:
        ru_word = ru_word.lower()
        ldist = levenshtein(en_word, ru_word)
        print(en_word, ':', ru_word, '-', ldist)
        if ldist <= 2:
            return ru_word

        else:
            dist_dict[ldist] = ru_word
        max_prob = max(list(dist_dict.keys()))
        if max_prob <= 4 and len(ru_word) != len(en_word) != 4:
            return ru_word



XML = 'files\\spb.xml'
feed = ET.parse(XML)
root = feed.getroot().findall("shop")[0]

offers = root.findall("offers")[0]
urls = set()
pairs = []
empty = []
n = 0

for child in offers.findall("offer"):
    for param in child:
        if param.tag == 'url':
            urls.add(param.text)
            n += 1
    if n > 100:
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
                          '(?:[\'’`-][A-Za-zÀ-ʯ]+)*', eng_str)
    trans_list = re.findall('[А-Яа-яЁё]+'
                            '(?:[\'’`-][А-Яа-яЁё]+)*', trans_str)

    if eng_list:
        print(url, eng_list, trans_list, sep='\n')
        if len(eng_list) == len(trans_list) == 1:
            pairs.append((eng_list[0], trans_list[0]))
        else:
            for eng_word in eng_list:
                trans_word = find_alike(eng_word, trans_list)
                if trans_word:
                    pairs.append((eng_word, trans_word))
                else:
                    empty.append((eng_word, trans_str))


for pair in pairs:
    print(pair[0], '-', pair[1])
print('='*100)
print('Not found pairs for words')
for emp_pair in empty:
    print(emp_pair[0], '-', emp_pair[1])
print('Parsing done. {} lines have been processed.'.format(n))
