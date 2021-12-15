import React, {useEffect, useRef, useState} from 'react';
import axios from 'axios';
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import {stringify} from "query-string";
import {rating, year} from "../../utils";


function FilterForm(props) {
    const [country, setCountry] = useState([]);
    const [genre, setGenre] = useState([]);
    const [min_rating, setMinRating] = useState([]);
    const [max_rating, setMaxRating] = useState([]);
    const [min_year, setMinYear] = useState([]);
    const [max_year, setMaxYear] = useState([]);
    const [countries__title, setCountryTitle] = useState([]);
    const [genres__title, setGenreTitle] = useState([]);
    const formRef = useRef();
    useEffect(() => {
        axios({
            method: "GET",
            url: `http://localhost:8080/api/countries/`,
        }).then(response => {
            setCountry(response.data)
        })
    }, [])
    useEffect(() => {
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
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = {
            'min_rating': min_rating,
            'max_rating': max_rating,
            'min_year': min_year,
            'max_year': max_year,
            'countries__title': countries__title,
            'genres__title': genres__title
        };
        let qs = stringify(data)
        props.history.push(`/movies/?${qs}`)
    }
    return (
        <div className="filter-form">
            <h1>Искать фильм</h1>
            <div className="filter-form-wrapper">
                <Form onSubmit={handleSubmit} ref={formRef}>
                    <div className="filter-form-fields">
                        <div className="filter-form-group-inputs">
                            <p>Страна</p>
                            <select name="countries__title" onChange={countryHandleChange}>
                                <option selected="selected"/>
                                {country.map((c) =>
                                    <option value={c.title}>{c.title}</option>)}
                            </select>
                        </div>
                        <div className="filter-form-group-inputs">
                            <p>Жанр</p>
                            <select name="genres__title" onChange={genreHandleChange}>
                                <option selected="selected"/>
                                {genre.map((g) =>
                                    <option value={g.title}>{g.title}</option>)}
                            </select>
                        </div>
                        <div className="filter-form-group-inputs">
                            <label className="filter-field-label">Минимальный рейтинг</label>
                            <Input type="number" name="min_rating" className="filter-input"
                                   onChange={minRatingHandleChange}
                                   value={min_rating}
                                   validations={[rating]}
                            />
                            <label className="filter-field-label">Максимальный рейтинг</label>
                            <Input type="number" name="max_rating"  className="filter-input"
                                   onChange={maxRatingHandleChange}
                                   value={max_rating}
                                   validations={[rating]}
                            />
                        </div>
                        <div className="filter-form-group-inputs">
                            <label className="filter-field-label">Минимальный год</label>
                            <Input type="number" name="min_year"  className="filter-input"
                                   onChange={minYearHandleChange}
                                   value={min_year}
                                   validations={[year]}
                            />
                            <label className="filter-field-label">Максимальный год</label>
                            <Input type="number" name="max_year" className="filter-input"
                                   onChange={maxYearHandleChange}
                                   value={max_year}
                                   validations={[year]}
                            />
                        </div>
                        <div className="submit-button">
                            <button  type="submit">
                                Submit
                            </button>
                        </div>
                    </div>
                </Form>
            </div>
        </div>
    )
}

export default FilterForm;

