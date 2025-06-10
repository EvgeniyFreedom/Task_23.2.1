import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_html(page_index):
    """Запрашивает HTML-страницу рейтинга фильмов"""
    endpoint = f'https://www.kinoafisha.info/rating/movies/?page={page_index}'
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.text
    except requests.RequestException as err:
        print(f"Ошибка при запросе страницы {page_index}: {err}")
        return ""

def parse_movies_from_page(html):
    """Парсит фильмы с одной HTML-страницы"""
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.select('div.movieList_item.movieItem.movieItem-rating.movieItem-position')
    parsed_movies = []

    for block in blocks:
        title_tag = block.select_one('div.movieItem_info a')
        rating_tag = block.select_one('span.movieItem_itemRating.miniRating.miniRating-good')
        genre_tag = block.select_one('div.movieItem_details span')

        movie = {
            "Фильм": title_tag.text.strip() if title_tag else "Не указано",
            "Жанр": genre_tag.text.strip() if genre_tag else "Не указано",
            "Рейтинг": rating_tag.text.strip() if rating_tag else "Не указано"
        }
        parsed_movies.append(movie)
    
    return parsed_movies

def gather_movie_data(limit=1000):
    """Собирает данные о фильмах с нескольких страниц"""
    results = []
    page = 0

    while len(results) < limit:
        html_doc = fetch_html(page)
        if not html_doc:
            break

        movies = parse_movies_from_page(html_doc)
        if not movies:
            break

        for movie in movies:
            if len(results) >= limit:
                break
            results.append(movie)

        page += 1

    return results

if __name__ == "__main__":
    movie_info = gather_movie_data()
    df = pd.DataFrame(movie_info)
    df.to_excel("movie_ratings.xlsx", index=False)
    print("Файл успешно сохранён как movie_ratings.xlsx")
