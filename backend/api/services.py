import json
import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from requests.structures import CaseInsensitiveDict

from backend.models import Film, Staff, Genre, Country


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
    # get_staff()
    # print(time.time() - start_time)
    # get_staff_full_information()
    # print(time.time() - start_time)
    # get_genres()
    # print(time.time() - start_time)
    # get_countries()
    # print(time.time() - start_time)
    get_films_videos()
    print(time.time() - start_time)



def get_full_information():
    with ThreadPoolExecutor(max_workers=3) as executor:
        for film in Film.objects.all():
            executor.map(updating_film, [film])
        executor.shutdown(wait=True)


def updating_film(film):
    if not Film.objects.get(pk=film.id).countries.exists():

        headers = CaseInsensitiveDict()
        headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
        headers["accept"] = "application/json"
        response = requests.get(
            f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film.filmId}?append_to_response=BUDGET',
            headers=headers)
        if response.status_code == 429:
            print("blyat suka ")
        response_data = response.json()['data']
        response = response.json()
        current_film = Film.objects.get(pk=film.id)
        current_film.slogan = response_data.get('slogan')
        current_film.description = response_data.get('description')
        current_film.filmLength = response_data.get('filmLength')
        current_film.type = response_data.get('type')
        current_film.ratingAgeLimits = response_data.get('ratingAgeLimits')
        current_film.premiereRu = response_data.get('premiereRu')
        current_film.premiereDigital = response_data.get('premiereDigital')
        current_film.premiereWorld = response_data.get('premiereWorld')
        current_film.premiereWorldCountry = response_data.get('premiereWorldCountry')
        current_film.budget = response.get('budget').get('budget')
        current_film.grossRu = response.get('budget').get('grossRu')
        current_film.grossWorld = response.get('budget').get('grossWorld')
        current_film.facts = response_data.get('facts')
        current_film.save()

        genres = [genre['genre'] for genre in response_data['genres']]
        for genre in genres:
            current_film.genres.add(Genre.objects.get_or_create(title=genre))
        countries = [country['country'] for country in response_data['countries']]
        for country in countries:
            current_film.countries.add(Country.objects.get_or_create(title=country))
        current_film.save()
    else:
        print(film.name)
        return


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
        # instances = Staff.objects.bulk_create(instances)

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
        print(staff.nameRu + ' updated')
        Staff.objects.filter(id=staff.id).update(
            birthday=response.get('birthday'),
            image=response.get('posterUrl'),
            death=response.get('death'),
            age=response.get('age'),
            growth=response.get('growth'),
            profession=response.get('profession'),
        )
    else:
        return


def get_genres():
    films = get_top_films()

    genres = Genre.objects.all()

    genres_titles = [genre.title for genre in genres]
    for film in films:
        for genre in film.get('genres'):
            if genre['genre'] not in genres_titles:
                print(genre['genre'])
                g = Genre(title=genre['genre'])
                g.save()
                genres = Genre.objects.all()
                genres_titles = [genre.title for genre in genres]


def get_countries():
    films = get_top_films()

    countries = Country.objects.all()

    countries_titles = [country.title for country in countries]
    for film in films:
        for country in film.get('countries'):
            if country['country'] not in countries_titles:
                print(country['country'])
                c = Country(title=country['country'])
                c.save()
                countries = Country.objects.all()
                countries_titles = [country.title for country in countries]


def get_films_videos():
    with ThreadPoolExecutor(max_workers=3) as executor:
        for film in Film.objects.all():
            executor.map(get_film_video, [film])
        executor.shutdown(wait=True)


def get_film_video(film):
    #if not Film.objects.get(pk=film.id).trailers:
    headers = CaseInsensitiveDict()
    headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
    headers["accept"] = "application/json"
    response = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film.filmId}/videos',
                            headers=headers)
    response = response.json()
    trailers_from_response = response.get('trailers')
    teasers_from_response = response.get('teasers')
    trailers = []
    teasers = []
    for trailer in trailers_from_response:
        dict_to_append = {'name': trailer.get('name'), 'url': trailer.get('url'), 'official': ''}

        if trailer.get('size') is not None:
            dict_to_append['official'] = 'True'
        else:
            dict_to_append['official'] = 'False'
        #print(dict_to_append)
        trailers.append(dict_to_append)

    for teaser in teasers_from_response:
        dict_to_append = {'name': teaser.get('name'), 'url': teaser.get('url'), 'official': ''}

        if teaser.get('size') is not None:
            dict_to_append['official'] = 'True'
        else:
            dict_to_append['official'] = 'False'
        teasers.append(dict_to_append)

    current_film = Film.objects.get(pk=film.id)

    current_film.trailers = trailers
    current_film.teasers = teasers
    current_film.save()
    print(current_film)
    #
    # else:
    #     return
