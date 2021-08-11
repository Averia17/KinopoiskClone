import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import { Link } from 'react-router-dom';

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

    const grouped = film.staff?.reduce((acc, item) => {
        if(acc[item.professionText]) {
            acc[item.professionText].push(item);
        }
        else {
            acc[item.professionText] = [item];
        }
        return acc;
    }, {})

    return(
        <div className="film-staff font-style">
            <div>
                <h1>Персоны и команда / {film.name}</h1>
            </div>
            <div>
                {(grouped && Object.keys(grouped)) ? Object.keys(grouped).map(profession => {
                    return <div key={profession.id} className="staff-subdivision">
                        <h3 key={profession.id}>{profession}</h3>
                        {grouped[profession].map(item => {
                            return <div>
                                <Link to={{pathname: `/staff/${item.id}/`}} key={item.id}>{item.nameRu}</Link>
                            </div>
                        })}
                    </div>
                }) : []}
            </div>
        </div>
    )
}

export default StaffPage;