import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import { Link, useParams } from 'react-router-dom'
import StarIcon from '@mui/icons-material/Star';
import Tokens from "../../services/auth-header";
import queryString from 'query-string';
import {handleMoveToFavorite} from "../../services/favorite.service";

function MainPage(props) {
    const [film, setFilm] = useState([]);
    const [favorites, setFavorites] = useState([]);
    const slug = props?.match?.params?.slug || queryString.parse(props?.location?.search).search;
    useEffect(() => {
        document.title = "Главная страница";
        props.getFilms(slug).then(response => {
            setFilm(response.data)
        })
    }, [])
    useEffect(() => {
        const accessToken = Tokens.AccessTokenHeader();
        axios({
            method: "GET",
            url: `http://localhost:8080/api/favorites/`,
            headers: {
                'Content-type': 'application/json',
                'Authorization': accessToken
            },
        }).then(response => {
            setFavorites(response.data)
        }).catch(error => {
            setFavorites([])
        })
    }, [])


    const moveToFavorites = (key, isFavorite) => {
        handleMoveToFavorite(key, isFavorite).then((response) => {
            setFavorites(response.data)
        }).catch(error => {
            if (error.request?.status === 401) {
                alert("You need to login")
            } else
                console.log(error)
        })
    }

    const isExists = (favoriteId) => favorites.includes(favoriteId)
    return(
        <div className="main-page font-style">
            <div className="films">
                {film.map((f) => {
                    const isFavorite = isExists(f.id)
                    return(
                        <div className="films-item" key={f.id}>
                            <button onClick={() => moveToFavorites(f.id, isFavorite)} style={{background: 'none', border:'none'}}>
                                <StarIcon fontSize={"large"} style={{color: isFavorite?  '#5CE9E2' : 'azure'}}/>
                            </button>
                            <Link to={{ pathname: `/films/${f.id}/`}}>
                                <div className="poster-main">
                                    <img src={f.image} className="main-img"></img>
                                </div>
                                <div className="film-description">
                                    <div id="film-title">
                                        <p id="genre">{f.genres__title}</p>
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