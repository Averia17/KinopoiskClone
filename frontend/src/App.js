import React, { Component } from "react"
import { withRouter } from "react-router";
import axios from "axios"
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import FilmDetail from "./components/film/FilmDetail";
import MainPage from "./components/main/MainPage";
import NavBar from "./components/navbar/NavBar";
import PersonPage from "./components/person/PersonPage";
import StaffPage from "./components/staff/StaffPage";
import GenreFilms from "./components/genres/GenreFilms";
import Login from "./components/LoginRegister/Login";
import Register from "./components/LoginRegister/Register";


class App extends Component {

    getFilms(isSerials) {
        let url = 'http://localhost:8080/api/films/';
        if(isSerials) url = 'http://localhost:8080/api/serials/'
        return axios({
            method: "GET",
            url: url,
        })
    }
    getByGenre(slug) {
        return axios({
            method: "GET",
            url: `http://localhost:8080/api/genres/${slug}/`,
        })
    }
    getByCountry(slug) {
        return axios({
            method: "GET",
            url: `http://localhost:8080/api/countries/${slug}/`,
        })
    }
    render() {
        return (
            <>
                <NavBar/>
                <Switch>
                    <Route path="/films/:id/" exact component={FilmDetail}/>
                    <Route path="/serials/:id/" exact component={FilmDetail}/>
                    <Route path="/films/" exact component={() => <MainPage getFilms = {(isSerials) => this.getFilms(false)}/>}/>
                    <Route path="/serials/" exact component={() => <MainPage getFilms = {(isSerials) => this.getFilms(true)}/>}/>
                    <Route path="/films/:id/staff" exact component={StaffPage}/>
                    <Route path="/staff/:id/" exact component={PersonPage}/>
                    <Route path="/genres/:slug/" exact component={(props) => <MainPage {...props} getFilms = {(slug) => this.getByGenre(slug)}/>}/>
                    <Route path="/countries/:slug/" exact component={(props) => <MainPage {...props} getFilms = {(slug) => this.getByCountry(slug)}/>}/>
                    <Route path="/login/" exact component={Login}/>
                    <Route path="/register/" exact component={Register}/>
                    <Route component={() => <MainPage getFilms = {(isSerials) => this.getFilms(false)}/>}/>
                </Switch>
            </>
        );
    }
}

export default withRouter(App);