import React, { Component } from "react"
import axios from "axios"
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import FilmDetail from "./components/film/FilmDetail";
import MainPage from "./components/main/MainPage";

if (window.location.origin === "http://localhost:3000") {
    axios.defaults.baseURL = "http://127.0.0.1:8000/api/films/";
}

class App extends Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route path="/films/:id/" exact component={FilmDetail}/>
                    <Route path="/films/" exact component={MainPage}/>
                </Switch>
            </Router>
        );
    }
}

export default App;
