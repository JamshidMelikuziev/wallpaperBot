from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import re
from database import WallpapersDB
load_dotenv()
import time



URL = ('https://wallpaperscraft.ru/')
HOST =('https://wallpaperscraft.ru')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}


class CategoryParser:
    def __init__(self, url, name, category_id, pages: int = 3, download=False):
        self.url = url
        self.name = name
        self.category_id = category_id
        self.pages = pages
        self.download = download

    def get_html(self, i):
        try:
            html = requests.get(self.url + f'/page{i}', headers=HEADERS).text
            return html
        except:
            print('Не удалось получить страницу')

    def get_soup(self, i):
        html = self.get_html(i)
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_data(self):
        for i in range(1, self.pages + 1):  # 1, 2, 3
            soup = self.get_soup(i)
            images_blocks = soup.find_all('a', class_='wallpapers__link')
            for block in images_blocks:
                try:
                    page_link = HOST + block['href']
                    print(page_link)
                    page_html = requests.get(page_link, headers=HEADERS).text
                    del page_link
                    page_soup = BeautifulSoup(page_html, 'html.parser')
                    resolution = page_soup.find_all('span', class_='wallpaper-table__cell')[1].get_text(strip=True)

                    image_link = block.find('img', class_='wallpapers__image').get('src')
                    image_link = image_link.replace('300x168', resolution)

                    WallpapersDB.insert_into_images(image_link, self.category_id)

                    if self.download:
                        if self.name not in os.listdir():
                            os.mkdir(str(self.name))
                        responceImage = requests.get(image_link, headers=HEADERS).content
                        image_name = image_link.replace('https://images.wallpaperscraft.ru/image/single/', '')
                        with open(file=f'{self.name}/{image_name}', mode='wb') as file:
                            file.write(responceImage)


                except Exception as e:
                    pass


def parsing():
    html = requests.get(URL, headers=HEADERS).text
    soup = BeautifulSoup(html, 'html.parser')
    block = soup.find('ul', class_='filters__list')
    filters = block.find_all('a', class_='filter__link')
    for f in filters:

        link = HOST + f.get('href')
        print(link)
        name = f.get_text(strip=True)
        print(name)
        true_name = re.findall(r'[3]*[Dа-яА-Я]+', name)[0]
        print(true_name)
        pages = int(re.findall(r'[0-9][0-9]+', name)[0]) // 15
        print(pages)
        WallpapersDB.insert_category(true_name)
        category_id = WallpapersDB.get_category_id(true_name)
        print(category_id)
        parser = CategoryParser(url=link,
                                name=true_name,
                                category_id=category_id)
        parser.get_data()



parsing()
