import React, { useEffect, useState} from 'react';
import axios from 'axios';
import moment from 'moment';
import 'moment/locale/ru'
import '../../App.css';
import { Link } from 'react-router-dom'


function FilmDetail({ match }) {
    const[film, setFilm] = useState( []);
    const[genre, setGenre] = useState( []);
    const[country, setCountry] = useState( []);
    const id = match.params.id;

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://127.0.0.1:8000/api/films/${id}/`,
        }).then(response => {
            setFilm(response.data)
        })
    }, [id])

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://127.0.0.1:8000/api/genres/`,
        }).then(response => {
            setGenre(response.data)
        })
    }, [])

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://127.0.0.1:8000/api/countries/`,
        }).then(response => {
            setCountry(response.data)
        })
    }, [])

    useEffect(() => {
        document.title = `${film.name}`;
    })
    let dateRu = moment(film.premiereRu).lang("ru").format('DD MMMM YYYY');
    let dateW = moment(film.premiereWorld).lang("ru").format('DD MMMM YYYY');

    if(film.ratingAgeLimits === null) {
        film.ratingAgeLimits = "0";
    }
    if(film.budget === null) {
        film.budget = "-";
    }
    if(film.grossRu === null) {
        film.grossRu = "0";
    }
    if(film.grossWorld === null) {
        film.grossWorld = "0";
    }
    if(film.premiereRu === null) {
        dateRu = "-";
    }
    if(film.premiereWorld === null) {
        dateW = "-";
    };

    var actors = film.staff?.filter(function(f) {
        return f.professionKey === "ACTOR";
    });

    let countries = film.countries?.map((c, index) => {return( c.title + (index != (film.countries.length-1) ? ',' : '' ))});

    const star = (film.rating / 0.1)

    return (
        <div className="film-details font-style">
            <div className="poster-details">
                <img src={film.image}/>
                <p className="ageLimit-poster">{film.ratingAgeLimits}+</p>
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
                <p>Премьера в мире: {dateW}</p>
                <p>Премьера в России: {dateRu}</p>
                <p>Бюджет: {film.budget}</p>
                <p>Сборы в мире: ${film.grossWorld}</p>
                <p>Сборы в России: ${film.grossRu}</p>
                <p>Время: {film.filmLength}</p>
            </div>
            <div className="rating-and-actors">
                <div className="film-rating">
                    <h1>{film.rating}</h1>
                    <div className="rating-body">
                        <div className="rating-active" style={{width: `${star}%`}}></div>
                    </div>
                </div>
                <div className="film-actors">
                    <h3>В главных ролях</h3>
                    <div>
                        <ul className="actors">
                            {actors?.map((a, index) => {
                                    if(index < 10)
                                        return(
                                        <div className="actors-item" key={a.id}>
                                            <p><Link key={a.id} className="actor" to={{ pathname: `/staff/${a.id}/`}}>{a.nameRu}</Link></p>
                                        </div>
                                )}
                            )}
                        </ul>
                        <Link key={film.id} id="others" to={{ pathname: `/films/${film.id}/staff`}}>Остальные актёры</Link>
                    </div>
                </div>
            </div>
        </div>

    );
}

export default FilmDetail;