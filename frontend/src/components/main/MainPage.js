import React, { useEffect, useState} from 'react';
import axios from 'axios';
import 'D:/KinopoiskClone/KinopoiskClone/frontend/src/App.css';
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
        <div>
            <ul className="films">
                {film.map((f) => {
                    return(
                        <div className="item" key={f.id}>
                            <img src={f.image} className="img"></img>
                            <h1><Link className="link-film" to={{ pathname: `/films/${f.id}/`}}>{f.name}</Link></h1>
                            <h2 className="filmInfo">{f.year}</h2>
                            <h2 className="filmInfo">{f.rating}</h2>
                        </div>
                    )}
                )}
            </ul>
        </div>
    )
}

export default MainPage;