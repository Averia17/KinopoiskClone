import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from pytils.translit import slugify
from requests.structures import CaseInsensitiveDict

from kinopoiskclone.api.serializers import FilmListSerpySerializer
from kinopoiskclone.models import Film, Staff, Genre, Country


def serialize_value_list_films(qs):
    queryset = qs.distinct('id', 'name', 'year', 'image').values_list(
        'id', 'name', 'year', 'image', 'genres__title', named=True
    )

    return FilmListSerpySerializer(queryset, many=True)


def delete_saved_users_film(self):
    userprofile = self.request.user.userprofile
    pk = self.request.data.get('id')
    film = Film.objects.get(pk=pk)
    userprofile.saved_films.remove(film)


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
    # get_films_videos()
    # print(time.time() - start_time)
    # get_filters()
    # print(time.time() - start_time)

    # get_all_filtered_films()
    # print(time.time() - start_time)
    # get_full_information()
    # print(time.time() - start_time)
    # get_staff()
    # print(time.time() - start_time)
    # get_staff_full_information()
    # print(time.time() - start_time)
    # delete_clones()
    # list_films()


def get_full_information():
    with ThreadPoolExecutor(max_workers=20) as executor:
        for film in Film.objects.all():
            executor.map(updating_film, [film])
        executor.shutdown(wait=True)


def updating_film(film):
    current_film = Film.objects.get(pk=film.id)
    if not current_film.countries.exists():

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
        # current_film.save()
        # ThroughGenresModel = Film.genres.through
        # ThroughCountryModel = Film.countries.through
        # genres = [genre['genre'] for genre in response_data['genres']]
        # instances = []
        # for genre in genres:
        #     instances.append(ThroughGenresModel(film_id=current_film.id, genre_id=Genre.objects.get(title=genre).id))
        # ThroughGenresModel.objects.bulk_create(instances)
        # countries = [country['country'] for country in response_data['countries']]
        # instances = []
        # for country in countries:
        #     instances.append(ThroughCountryModel(film_id=current_film.id,
        #                                          genre_id=Genre.objects.get(title=country).id))
        # ThroughCountryModel.objects.bulk_create(instances)
        # genres = [genre['genre'] for genre in response_data['genres']]
        # grs = [Genre.objects.get(title=genre) for genre in genres]
        # current_film.genres.add(*grs)
        # countries = [country['country'] for country in response_data['countries']]
        # cntrs = [Country.objects.get(title=country) for country in countries]
        # current_film.countries.add(*cntrs)

        current_film.save()
        print(current_film.genres.all())
    else:
        print(film.name)
        return


def get_staff():
    films = Film.objects.filter(type='FILM').order_by('-year')
    with ThreadPoolExecutor(max_workers=20) as executor:
        for film in films:
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
        current_film.staff.add(*instances)
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


def get_staff_full_information():
    with ThreadPoolExecutor(max_workers=15) as executor:
        for staff in Staff.objects.all():
            executor.map(update_staff, [staff])
        executor.shutdown(wait=True)


def update_staff(staff):
    current_staff = Staff.objects.get(pk=staff.id)
    if current_staff.birthday is None:
        headers = CaseInsensitiveDict()
        headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
        headers["accept"] = "application/json"
        response = requests.get(f'https://kinopoiskapiunofficial.tech/api/v1/staff/{staff.staffId}',
                                headers=headers)

        response = response.json()
        current_staff.birthday = response.get('birthday')
        current_staff.image = response.get('posterUrl')
        current_staff.death = response.get('death')
        current_staff.age = response.get('age')
        current_staff.growth = response.get('growth')
        current_staff.profession = response.get('profession')
        current_staff.save()
        print(staff.nameRu + ' updated')

    else:
        return


def get_films_videos():
    with ThreadPoolExecutor(max_workers=3) as executor:
        for film in Film.objects.all():
            executor.map(get_film_video, [film])
        executor.shutdown(wait=True)


def get_film_video(film):
    current_film = Film.objects.get(pk=film.id)

    if not current_film.trailers:
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
            # print(dict_to_append)
            trailers.append(dict_to_append)

        for teaser in teasers_from_response:
            dict_to_append = {'name': teaser.get('name'), 'url': teaser.get('url'), 'official': ''}

            if teaser.get('size') is not None:
                dict_to_append['official'] = 'True'
            else:
                dict_to_append['official'] = 'False'
            teasers.append(dict_to_append)

        current_film.trailers = trailers
        current_film.teasers = teasers
        current_film.save()
        print(current_film)

    else:
        return


def get_filters():
    headers = CaseInsensitiveDict()
    headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
    headers["accept"] = "application/json"
    response = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/filters',
                            headers=headers)
    response = response.json()
    genres = response['genres']
    countries = response['countries']

    for genre in genres:
        print(genre['genre'])

        if not Genre.objects.filter(title=genre['genre']).exists():
            g = Genre(title=genre['genre'])
            print(genre['genre'])
            g.save()
    for country in countries:
        if not Country.objects.filter(title=country['country']).exists():
            c = Country(title=country['country'])
            print(country['country'])
            c.save()


def get_all_filtered_films():
    with ThreadPoolExecutor(max_workers=5) as executor:
        yearTo = 1971
        while yearTo != 2023:
            executor.map(get_filtered_films, [yearTo])
            yearTo += 1
    executor.shutdown(wait=True)


def get_filtered_films(yearTo):
    headers = CaseInsensitiveDict()
    headers["X-API-KEY"] = "3b1e332f-f435-484a-acda-e9b053640444"
    headers["accept"] = "application/json"
    url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?country=0&order=RATING&type=FILM&ratingFrom={ratingFrom}&ratingTo={ratingTo}&yearFrom={yearFrom}&yearTo={yearTo}&page={page}'
    ratingTo = 6
    while ratingTo != 10:
        response = requests.get(
            url.format(ratingFrom=ratingTo - 1, ratingTo=ratingTo, yearFrom=yearTo - 1, yearTo=yearTo, page=1),
            headers=headers)
        if response.status_code == 429:
            print("blyat suka ")
        response = response.json()
        instances = []
        for page in range(1, response.get('pagesCount') + 1):
            response = requests.get(
                url.format(ratingFrom=ratingTo - 1, ratingTo=ratingTo, yearFrom=yearTo - 1, yearTo=yearTo, page=page),
                headers=headers)
            response = response.json()
            response = response.get('films')
            for film in response:
                if not Film.objects.filter(filmId=film.get('filmId')).exists():
                    f = Film(
                        name=film.get('nameRu'),
                        year=film.get('year'),
                        rating=film.get('rating'),
                        image=film.get('posterUrl'),
                        filmId=film.get('filmId'))
                    instances.append(f)
                    print(film.get('nameRu'))
        Film.objects.bulk_create(instances)
        ratingTo += 1


def check_is_clone(staff):
    query = Staff.objects.filter(staffId=staff.staffId)
    print('works')
    if len(query) > 1:
        try:
            query[1].delete()
            print(query)
        except Exception as ex:
            print(ex)


def delete_clones():
    # import sqlite3
    # conn = sqlite3.connect('KinopoiskClone.db', isolation_level=None)
    # conn.execute("VACUUM")
    # conn.close()
    with ThreadPoolExecutor(max_workers=15) as executor:
        n = 0
        for staff in Staff.objects.all().reverse():
            executor.map(check_is_clone, [staff])
            n += 1
            print(n)
        executor.shutdown(wait=True)


def list_films():
    for film in Film.objects.all():
        if not film.slug:
            slug = slugify(film.name)
            film.slug = slug
            film.save()
            print(film.slug)
