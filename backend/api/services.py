import time
from concurrent.futures.thread import ThreadPoolExecutor

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
        response = requests.get(
            f'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_250_BEST_FILMS&page={page}',
            headers=headers)
        response = response.json()
        films.extend(response['films'])
    return films


def check_if_empty_films():
    start_time = time.time()
    if Film.objects.all().count() == 0:
        instances = [Film(
            name=film.get('nameRu'),
            year=film.get('year'),
            rating=film.get('rating'),
            image=film.get('posterUrl'),
            filmId=film.get('filmId'))
            for film in get_top_films()
        ]
        Film.objects.bulk_create(instances)
        print(time.time() - start_time)
        get_full_information()
        print(time.time() - start_time)


def get_full_information():

    with ThreadPoolExecutor(max_workers=100) as executor:
        for film in Film.objects.all():
            executor.map(updating_film, [film])
        executor.shutdown(wait=True)


def updating_film(film):
    headers = CaseInsensitiveDict()
    headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
    headers["accept"] = "application/json"
    response = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film.filmId}',
                            headers=headers)
    response = response.json()['data']
    Film.objects.filter(id=film.id).update(
        slogan=response['slogan'],
        description=response['description'],
        filmLength=response['filmLength'],
        type=response['type'],
        ratingAgeLimits=response['ratingAgeLimits'],
        premiereRu=response['premiereRu'],
        premiereWorld=response['premiereWorld'],
        premiereDigital=response['premiereDigital'],
        premiereWorldCountry=response['premiereWorldCountry'],
    )