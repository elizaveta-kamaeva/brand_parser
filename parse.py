import re
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def add_sgwords(eng_list, trans_list):
    global known_words
    sg_pairs = []
    for i in range(len(eng_list)):
        if len(eng_list[i]) > 2 and len(trans_list[i]) > 2:
            pair = eng_list[i], trans_list[i]
            sg_pairs.append(pair)
    return sg_pairs

XML = 'files\\spb.xml'
feed = ET.parse(XML)
root = feed.getroot().findall("shop")[0]
categories = root.findall("categories")[0]

offers = root.findall("offers")[0]
url_name = {}

for child in offers.findall("offer"):
    for param in child:
        if param.tag == 'url':
            url = param.text
        if param.tag == 'name':
            url_name[url] = param.text



file = open('riteilrocket.xml', 'r', encoding='utf-8')
outfile = open('simplewine_parsed.csv', 'w', encoding='utf-8')
outfile.write('brand\talias\n')
offer_reading = False
n = 0
for line in file:
    # finding a url for a product
    if '<offer' in line:
        offer_reading = True
    if '<url>' in line and offer_reading:
        url = re.sub('</?url>', '', line).strip()

        # collecting data
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            code = soup.find("div", class_="code")
            trans_raw = code.text.split(',')[1]
        except:
            print('A error happened for this url:')
            print(url)
            offer_reading = False

    if '<name>' in line and offer_reading:
        pairs = []
        eng_raw = re.sub('</?name>', '', line).strip()

        # exclude translations
        eng_raw = re.sub('year old', '', eng_raw, flags=re.IGNORECASE)
        trans_raw = re.sub('-\w+ летний', '', trans_raw, flags=re.IGNORECASE)

        # find only letters, separated by ['`-]
        eng_list = re.findall('[^\u0000-\u0040\u005B-\u0060\u007B-\u00BF]+'
                    '(?:[\'`-][^\u0000-\u0040\u005B-\u0060\u007B-\u00BF]+)*', eng_raw)
        trans_list = re.findall('[А-Яа-яЁё]+'
                      '(?:[\'`-][А-Яа-яЁё]+)*', trans_raw)

        if len(eng_list) == len(trans_list):
            pairs.extend(add_sgwords(eng_list, trans_list))
        # if there are the same neighbour words
        elif len(set(eng_list)) == len(set(trans_list)):
            j = 0
            while j < len(set(eng_list))-1:
                if eng_list[j] == eng_list[j+1]:
                    del eng_list[j+1]
                    continue
                if trans_list[j] == trans_list[j+1]:
                    del trans_list[j+1]
                    continue
                j += 1
            if len(eng_list) == len(trans_list):
                pairs.extend(add_sgwords(eng_list, trans_list))

        if len(eng_list) > 1:
            long_pair = ' '.join(eng_list), ' '.join(trans_list)
            pairs.append(long_pair)

        for p in pairs:
            outfile.write('{}\t{}\n'.format(p[0], p[1]))
        n += 1

        if n % 100 == 0:
            print('{} transliterations done'.format(n))

    if '</offer' in line:
        offer_reading = False

file.close()
outfile.close()
print('Parsing done. {} lines have been processed.'.format(n))
