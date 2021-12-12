import React, { useEffect, useState} from 'react';
import moment from 'moment';
import 'moment/locale/ru'
import '../../App.css';
import { Link, useParams } from 'react-router-dom'

function FilmDetail(props) {
    const [film, setFilm] = useState( []);
    const id = props?.match?.params?.id;

    useEffect(() => {
        document.title = `${film.name}`;
        props.getFilms(id).then(response => {
            setFilm(response.data)
        })
    }, [])
    const dateFormat = 'DD MMMM YYYY';
    const dateRu = moment(film?.premiereRu).lang("ru").format(dateFormat);
    const dateWorld = moment(film?.premiereWorld).lang("ru").format(dateFormat);
    const actors = film?.staff?.filter(function(f) {
        return f.professionKey === "ACTOR";
    });
    const countries = film?.countries?.map((c, index) => {
        return( c.title + (index != (film?.countries.length - 1) ? ',' : '' ))
    });
    let emptiness = [];
    return (
        <div className="film-details font-style">
            <div className="poster-details">
                <img className="poster-img" src={film.image}/>
                <p className="ageLimit-poster">{
                    film?.ratingAgeLimits ? film?.ratingAgeLimits : 0 }+
                </p>
            </div>
            <div className="film-info">
                <div>
                    <h1>{film.name} ({film.year})</h1>
                    <h2 className="film-slogan">{film.slogan}</h2>
                </div>
                <h2>О фильме</h2>
                <p>Год выпуска: {film.year}</p>
                <div className="film-countries-genres">
                    <ul className="film-list">Страна: {film.countries?.map((с, index) => {
                        return(
                            <Link className="list-item" key={index} to={{ pathname: `/countries/${с.slug}/`}}>{с.title}</Link>
                        )
                    })}</ul>
                    <ul className="film-list">Жанр: {film.genres?.map((g, index) => {
                        return(
                            <Link className="list-item" key={index} to={{ pathname: `/genres/${g.slug}/`}}>{g.title}</Link>
                        )
                    })}</ul>
                </div>
                <p>Премьера в мире: {
                    moment(dateWorld, dateFormat, true).isValid() ? dateWorld : "-"
                }
                </p>
                <p>Премьера в России: {
                    moment(dateRu, dateFormat, true).isValid()  ? dateRu : "-"
                }
                </p>
                <p>Бюджет: {
                    film?.budget ? film?.budget : "-"
                }
                </p>
                <p>Сборы в мире: ${
                    film?.grossWorld ? film?.grossWorld : 0
                }
                </p>
                <p>Сборы в России: ${
                    film?.grossRu ? film?.grossRu : 0
                }
                </p>
                <p>Время: {film?.filmLength}</p>
            </div>
            <div className="rating-and-actors">
                <div className="film-rating">
                    <h1>{film.rating}</h1>
                    <div className="rating-body">
                        <div className="rating-active" style={{width: `${film.rating / 0.1}%`}}></div>
                    </div>
                </div>
                <div className="film-actors">
                    <h3>В главных ролях</h3>
                    <div>
                        <ul className="actors">
                            {actors ? actors?.map((a, index) => {
                                    if(index < 10)
                                        return(
                                        <div className="actors-item" key={a.id}>
                                            <p><Link key={a.id} className="actor" to={{ pathname: `/staff/${a.id}/`}}>{a.nameRu}</Link></p>
                                        </div>
                                )}
                            ) : emptiness.unshift("gecnj")}
                        </ul>
                        <p>{emptiness[0]}</p>
                        <Link key={film.id} id="others" to={{ pathname: `/films/${film.id}/staff`}}>Остальные персоны</Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default FilmDetail;