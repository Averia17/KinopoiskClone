import React, { Component } from "react"
import axios from "axios"
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import FilmDetail from "./components/film/FilmDetail";
import MainPage from "./components/main/MainPage";
import NavBar from "./components/navbar/NavBar";
import PersonPage from "./components/person/PersonPage";
import StaffPage from "./components/staff/StaffPage";
import GenreFilms from "./components/genres/GenreFilms";

if (window.location.origin === "http://localhost:3000") {
    axios.defaults.baseURL = "http://127.0.0.1:8000/api/films/";
}

class App extends Component {
    render() {
        return (
            <Router>
                <NavBar/>
                <Switch>
                    <Route path="/films/:id/" exact component={FilmDetail}/>
                    <Route path="/films/" exact component={MainPage}/>
                    <Route path="/films/:id/staff" exact component={StaffPage}/>
                    <Route path="/staff/:id/" exact component={PersonPage}/>
                    <Route path="/genres/:slug/" exact component={GenreFilms}/>
                    <Route component={MainPage}/>
                </Switch>
            </Router>
        );
    }
}

export default App;