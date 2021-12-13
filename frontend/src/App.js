import React, {Component} from "react"
import {withRouter} from "react-router";
import axios from "axios"
import './App.css';
import {Switch, Route} from 'react-router-dom';
import FilmDetail from "./components/Film/FilmDetail";
import MainPage from "./components/Films/MainPage";
import NavBar from "./components/Navbar/NavBar";
import PersonPage from "./components/Person/PersonPage";
import StaffPage from "./components/Staff/StaffPage";
import Login from "./components/LoginRegister/Login";
import Register from "./components/LoginRegister/Register";
import FilterForm from "./components/Filter/Filter";
import Profile from "./components/Profile/Profile";
import GenresCountries from "./components/GenresCountries/GenresCountries";


class App extends Component {
    state = {
        favorites: []
    }

    getFilms(isSerials) {
        let url = 'http://localhost:8080/api/films/';
        if (isSerials) url = 'http://localhost:8080/api/serials/'
        return axios({
            method: "GET",
            url: url,
        })
    }

    getMovie(id) {
        return axios({
            method: "GET",
            url: `http://localhost:8080/api/movies/${id}`,
        })
    }

    getAllMovies() {
        return axios({
            method: "GET",
            url: `http://localhost:8080/api/movies/`,
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
            method: 'GET',
            url: `http://localhost:8080/api/countries/${slug}/`,
        })
    }

    searchMovies(params) {
        if (params && params["search"] !== undefined) {
            params.name = params.search
            delete params.search
        }
        return axios({
            method: "GET",
            headers: {
                'Content-type': 'application/json',
            },
            params: params,
            url: `http://localhost:8080/api/movies/`,
        })
    };

    getTypesByGenresOrCountries(isCountries) {
        let url = `http://localhost:8080/api/genres/`;
        if (isCountries) url = `http://localhost:8080/api/countries/`;
        return axios({
            method: 'GET',
            url: url,
        })
    }


    filterMovies(params) {
        console.log(params)

        return axios({
            method: "GET",
            headers: {
                'Content-type': 'application/json',
            },
            url: `http://localhost:8080/api/movies/?${params}`,
        })
    };


    render() {
        return (
            <>
                <NavBar {...this.props}/>
                <Switch>
                    <Route path="/movies/:id/" exact
                           component={(props) => <FilmDetail {...props} getFilms={(id) => this.getMovie(id)}/>}/>
                    <Route path="/films/:id/" exact
                           component={(props) => <FilmDetail {...props} getFilms={(id) => this.getMovie(id)}/>}/>
                    <Route path="/serials/:id/" exact
                           component={(props) => <FilmDetail {...props} getFilms={(id) => this.getMovie(id)}/>}/>
                    <Route path="/films/" exact
                           component={() => <MainPage getFilms={(isSerials) => this.getFilms(false)}/>}/>
                    <Route path="/serials/" exact
                           component={() => <MainPage getFilms={(isSerials) => this.getFilms(true)}/>}/>
                    <Route path="/films/:id/staff" exact component={StaffPage}/>
                    <Route path="/staff/:id/" exact component={PersonPage}/>
                    <Route path="/movies/" exact
                           component={(props) => <MainPage {...props} getFilms={(slug) => this.searchMovies(slug)}/>}/>
                    <Route path="/genres/:slug/" exact
                           component={(props) => <MainPage {...props} getFilms={(slug) => this.getByGenre(slug)}/>}/>
                    <Route path="/countries/:slug/" exact
                           component={(props) => <MainPage {...props} getFilms={(slug) => this.getByCountry(slug)}/>}/>
                    <Route path="/users/:id/" exact
                           component={(props) => <Profile {...props}/>}/>
                    <Route path="/login/" exact component={Login}/>
                    <Route path="/register/" exact component={Register}/>
                    <Route path="/filter/" exact component={(props) => <FilterForm {...props}/>}/>
                    <Route path="/genres/" exact component={() => <GenresCountries getFilms={(isCountries) =>
                        this.getTypesByGenresOrCountries(false)}/>}/>
                    <Route path="/countries/" exact component={() => <GenresCountries getFilms={(isCountries) =>
                        this.getTypesByGenresOrCountries(true)}/>}/>
                    <Route component={() => <MainPage getFilms={(isSerials) => this.getFilms(false)}/>}/>
                </Switch>
            </>
        );
    }
}

export default withRouter(App);