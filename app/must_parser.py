from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import random

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

# Асинхронная функция для загрузки ПОЛНОЙ страницы
async def get_full_page(playwright):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            browser = await playwright.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1280, "height": 1080})
            await page.goto(f"https://mustapp.com/@{must_nickname}/want")
            #await page.wait_for_load_state("networkidle", timeout=10000)  # 10 секунд таймаут
            await asyncio.sleep(1)
            previous_height = None
            while True:
                current_height = await page.evaluate('document.body.scrollHeight')
                if previous_height == current_height:
                    break
                previous_height = current_height
                await page.keyboard.press('End')
                await asyncio.sleep(0.3)

            content = await page.content()
            await browser.close()
            return content
        except PlaywrightTimeoutError:
            retries += 1
            print(f"Timeout error, retrying {retries}/{max_retries}...")
            await browser.close()
    raise Exception("Failed to load full page after several retries")

# Асинхронная функция для получения рейтинга Must
async def get_rating():
    async with aiohttp.ClientSession() as session:
        url = f"https://mustapp.com/@{must_nickname}/"
        page_content = await fetch_page(session, url)
        soup = bs(page_content, 'html.parser')
        item_rating = soup.find_all('div', class_='profile__meta_item m_laurels')
        if item_rating:
            global rating 
            rating = item_rating[0].find('div', class_='profile__meta_value').text.strip()
        return rating

# Асинхронная функция для получения списка сериалов и фильмов
async def get_list():
    try:
        async with async_playwright() as playwright:
            async with aiohttp.ClientSession() as session:
                serials.clear()
                movies.clear()
                urls.clear()
                urls_movies.clear()

                page_content = await get_full_page(playwright)
                soup = bs(page_content, 'html.parser')

                links = soup.find_all('a', class_='poster js_item')

                tasks = [fetch_page(session, f'https://mustapp.com{link["href"]}') for link in links]
                pages_content = await asyncio.gather(*tasks)

                serials_list = []
                movies_list = []
                for i, page in enumerate(pages_content):
                    show_soup = bs(page, 'html.parser')
                    name = soup.find_all('div', class_='poster__title')[i].text.strip()
                    url = links[i]['href']
                    if show_soup.find('div', class_='productShow'):
                        serials_list.append((name, url))
                        serials.append(name)
                        urls.append(url)
                    else:
                        movies_list.append((name, url))
                        movies.append(name)
                        urls_movies.append(url)
    except Exception as e:
        return False, str(e)
    return True, None

# Асинхронная функция для получения случайного сериала
async def get_random_serial():
    if not serials:
        success, error = await get_list()
        if not success:
            return 'Не удалось загрузить список, ошибка со стороны Must. Попробуйте еще раз!', ''
        if not serials:
            return 'Список запланированных сериалов пуст🤷‍♂️\nЕсли у вас в Must все-таки есть список запланированного, нажмите на "Загрузить список запланированного" в меню или перепривязать Must в разделе "Профиль"', ''
    chosen_serial = random.choice(serials)
    chosen_serial_url = urls[serials.index(chosen_serial)]    
    return chosen_serial, f'https://mustapp.com{chosen_serial_url}'
    
# Асинхронная функция для получения случайного фильма
async def get_random_movie():
    if not movies:
        success, error = await get_list()
        if not success:
            return 'Не удалось загрузить список, ошибка со стороны Must. Попробуйте еще раз!', ''
        if not movies:
            return 'Список запланированных фильмов пуст 🤷‍♂️\nЕсли у вас в Must все-таки есть список запланированного, нажмите на "Загрузить список запланированного" в меню или перепривязать Must в разделе "Профиль"', ''
    chosen_movie = random.choice(movies)
    chosen_movie_url = urls_movies[movies.index(chosen_movie)]
    return chosen_movie, f'https://mustapp.com{chosen_movie_url}'
