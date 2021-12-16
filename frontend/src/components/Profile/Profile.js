import React, {useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import Tokens from "../../services/auth-header";
import Film from "../Films/Film";


function Profile(props) {
    const [user, setUser] = useState([]);
    const id = props?.match?.params?.id;
    const [favorites, setFavorites] = useState([]);
    const [userFavorites, setUserFavorites] = useState([]);

    useEffect(() => {
        const url = `http://localhost:8080/api/users/${id}`;
        axios({
            method: 'GET',
            url: url,
            headers: {
                'Content-type': 'application/json',
            },
        }).then(response => setUser(response.data))
    }, [id])
    useEffect(() => {
        axios({
            method: "GET",
            url: `http://localhost:8080/api/favorites/${id}`,
            headers: {
                'Content-type': 'application/json',
            },
        }).then(response => {
            setUserFavorites(response.data)
        }).catch(error => {
            setUserFavorites([])
        })
    }, [id])
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
    const updateFavorites = (favorites) => {
        setFavorites(favorites)
        if(Tokens.getCurrentUserTokens().id.toString() === id) {
            setUserFavorites(favorites)
        }
    }

    return (
        <div className="user-profile">
            <div className="user-profile-title">{user?.email} profile</div>
            <div className="user-profile-title">User's favorite movies </div>
            <div className="films">
                {userFavorites?.map((film) => {
                    return (
                        <Film key={film.id} film={film} updateFavorites={updateFavorites} favorites={favorites}/>
                    )
                })
                }
            </div>

        </div>
    );
}


export default Profile;