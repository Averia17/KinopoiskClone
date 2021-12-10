import React, {useEffect, useState} from 'react';
import { useLocation } from "react-router-dom";
import axios from 'axios';
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";

/*interface Values {
    min_rating?: string;
    max_rating?: string;
    min_year?: string;
    max_year?: string;
    countries__title?: string;
    genres__title?: string;
};*/

/*
const getQueryStringFromObject = (filter: Filter) => {
    return new URLSearchParams(filter).toString();
};
*/

function FilterForm() {
    const [country, setCountry] = useState( []);
    const [genre, setGenre] = useState([]);
    const [min_rating, setMinRating] = useState([]);
    const [max_rating, setMaxRating] = useState([]);
    const [min_year, setMinYear] = useState([]);
    const [max_year, setMaxYear] = useState([]);
    const [countries__title, setCountryTitle] = useState([]);
    const [genres__title, setGenreTitle] = useState([]);
    const query = new URLSearchParams(useLocation().search)
    const removeEmptyParams = () => {
        return query.toString().replace(/[^=&]+=(?:&|$)/g, "");
    }
    console.log('LINK ' + removeEmptyParams())
    useEffect( () => {
        axios({
            method: "GET",
            url: `http://localhost:8080/api/countries/`,
        }).then(response => {
            setCountry(response.data)
        })
    }, [])
    useEffect( () => {
        axios({
            method: "GET",
            url: `http://localhost:8080/api/genres/`,
        }).then(response => {
            setGenre(response.data)
        })
    }, [])
    const minRatingHandleChange = (event) => {
        setMinRating(event.target.value);
    }
    const maxRatingHandleChange = (event) => {
        setMaxRating(event.target.value);
    }
    const minYearHandleChange = (event) => {
        setMinYear(event.target.value);
    }
    const maxYearHandleChange = (event) => {
        setMaxYear(event.target.value);
    }
    const countryHandleChange = (event) => {
        setCountryTitle(event.target.value);
    }
    const genreHandleChange = (event) => {
        setGenreTitle(event.target.value);
    }
    return (
        <div className="filter-form">
            <h1>Искать фильм</h1>
                <Form>
                    <div className="filter-form-fields">
                        <div className="filter-form-group-inputs">
                            <p>Страна</p>
                            <select name="countries__title">
                                {country.map((c) =>
                                <option value={c.title} onChange={countryHandleChange}>{c.title}</option>)}
                            </select>
                        </div>
                        <div className="filter-form-group-inputs">
                            <p>Жанр</p>
                            <select name="genres__title">
                                {genre.map((g) =>
                                <option value={g.title} onChange={genreHandleChange}>{g.title}</option>)}
                            </select>
                        </div>
                        <div className="filter-form-group-inputs">
                            <label>Минимальный рейтинг</label>
                            <Input type="text" name="min_rating"
                                   onChange={minRatingHandleChange}
                                   value={min_rating}/>
                            <p>-</p>
                            <label>Максимальный рейтинг</label>
                            <Input type="text" name="max_rating"
                                   onChange={maxRatingHandleChange}
                                   value={max_rating}/>
                        </div>
                        <div className="filter-form-group-inputs">
                            <label>Минимальный год</label>
                            <Input type="text" name="min_year"
                                   onChange={minYearHandleChange}
                                   value={min_year}/>
                            <p>- </p>
                            <label>Максимальный год</label>
                            <Input type="text" name="max_year"
                                   onChange={maxYearHandleChange}
                                   value={max_year}/>
                        </div>
                        <button className="submit-button" type="submit">
                            Submit
                        </button>
                    </div>
                </Form>
        </div>
)}
export default FilterForm;

