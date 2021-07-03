import React, { useState, useEffect } from "react"
import axios from "axios"
import './App.css';

function App() {
      const [film, setFilm] = useState( [])

      useEffect( () => {
            axios({
                  method: "GET",
                  url: 'http://127.0.0.1:8000/api/top-films/',

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
                                      <img src={f.posterUrl} className="img"></img>
                                      <h1>{f.nameRu}</h1>
                                      <h2 className="filmInfo">{f.year}</h2>
                                      <h2 className="filmInfo">{f.rating}</h2>
                                </div>
                            )
                      })}

                </ul>
          </div>
      );
}
/*class App extends React.Component {

      render() {
            this.state = []
            fetch('http://127.0.0.1:8000/api/top-films/')
                .then(response => response.json())
      return (
          <div>
                {this.state.map((info) => {
                      return (
                          <div>
                                <h1>{info.nameRu}</h1>
                                <h2>{info.age}</h2>
                          </div>
                      );
                })}
          </div>
      );
      }
}*/

export default App;
