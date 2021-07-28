import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import { Link } from 'react-router-dom'

function StaffPage({ match }) {
    const[film, setFilm] = useState( []);
    const id = match.params.id;

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://127.0.0.1:8000/api/films/${id}/`,
        }).then(response => {
            setFilm(response.data)
        })
    }, [id])

    const staff = film.staff
    return(

    )
}

export default StaffPage;