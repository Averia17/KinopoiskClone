import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import { Link } from 'react-router-dom'

function GenreFilms({ match }) {
    const [genre, setGenre] = useState( []);
    const slug = match.params.slug;

    console.log(slug)
    useEffect( () => {
        axios({
            method: "GET",
            url: `http://localhost:8080/api/genres/${slug}/`,
        }).then(response => {
            setGenre(response.data)
        })
    }, [slug])

    return (
        <div>
            <ul>
                {genre.map((film) => {
                    return (
                        <Link key={film.id} to={{pathname: `/films/${film.id}/`}}>{film.name}</Link>
                    )
                })}
            </ul>
        </div>
    )
}

export default GenreFilms;