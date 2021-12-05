import React, { useEffect, useState} from 'react';
import axios from 'axios';
import '../../App.css';
import { Link } from 'react-router-dom'

function PersonPage({ match }) {
    const[person, setPerson] = useState( []);
    const id = match.params.id;

    useEffect( () => {
        axios({
            method: "GET",
            url: `http://localhost:8080/api/staff/${id}/`,
        }).then(response => {
            setPerson(response.data)
        })
    }, [id])

    return(
        <div>
            <p>{person.nameRu}</p>
            <div className="poster-details">
                <img src={person.image}/>
            </div>
        </div>
    )
}

export default PersonPage;