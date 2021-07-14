import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import { Link } from 'react-router-dom'

function MainPage() {
    const [film, setFilm] = useState( [])

    useEffect( () => {
        axios({
            method: "GET",
            url: 'http://127.0.0.1:8000/api/films/',
        }).then(response => {
            setFilm(response.data)
        })
    }, [])

    return(
        <div className="main-page font-style">
            <div className="films">
                {film.map((f) => {
                    return(
                        <div className="films-item" key={f.id}>
                            <Link  to={{ pathname: `/films/${f.id}/`}}>
                                <div className="poster-main">
                                    <img src={f.image} className="img"></img>
                                </div>
                                <div className="film-description">
                                    <div id="film-title">
                                        <p id="genre">{f.genres[0].title}</p>
                                        <p id="year">{f.year}</p>
                                    </div>
                                    <div id="name">
                                        <p>{f.name}</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    )}
                )}
            </div>
        </div>
)
}

export default MainPage;