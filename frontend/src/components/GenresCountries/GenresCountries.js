import React, { useEffect, useState} from 'react';
import axios from 'axios';
import { Link, useHistory } from 'react-router-dom';
import './GenresCountriesStyles.css';
import genreImage from '../../assets/genre.png'
import countryImage from '../../assets/country.png'

function GenresCountries(props) {
    const [item, setItem] = useState([]);
    let history = useHistory();
    let image = genreImage;
    let title = 'Жанры';
    let type = 'genres'
    if (history.location.pathname === '/countries/') {
        image = countryImage;
        title = 'Страны';
        type = 'countries'
    }
    useEffect(() => {
        props.getFilms().then(response => {
            setItem(response.data)
        })
    }, [])

    return (
        <div className='items-main-block'>
            <p id='items-header'>{title}</p>
            <ul className="items-list">
                {item.map((item) => {
                    return (
                        <div key={item.id} className='item-block'>
                            <div className='item-image'>
                                <img src={image}/>
                            </div>
                            <li className='item'>
                                <Link key={item.id} to={{pathname: `/${type}/${item.slug}/`}}>{item.title}</Link>
                            </li>
                        </div>
                    )
                })}
            </ul>
        </div>
    )
}

export default GenresCountries;