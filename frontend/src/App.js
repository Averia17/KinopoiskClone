import React, {Component} from "react"
import {withRouter} from "react-router";
import axios from "axios"
import './App.css';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import FilmDetail from "./components/Film/FilmDetail";
import MainPage from "./components/Films/MainPage";
import NavBar from "./components/Navbar/NavBar";
import PersonPage from "./components/Person/PersonPage";
import StaffPage from "./components/Staff/StaffPage";
import Login from "./components/LoginRegister/Login";
import Register from "./components/LoginRegister/Register";
import FilterForm from "./components/Filter/Filter";
import Profile from "./components/Profile/Profile";


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
            method: "GET",
            url: `http://localhost:8080/api/countries/${slug}/`,
        })
    }

    searchMovies(searchText) {
        console.log(searchText)

        return axios({
            method: "GET",
            headers: {
                'Content-type': 'application/json',
            },
            params: {
                'name': searchText
            },
            url: `http://localhost:8080/api/movies/`,
        })
    };
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
                    <Route path="/films/:id/" exact component={FilmDetail}/>
                    <Route path="/serials/:id/" exact component={FilmDetail}/>
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
                    <Route component={() => <MainPage getFilms = {(isSerials) => this.getFilms(false)}/>}/>

                    <Route component={() => <MainPage getFilms={(isSerials) => this.getFilms(false)}/>}/>
                </Switch>
            </>
        );
           /*<Route path="/filters/" exact*/
                     /*       component={(props) => <MainPage {...props} getFilms={(slug) => this.filterMovies(slug)}/>}/>*/
    }
}

export default withRouter(App);