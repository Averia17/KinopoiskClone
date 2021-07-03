import requests
from requests.structures import CaseInsensitiveDict


def get_top_films():
    headers = CaseInsensitiveDict()
    headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
    headers["accept"] = "application/json"
    response = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_250_BEST_FILMS&page=1',
                            headers=headers)

    return response.json()['films']
