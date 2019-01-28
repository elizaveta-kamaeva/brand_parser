import re
import xml.etree.ElementTree as ET


XML = "C:\cygwin64\home\deer\yandex_market"
feed = ET.parse(XML)
root = feed.getroot().findall("shop")[0]

offers = root.findall("offers")[0]
titles = set()
pairs = []
n = 0
num_wrong = 0

for child in offers.findall("offer"):
    for param in child:
        if param.tag == 'name':
            titles.add(param.text)
            n += 1
    if n % 1000 == 0:
        print(n, 'names done.')

outfile = open('files\\wineshopper_parsed.csv', 'w', encoding='utf-8')

for name in titles:
    try:
        eng_str, trans_str = name.strip().split('(')
    except ValueError:
        continue

    # remove size
    eng_str = re.sub('\d+[.,]\d+\s?\w \Z', '', eng_str)
    trans_str = re.sub('\d+[.,]\d+\s?\w\)\Z', '', trans_str)

    # find only letters, separated by ['`-]
    eng_list = re.findall('[A-Za-zÀ-ʯ]+'
                          '(?:[\'’`-][A-Za-zÀ-ʯ]+)*', eng_str)
    trans_list = re.findall('[А-Яа-яЁё]+'
                            '(?:[\'’`-][А-Яа-яЁё]+)*', trans_str)

    if eng_list:
        if len(eng_list) != len(trans_list):
            num_wrong += 1
        outfile.write('{};{}\n'.format(' '.join(eng_list), ' '.join(trans_list)))
outfile.close()

print('Parsing done. {} lines have been processed.'.format(n))
print('Number of unequal lines:', num_wrong)
