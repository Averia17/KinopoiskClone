import React, {useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import Tokens from "../../services/auth-header";
import queryString from 'query-string';
import Film from "./Film";

function MainPage(props) {
    const [film, setFilm] = useState([]);
    const [favorites, setFavorites] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage] = useState(99);
    const [isLoading, setLoading] = useState(false);
    const slug = props?.match?.params?.slug || queryString.parse(props?.location?.search);
    useEffect(() => {
        setLoading(true)
        document.title = "Главная страница";
        props.getFilms(slug).then(response => {
            setFilm(response.data)
        })
        setLoading(false)
    }, [isLoading])
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
    const lastItemIndex = currentPage * itemsPerPage
    const currentItem = film.slice(0, lastItemIndex)
    const paginate = pageNumber => setCurrentPage(pageNumber);
    useEffect(() => {
        document.addEventListener('scroll', scrollHandler)
        return function () {
            document.removeEventListener('scroll', scrollHandler)
        }
    }, [currentPage])
    const scrollHandler = (event) => {
        if (event.target.documentElement.scrollHeight -
            (event.target.documentElement.scrollTop + window.innerHeight) < 100) {
            let number = currentPage + 1;
            paginate(number)
        }
    }
    return (
        <div className="main-page font-style">
            {currentItem.length > 0 ?
                <div className="films">
                    {currentItem.map((f) => {
                            return <Film key={film.id} film={f} updateFavorites={updateFavorites} favorites={favorites}/>
                        }
                    )}
                </div> :
                <div className="films">
                    {isLoading ?
                        <div className="films-not__found">Загрузка..</div> :
                        <div className="films-not__found">К сожалению, пока ничего нет :(</div>
                    }
                </div>}
        </div>
    )
}

export default MainPage;