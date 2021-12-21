import React, {useEffect, useState} from 'react';
import axios from 'axios';
import './StaffPage.css';
import {Link} from 'react-router-dom';

function StaffPage({match}) {
    const [film, setFilm] = useState([]);
    const id = match.params.id;
    console.log(film)

    useEffect(() => {
        let url_addition = 'films';
        if(film?.type === 'TV_SHOW')
            url_addition = 'serials';
        axios({
            method: "GET",
            url: `http://localhost:8080/api/${url_addition}/${id}/`,
        }).then(response => {
            setFilm(response.data)
        })
    }, [id])

    const grouped = film.staff?.reduce((acc, item) => {
        if (acc[item.professionText]) {
            acc[item.professionText].push(item);
        } else {
            acc[item.professionText] = [item];
        }
        return acc;
    }, {})
    return (
        <div className="film-staff font-style">
            <div>
                <h1>Персоны и команда / {film.name}</h1>
            </div>
            <div className="film-staff-wrapper">
                {(grouped && Object.keys(grouped)) ? Object.keys(grouped).map(profession => {
                    return <div key={profession.id} className="staff-subdivision">
                        <h1 className="staff-group-title" key={profession.id}>{profession}</h1>
                        {grouped[profession].map(item => {
                            return <div>
                                <div className="staff-item-wrapper">
                                    <div className="staff-image">
                                        <img className="" src={item.image}/>
                                    </div>
                                    <div className="staff-item-name">
                                        <Link to={{pathname: `/staff/${item.id}/`}} key={item.id}>{item.nameRu}</Link>
                                    </div>
                                </div>
                            </div>
                        })}
                    </div>
                }) : []}
            </div>
        </div>
    )
}

export default StaffPage;