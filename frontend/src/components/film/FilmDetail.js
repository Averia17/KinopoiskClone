import React, { useEffect, useState} from 'react';
import axios from 'axios';
import moment from 'moment';
import 'moment/locale/ru'
import '../../App.css';

function FilmDetail({ match }) {

    const[film, setFilm] = useState( [])
    const id = match.params.id;

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://127.0.0.1:8000/api/films/${id}/`,
        }).then(response => {
            setFilm(response.data)
        })
    }, [id])

    let dateRu = moment(film.premiereRu).lang("ru").format('DD MMMM YYYY');
    let dateW = moment(film.premiereWorld).lang("ru").format('DD MMMM YYYY');

    if( film.ratingAgeLimits === null) {
        film.ratingAgeLimits = "0";
    }
    if( film.premiereRu === null) {
        dateRu = "-";
    }
    if( film.premiereWorld === null) {
        dateW = "-";
    }

    return (
        <div className="film-details font-style">
            <div className="poster-details">
                <img src={film.image}/>
                <p className="ageLimit-poster">{film.ratingAgeLimits}+</p>
            </div>
            <div className="film-info">
                <h1>{film.name} ({film.year})</h1>
                <h2 className="film-slogan">{film.slogan}</h2>
                <h2>О фильме</h2>
                <h4>Год выпуска: {film.year}</h4>
                <h4>Страна: {film.premiereWorldCountry}</h4>
                <h4>Премьера в России: {dateRu}</h4>
                <h4>Премьера в мире: {dateW}</h4>
                <h4>Время: {film.filmLength}</h4>
                <p>{film.description}</p>
            </div>
            <div className="film-rating">
                <h3>Рейтинг: {film.rating}</h3>
                <input type="radio" id="star-10" name="rating" value="10"/>
                <label htmlFor="star-10" title="10"></label>
                <input type="radio" id="star-9" name="rating" value="9"/>
                <label htmlFor="star-9" title="9"></label>
                <input type="radio" id="star-8" name="rating" value="8"/>
                <label htmlFor="star-8" title="8"></label>
                <input type="radio" id="star-7" name="rating" value="7"/>
                <label htmlFor="star-7" title="7"></label>
                <input type="radio" id="star-6" name="rating" value="6"/>
                <label htmlFor="star-6" title="6"></label>
                <input type="radio" id="star-5" name="rating" value="5"/>
                <label htmlFor="star-5" title="5"></label>
                <input type="radio" id="star-4" name="rating" value="4"/>
                <label htmlFor="star-4" title="4"></label>
                <input type="radio" id="star-3" name="rating" value="3"/>
                <label htmlFor="star-3" title="3"></label>
                <input type="radio" id="star-2" name="rating" value="2"/>
                <label htmlFor="star-2" title="2"></label>
                <input type="radio" id="star-1" name="rating" value="1"/>
                <label htmlFor="star-1" title="1"></label>
            </div>
        </div>
    );
}

export default FilmDetail;