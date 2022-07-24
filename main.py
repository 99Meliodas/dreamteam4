import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv
def get_data():
    r = requests.get('https://lalafo.kg/kyrgyzstan/q-%D0%BF%D0%BE%D1%81%D1%83%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0', verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    items = soup.findAll('div', class_='main-feed__wrapper')
    return items

def parse_data():
    result = []
    all_names = []
    all_prices = []
    all_images = []
    l = 0
    for item in get_data():
        names = item.findAll('a', class_='adTile-title')
        image = item.findAll('img', class_='lazyload')
        price = item.findAll('p', class_='adTile-price')

        for k in price:
            if 'old-price' not in k['class']:
                all_prices.append(k.get_text())
                print(k['class'])

        for i in image:
            if i['alt'] != "paid feature icon" and i['alt'] != "":
               all_images.append(i['data-src'])
                    
        for j in names:
            all_names.append(j.get_text())
            result.append({
                'names': j.get_text(),
                'link': 'https://lalafo.kg' + j['href'],
                'price': all_prices[l],
                'link_image': all_images[l]
            })
            l += 1
    return result

def save_data():
    with open('result.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['names', 'link', 'price', 'link_image'])
        writer.writeheader()
        writer.writerows(parse_data())

if __name__ == '__main__':
    save_data()
