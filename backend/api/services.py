import requests
from requests.structures import CaseInsensitiveDict

from backend.models import Film


def get_top_films():
    headers = CaseInsensitiveDict()
    headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
    headers["accept"] = "application/json"
    response = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_250_BEST_FILMS&page=1',
                            headers=headers)
    response = response.json()
    films = []
    for page in range(1, response['pagesCount'] + 1):
        response = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_250_BEST_FILMS&page={page}',
                                headers=headers)
        response = response.json()
        films.extend(response['films'])
    return films


def check_if_empty_films():
    if not Film.objects.all().exists():
        for film in get_top_films():
            f = Film(name=film.get('nameRu'),
                     year=film.get('year'),
                     rating=film.get('rating'),
                     image=film.get('posterUrl'),
                     filmId=film.get('filmId')
                     )
            f.save()
