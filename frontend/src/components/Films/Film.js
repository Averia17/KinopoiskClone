import StarIcon from "@mui/icons-material/Star";
import {Link} from "react-router-dom";
import React from "react";
import '../../App.css';
import {handleMoveToFavorite} from "../../services/favorite.service";
import withRouter from "react-router-dom/es/withRouter";

function Film(props) {
    const film = props.film;
    const updateFavorites = props.updateFavorites;
    const favorites = props.favorites;
    const moveToFavorites = (key, isFavorite) => {
        handleMoveToFavorite(key, isFavorite).then((response) => {
            updateFavorites(response.data)
        }).catch(error => {
            if (error.request?.status === 401) {
                props.history.push('/login/')
            } else
                console.log(error)
        })
    }
    const isFavorite = favorites.some((item) => item.id === film.id);
    let url = 'films'
    if (film.type === 'TV_SHOW')
        url = 'serials'
    return (
        <div className="films-item" >
            <button className="favorite-button" onClick={() => moveToFavorites(film.id, isFavorite)} style={{background: 'none', border: 'none'}}>
                <StarIcon fontSize={"large"} style={{color: isFavorite ? '#5CE9E2' : '#ECECEC'}}/>
            </button>
            <Link to={{pathname: `/${url}/${film.id}/`}}>
                <div className="poster-main">
                    <img src={film.image} className="main-img" alt=""/>
                </div>
                <div className="film-description">
                    <div id="film-title">
                        <p id="genre">{film.genres__title}</p>
                        <p id="year">{film.year}</p>
                    </div>
                    <div id="name">
                        <p>{film.name}</p>
                    </div>
                </div>
            </Link>
        </div>
    )
}

export default withRouter(Film);