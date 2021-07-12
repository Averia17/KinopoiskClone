import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from requests.structures import CaseInsensitiveDict

from backend.models import Film, Staff


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
        print("films empty")
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
        get_staff()
        print(time.time() - start_time)
    get_staff_full_information()
        # print(time.time() - start_time)


def get_full_information():
    with ThreadPoolExecutor(max_workers=3) as executor:
        for film in Film.objects.all():
            executor.map(updating_film, [film])
        executor.shutdown(wait=True)


def updating_film(film):
    headers = CaseInsensitiveDict()
    headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
    headers["accept"] = "application/json"
    response = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film.filmId}',
                            headers=headers)
    if response.status_code == 429:
        print("blyat suka ")
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
        # genres=response['genres'],
        # budget=response['budget']['budget'],
    )


def get_staff():
    with ThreadPoolExecutor(max_workers=3) as executor:
        for film in Film.objects.all():
            executor.map(get_film_staff, [film])
        executor.shutdown(wait=True)


def get_film_staff(film):
    if not Film.objects.get(pk=film.id).staff.exists():
        headers = CaseInsensitiveDict()
        headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
        headers["accept"] = "application/json"
        response = requests.get(f'https://kinopoiskapiunofficial.tech/api/v1/staff?filmId={film.filmId}',
                                headers=headers)
        if response.status_code == 429:
            print("blyat suka ")
        response = response.json()
        instances = []
        for staff in response:
            if not Staff.objects.filter(staffId=staff.get('staffId')).exists():
                s = Staff(
                    nameRu=staff.get('nameRu'),
                    staffId=staff.get('staffId'),
                    description=staff.get('description'),
                    image=staff.get('posterUrl'),
                    professionText=staff.get('professionText'),
                    professionKey=staff.get('professionKey'))
                s.save()
            else:
                s = Staff.objects.get(staffId=staff.get('staffId'))
            instances.append(s)
        # instances = [
        #     Staff(
        #         nameRu=staff.get('nameRu'),
        #         staffId=staff.get('staffId'),
        #         description=staff.get('description'),
        #         image=staff.get('posterUrl'),
        #         professionText=staff.get('professionText'),
        #         professionKey=staff.get('professionKey'))
        #     for staff in response
        # ]
        #instances = Staff.objects.bulk_create(instances)

        current_film = Film.objects.get(pk=film.id)
        for instance in instances:
            current_film.staff.add(instance)
        print(current_film)

        # ThroughFilmStaffModel = Film.staff.through
        # through_list = []
        # for instance in instances:
        #     print(instance.id)
        #     film_staff = ThroughFilmStaffModel(film_id=current_film.id, staff_id=instance.id)
        #     through_list.append(film_staff)
        # ThroughFilmStaffModel.objects.bulk_create(through_list)
        # Staff.objects.bulk_insert(instances)
    else:
        return
##...А зори здесь тихие


def get_staff_full_information():
    with ThreadPoolExecutor(max_workers=3) as executor:
        for staff in Staff.objects.all():
            executor.map(update_staff, [staff])
        executor.shutdown(wait=True)


def update_staff(staff):
    if Staff.objects.get(pk=staff.id).birthday is None:
        headers = CaseInsensitiveDict()
        headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
        headers["accept"] = "application/json"
        response = requests.get(f'https://kinopoiskapiunofficial.tech/api/v1/staff/{staff.staffId}',
                                headers=headers)

        response = response.json()

        Staff.objects.filter(id=staff.id).update(
            birthday=response.get('birthday'),
            image=response.get('posterUrl'),
            death=response.get('death'),
            age=response.get('age'),
            growth=response.get('growth'),
            profession=response.get('profession'),
        )
