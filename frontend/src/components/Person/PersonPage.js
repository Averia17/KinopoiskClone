import React, { useEffect, useState} from 'react';
import axios from 'axios';
import './PersonPageStyles.css';
import moment from "moment";

function PersonPage({ match }) {
    const[person, setPerson] = useState( []);
    const id = match.params.id;
    const dateFormat = "DD MMMM YYYY";
    const dateOfBirth = moment(person?.birthday).lang("ru").format(dateFormat);
    const dateOfDeath = moment(person?.death).lang("ru").format(dateFormat);

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://localhost:8080/api/staff/${id}/`,
        }).then(response => {
            setPerson(response.data)
        })
    }, [id])

    return(
        <div className="person-page-block">
            <div className="person-poster-details">
                <img alt="Person" src={person?.image}/>
            </div>
            <div className="person-page-info">
                <div className="person-page-header">
                    <p>{person?.nameRu}</p>
                </div>
                <div className="person-page-info__career">
                    <p>Карьера: {person?.profession}</p>
                </div>
                <div className="person-page-info__birthday">
                    <p>Дата рождения:</p>
                    <p id="date">{moment(dateOfBirth, dateFormat, true).isValid()  ? dateOfBirth : "-"}</p>
                    <p id="age">{person?.age ? person.age : null} лет</p>
                </div>
                    {person?.death ?
                        <div className="person-page-info__death">
                            <p>Дата смерти:</p>
                            <p id="death">{moment(dateOfDeath, dateFormat, true).isValid()  ? dateOfDeath : "-"}</p>
                        </div> :
                        null}
                <div className="person-page-info__growth">
                    <p>Рост:</p>
                    <p id="growth">{person?.growth ? person?.growth : "-"}</p>
                </div>
            </div>

        </div>
    )
}

export default PersonPage;