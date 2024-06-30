import aiohttp
import random
import asyncio
from bs4 import BeautifulSoup as bs

# Глобальные переменные для хранения данных пользователя и рейтинга
must_nickname = ''
rating = ''
serials = []
movies = []
urls = []
urls_movies = []

# Асинхронная функция для загрузки страницы
async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

# Асинхронная функция для получения рейтинга Must
async def must_rating():
    async with aiohttp.ClientSession() as session:
        page_content = await fetch_page(session, f'https://mustapp.com/@{must_nickname}/want')
        soup = bs(page_content, 'html.parser')
        item_rating = soup.find_all('div', class_='profile__meta_item m_laurels')
        if item_rating:
            global rating 
            rating = item_rating[0].find('div', class_='profile__meta_value').text.strip()
    return rating

# Асинхронная функция для получения списка сериалов
async def get_list():
    serials.clear()
    movies.clear()
    urls.clear()
    urls_movies.clear()
    async with aiohttp.ClientSession() as session:
        page_content = await fetch_page(session, f'https://mustapp.com/@{must_nickname}/want')
        soup = bs(page_content, 'html.parser')

        links = soup.find_all('a', class_='poster js_item')
        tasks = [fetch_page(session, f'https://mustapp.com{link["href"]}') for link in links]

        pages_content = await asyncio.gather(*tasks)

        serials_list = []
        movies_list = []
        for i, page in enumerate(pages_content):
            show_soup = bs(page, 'html.parser')
            if show_soup.find('div', class_='productShow'):
                name = soup.find_all('div', class_='poster__title')[i].text.strip()
                url = links[i]['href']
                serials_list.append((name, url))
                serials.append(name)
                urls.append(url)
            else:
                name = soup.find_all('div', class_='poster__title')[i].text.strip()
                url = links[i]['href']
                movies_list.append((name, url))
                movies.append(name)
                urls_movies.append(url)

# Асинхронная функция для получения случайного сериала
async def get_random_serial():
    if not serials:
        await get_list()
    chosen_serial = random.choice(serials)
    chosen_serial_url = urls[serials.index(chosen_serial)]    
    return chosen_serial, f'https://mustapp.com{chosen_serial_url}'

# Асинхронная функция для получения случайного фильма
async def get_random_movie():
    if not movies:
        await get_list()
    chosen_movie = random.choice(movies)
    chosen_movie_url = urls_movies[movies.index(chosen_movie)]
    return chosen_movie, f'https://mustapp.com{chosen_movie_url}'
