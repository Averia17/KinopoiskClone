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
                <h1>Hhhhhhh</h1>
                <div>
                      {film.map((f) => {
                            return(
                                <ul>
                                      <li>{f.nameRu}</li>
                                </ul>
                            )
                      })}

                </div>
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
