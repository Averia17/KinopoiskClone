import React, {useEffect, useRef, useState} from 'react';
import axios from 'axios';
import {stringify} from "query-string";
import {rating, year} from "../../utils";
import {useFormik} from 'formik';

function FilterForm(props) {
    const [country, setCountry] = useState([]);
    const [genre, setGenre] = useState([]);

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
    const formik = useFormik({
        validateOnChange: false,
        validateOnBlur: false,
        initialValues: {
            'min_rating': '',
            'max_rating': '',
            'min_year': '',
            'max_year': '',
            'countries__title': '',
            'genres__title': ''
        },
        onSubmit: values => {
            values = Object.entries(values).reduce((a, [k, v]) => (v === '' ? a : (a[k] = v, a)), {})
            let qs = stringify(values)
            props.history.push(`/movies/?${qs}`)
        },
        validate: values => {
            let errors = {};
            if (values.min_rating > 10 || values.min_rating < 0) {
                errors.min_rating = 'Рейтинг должен быть от 0 до 10'
            }
            if (values.max_rating > 10 || values.max_rating < 0) {
                errors.max_rating = 'Рейтинг должен быть от 0 до 10'
            }
            if (values.min_year > 2030 || values.min_year < 0) {
                errors.min_year = 'Год должен быть от 0 до 2030'
            }
            if (values.max_year > 2030 || values.max_year < 0) {
                errors.max_year = 'Год должен быть от 0 до 2030'
            }
            if (!Number.isInteger(values.min_year) && values.min_year !== '') {
                errors.min_year = 'Введите целое значение'
            }
            if (!Number.isInteger(values.max_year) && values.max_year !== '') {
                errors.max_year = 'Введите целое значение'
            }
            return errors
        }
    })

    return (
        <div className="filter-form">
            <h1>Искать фильм</h1>
            <div className="filter-form-wrapper">
                <form onSubmit={formik.handleSubmit}>

                    <div className="filter-form-fields">
                        <div className="filter-form-group-inputs">
                            <p>Страна</p>
                            <select name="countries__title" onChange={formik.handleChange}>
                                <option selected="selected"/>
                                {country.map((c) =>
                                    <option value={c.title}>{c.title}</option>)}
                            </select>
                        </div>
                        <div className="filter-form-group-inputs">
                            <p>Жанр</p>
                            <select name="genres__title" onChange={formik.handleChange}>
                                <option selected="selected"/>
                                {genre.map((g) =>
                                    <option value={g.title}>{g.title}</option>)}
                            </select>
                        </div>
                        <div className="filter-form-group-inputs">
                            <div className="filter-form-field-wrapper">
                                <div className="filter-form-field">
                                    <label className="filter-field-label">Минимальный рейтинг</label>
                                    <input type="number" name="min_rating" id="min_rating" className="filter-input"
                                           onChange={formik.handleChange}
                                           value={formik.values.min_rating}
                                    />
                                </div>
                                {formik.errors.min_rating && <div className="error">{formik.errors.min_rating}</div>}
                            </div>
                            <div className="filter-form-field-wrapper">
                                <div className="filter-form-field">
                                    <label className="filter-field-label">Максимальный рейтинг</label>
                                    <input type="number" name="max_rating" id="max_rating" className="filter-input"
                                           onChange={formik.handleChange}
                                           value={formik.values.max_rating}
                                    />
                                </div>
                                {formik.errors.max_rating && <div className="error">{formik.errors.max_rating}</div>}
                            </div>
                        </div>
                        <div className="filter-form-group-inputs">
                            <div className="filter-form-field-wrapper">
                                <div className="filter-form-field">
                                    <label className="filter-field-label">Минимальный год</label>
                                    <input type="number" name="min_year" className="filter-input"
                                           onChange={formik.handleChange}
                                           value={formik.values.min_year}
                                    />
                                </div>
                                {formik.errors.min_year && <div className="error">{formik.errors.min_year}</div>}
                            </div>
                            <div className="filter-form-field-wrapper">
                                <div className="filter-form-field">
                                    <label className="filter-field-label">Максимальный год</label>
                                    <input type="number" name="max_year" className="filter-input"
                                           onChange={formik.handleChange}
                                           value={formik.values.max_year}
                                    />
                                </div>
                                {formik.errors.max_year && <div className="error">{formik.errors.max_year}</div>}
                            </div>
                        </div>
                        <div className="submit-button">
                            <button type="submit">
                                Submit
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default FilterForm;

