import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';

function FilmDetail({ match }) {

    const[film, setFilm] = useState( [])
    const id = match.params.id
    console.log(id);

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://127.0.0.1:8000/api/films/${id}/`,
        }).then(response => {
            setFilm(response.data)
        })
    }, [id])

    return (
        <div className="div-style">
            <img src={film.image}/>
            <h1>{film.name}</h1>
        </div>
    );
}

export default FilmDetail;