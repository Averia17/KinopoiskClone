import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';

function PersonPage({ match }) {
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
    console.log(film.staff)
    var actors = film.staff?.filter(function(f) {
        return f.professionKey === "ACTOR";
    });
    var writers = film.staff?.filter(function(f) {
        return f.professionKey === "WRITER";
    });
    var operators = film.staff?.filter(function(f) {
        return f.professionKey === "OPERATOR";
    });
    var editors = film.staff?.filter(function(f) {
        return f.professionKey === "EDITOR";
    });
    var composers = film.staff?.filter(function(f) {
        return f.professionKey === "COMPOSER";
    });

    var translators = film.staff?.filter(function(f) {
        return f.professionKey === "TRANSLATOR";
    });
    var directors = film.staff?.filter(function(f) {
        return f.professionKey === "DIRECTOR";
    });
    var designers = film.staff?.filter(function(f) {
        return f.professionKey === "DESIGN";
    });
    var voice_directors = film.staff?.filter(function(f) {
        return f.professionKey === "VOICE_DIRECTOR";
    });
    if(film.countries?.includes("СССР") === true) {
        var producers = film.staff?.filter(function(f) {
            return f.professionKey === "PRODUCER_USSR";
        });
    }
    else {
        var producers = film.staff?.filter(function(f) {
            return f.professionKey === "PRODUCER";
        });
    }

    return(
        <div>
            <div className="film-staff">
                <div>
                    <p>{film.name}</p>
                </div>
                <div className="film-directors">
                    <p>Режиссёры</p>
                    {directors?.map((d) => {
                        return (
                            <div key={d.id}>
                                <p>{d.nameRu}</p>
                            </div>
                        )
                    })}
                </div>
                <div className="film-staff">
                    <p>Актёры</p>
                    {actors?.map((a) => {
                        return (
                            <div key={a.id}>
                                <p>{a.nameRu}</p>
                            </div>
                        )
                    })}
                </div>
                <div className="film-producers">
                    <p>Продюсеры</p>
                    {producers?.map((p) => {
                        return (
                            <div key={p.id}>
                                <p>{p.nameRu}</p>
                            </div>
                        )
                    })}
                </div>
                <div className="film-producers">
                    <p>Продюсеры</p>
                    {translators?.map((d) => {
                        return (
                            <div key={d.id}>
                                <p>{d.nameRu}</p>
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}

export default PersonPage;