import React, {useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import {Link, useParams, useHistory} from 'react-router-dom'
import StarIcon from '@mui/icons-material/Star';
import Tokens from "../../services/auth-header";
import queryString from 'query-string';
import {handleMoveToFavorite} from "../../services/favorite.service";
import Film from "./Film";

function MainPage(props) {
    const [film, setFilm] = useState([]);
    const [favorites, setFavorites] = useState([]);
    const slug = props?.match?.params?.slug ||  queryString.parse(props?.location?.search);
    const slug = props?.match?.params?.slug || queryString.parse(props?.location?.search).search;
    const history = useHistory();
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
    const updateFavorites = (films) => {
        setFavorites(films);
    }
    return (
        <div className="main-page font-style">
            <div className="films">
                {film.map((f) => {
                        return (
                            <Film key={film.id} film={f} updateFavorites={updateFavorites} favorites={favorites}/>
                        )
                    }
                )}
            </div>
        </div>
    )
}

export default MainPage;