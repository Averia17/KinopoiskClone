import React, { useState, useEffect } from "react"
import axios from "axios"
import './App.css';

function App() {
      const [film, setFilm] = useState( [])

      useEffect( () => {
            axios({
                  method: "GET",
                  url: 'http://127.0.0.1:8000/api/films/',

            }).then(response => {
                  setFilm(response.data)
            })
      }, [])
      return (
          <div>
                <ul className="films">
                      {film.map((f) => {
                            return(
                                <div className="item">
                                      <img src={f.image} className="img"></img>
                                      <h1>{f.name}</h1>
                                      <h2 className="filmInfo">{f.year}</h2>
                                      <h2 className="filmInfo">{f.rating}</h2>
                                </div>
                            )
                      })}

                </ul>
          </div>
      );
}


export default App;
