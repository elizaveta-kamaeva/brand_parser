import requests
from bs4 import BeautifulSoup
import time

resp = requests.get('https://simplewine.ru/catalog/product/casa_defra_prosecco_spumante_brut_075_6/')
soup = BeautifulSoup(resp.text, 'html.parser')
title = soup.find("h1", class_= "title")
code = soup.find("div", class_= "code")

print(title.text.strip() + '\n' + code.text.strip().split(',')[1])

for url in urls:
    print('https://simplewine.ru' + url['href'])

recipes_urls = []
for n in range(1, 19):
    print(n)
    resp = requests.get('https://www.utkonos.ru/recipes/category?page={}'.format(n))
    soup = BeautifulSoup(resp.text, 'html.parser')
    rec = soup("a", class_="title")
    for d in rec:
        recipes_urls.append('https://www.utkonos.ru' + d['href'])
    time.sleep(2)

# https://www.utkonos.ru/recipes/category?page=2

#сслыки на разделы с рецептами
import requests
from bs4 import BeautifulSoup
import time

resp = requests.get('https://www.gastronom.ru/recipe/')
soup = BeautifulSoup(resp.text, 'html.parser')

cat_urls = []
recs = soup.select("div.popular > a[href^='/recipe']")

for d in recs:
    cat_urls.append('https://www.gastronom.ru'+d['href'])
print(cat_urls)

def lastpage(url):
    url = url + '?&page=999'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.select("div.pagination > a:nth-of-type(7)"):
        return soup.select("div.pagination > a:nth-of-type(7)")[0].text
    else:
        return '1'

for cat in cat_urls:
    print(cat.split('/')[6] + ' ' + lastpage(cat) + ' страниц')

# забыл про переход по страницам
import re


def lastpage(url):
    url = url + '?&page=999'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.select("div.pagination > a:nth-of-type(7)"):
        return soup.select("div.pagination > a:nth-of-type(7)")[0].text
    else:
        return '1'


with open('recipes_gastronom.csv', 'w') as f:
    f.write('name|ingredients|text\n')

k = 1  # категория
url = ''
rec_urls = []
count = 0
for cat_url in cat_urls:
    for x in range(1, int(lastpage(cat_url))):
        resp = requests.get(cat_url + '?&page={}'.format(x))  # x - номер страницы в категории
        soup = BeautifulSoup(resp.text, 'html.parser')
        rec = soup.select("div.row.feed h3 > a")
        n = 1  # номер рецепта на странице

        for el in rec:
            rec_text = ''
            url = 'https://www.gastronom.ru' + el['href']
            rec_urls.append(url)
            if rec_urls.count(url) > 1:
                print(url, rec_urls.count(url))
                continue
            resp = requests.get(url)
            print(k, x, n, url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.find("h1").text
            steps = soup.select("div.step.instruction p")
            for step in steps:
                rec_text += step.text.replace('\r\n', '').replace('\xa0', ' ')
            rec_text = re.sub(r"\s+", u" ", rec_text).strip()
            ingredients_collection = soup.select("li.ingredient")
            ingredients = [i.text.replace('\xa0', ' ') for i in ingredients_collection]
            with open('recipes_gastronom.csv', 'a') as f:
                f.write('{}|{}|{}\n'.format(title, ','.join(ingredients), rec_text))
            n += 1
            count += 1
            time.sleep(2)
    k += 1
print('Всего ссылок: ', len(rec_urls), ' Уникальных: ', count)

recipes_urls = []
resp = requests.get('https://www.gastronom.ru/recipe/group/3225/recepty-salatov')
soup = BeautifulSoup(resp.text, 'html.parser')
recs = soup.select("div.row.feed h3 > a")

for d in recs:
    recipes_urls.append('https://www.gastronom.ru'+d['href'])
recipes_urls

import re
rec_text = ''
resp = requests.get('https://www.gastronom.ru/recipe/39093/kvashenaya-kapusta-bystrogo-prigotovleniya')
soup = BeautifulSoup(resp.text, 'html.parser')
title = soup.find("h1").text
steps = soup.select("div.step.instruction p")
for step in steps:
    rec_text += step.text.replace('\r\n', '').replace('\xa0', ' ')
rec_text = re.sub(r"\s+", u" ", rec_text).strip()
ingredients_collection = soup.select("li.ingredient")
ingredients = [i.text.replace('\xa0', ' ') for i in ingredients_collection]

import re

with open('recipes_gastronom.csv', 'w') as f:
    f.write('name|ingredients|text\n')

n = 0

for n, url in enumerate(recipes_urls, 1):
    if n == 3:
        break
    rectext = ''
    print(n, url)
    resp_recipe = requests.get(url)
    recipe = BeautifulSoup(resp_recipe.text, 'html.parser')
    recsteps = recipe.select("div.step.instruction p")
    if len(recsteps) == 0:
        print('0')
        continue
    name = recipe.find("h1").text
    ingredients_collection = recipe.select("li.ingredient")
    ingredients = [i.text.replace('\xa0', ' ') for i in ingredients_collection]
    for step in recsteps:
        rectext += step.text.replace('\r\n', '').replace('\xa0', ' ')
    rectext = re.sub(r"\s+", u" ", rectext).strip()
    with open('recipes_gastronom.csv', 'a') as f:
        f.write('{}|{}|{}\n'.format(name, ','.join(ingredients), rectext))
    n += 1
    time.sleep(2)

recp_recipe = requests.get('https://www.utkonos.ru/recipe/1072')
recipe = BeautifulSoup(recp_recipe.text, 'html.parser')

name = recipe.find("h1")
print(name.text)

rectext = ''
recsteps = recipe("div", class_= "cooking_step_desc")
for step in recsteps:
        rectext += step.text
print(rectext)

ingredients_collection = reciepe.select("dd")
del ingredients_collection[len(ingredients_collection) - 1]
ingredients = [i.text.split('—')[0].strip() for i in ingredients_collection]
print(ingredients)

