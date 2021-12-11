import React, {useEffect, useState} from 'react';
import axios from 'axios';
import moment from 'moment';
import 'moment/locale/ru'
import '../../App.css';
import {Link, useParams} from 'react-router-dom'
import Tokens from "../../services/auth-header";
import Film from "../Films/Film";


function Profile(props) {
    const [user, setUser] = useState([]);
    const id = props?.match?.params?.id;
    const [favorites, setFavorites] = useState([]);

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
        const accessToken = Tokens.AccessTokenHeader();
        let headers = {
            'Content-type': 'application/json',
        }
        if(accessToken) headers['Authorization'] = accessToken
        axios({
            method: "GET",
            url: `http://localhost:8080/api/favorites/`,
            headers: headers,
            data: {
                id: id
            }
        }).then(response => {
            setFavorites(response.data)
        }).catch(error => {
            setFavorites([])
        })
    }, [])
    const updateFavorites = (favorites) => {
        setFavorites(favorites)
    }
    return (
        <div className="user-profile">
            <div className="user-profile-title">{user?.email} profile</div>
            <div className="films">
                {user?.saved_films?.map((film) => {
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