from LxmlSoup import LxmlSoup as ls
import requests
import random


must_nickname = '' 
rating = ''
serials = []
movies = []
urls = []
urls_movies = []
chosen_serial = ''
chosen_serial_url = ''
chosen_movie = ''
chosen_movie_url = ''

def must_rating():
    html = requests.get(f'https://mustapp.com/@{must_nickname}/want').text
    soup = ls(html)

    item_rating = soup.find_all('div', class_='profile__meta_item m_laurels')
    for i in enumerate(item_rating):
        global rating 
        rating = soup.find_all('div', class_='profile__meta_value')[0].text()
    


def random_project():
    html = requests.get(f'https://mustapp.com/@{must_nickname}/want').text
    soup = ls(html)

    links = soup.find_all('a', class_='poster js_item')

    for i, link in enumerate(links):
        url = link.get('href')
        html_shows = requests.get(f'https://mustapp.com/{url}').text
        shows = ls(html_shows)
        check_serial = shows.find_all('div', class_='productShow')
        if not check_serial:
            movie_name = soup.find_all('div', class_='poster__title')[i].text()
            movies.append(movie_name)
            urls_movies.append(url)
        else:
            name = soup.find_all('div', class_='poster__title')[i].text()
            serials.append(name)
            urls.append(url)
    
    global chosen_serial
    global chosen_serial_url
    chosen_serial = random.choice(serials)
    chosen_serial_number = serials.index(chosen_serial)
    chosen_serial_url = 'https://mustapp.com' + urls[chosen_serial_number]
    
    global chosen_movie
    global chosen_movie_url
    chosen_movie = random.choice(movies)
    chosen_movie_number = movies.index(chosen_movie)
    chosen_movie_url = 'https://mustapp.com' + urls_movies[chosen_movie_number]
    
    movies.clear()
    serials.clear()
    urls.clear()
    urls_movies.clear()