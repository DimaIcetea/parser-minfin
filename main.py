import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = "https://minfin.com.ua/"
URL = "https://minfin.com.ua/ua/cards/"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0')
    cards = []
    
    for item in items:
        cards.append(
            {
              'title':item.find('div', class_='be80pr-15').find('a').get_text(strip=True),
              'link_product':item.find('div', class_='be80pr-15').find('a').get('href'),
              'brand':item.find('div', class_='be80pr-16').find('span').get_text(strip=True),
              'card_img':item.find('div', class_='be80pr-9').find('img').get('src'),
            }
        )
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта', 'Ссылка на продукт', 'Банк', 'Изображение карты'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['brand'], item['card_img']])


def parser():
    PAGENATION = input("Укажите количество страниц для парсинга: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards= []
        print('Парсим страницу')
        cards.extend(get_content(html.text))
        print("Парсинг закончен")
        save_doc(cards, CSV)
    else:
        print('Error')

parser()


