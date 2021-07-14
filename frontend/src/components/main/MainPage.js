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
            <ul className="films">
                {film.map((f) => {
                    return(
                        <div className="films-item" key={f.id}>
                            <div className="poster-main">
                                <img src={f.image} className="img"></img>
                            </div>
                            <h1><Link className="film-header" to={{ pathname: `/films/${f.id}/`}}>{f.name}</Link></h1>
                        </div>
                    )}
                )}
            </ul>
        </div>
)
}

export default MainPage;