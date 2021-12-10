import React, { Component } from 'react';
import '../../App.css';
import "../../../public/logo.svg";
import Filter from "../Filter/Filter"
import { Link } from 'react-router-dom'
import filter from '../../assets/filter.png'

function NavBar() {
    return (
        <nav className="navbar font-style">
            <ul className="navbar-items">
                <li>
                    <Link to={{ pathname: `/films/`}}>
                        <div className="logo">
                            <img src="/assets/logo.svg"></img>
                        </div>
                    </Link>
                </li>
                <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                <li><Link className="link" to={{ pathname: `/serials/`}}>Сериалы</Link></li>
                <li><Link className="link" to={{ pathname: `/films/`}}>Жанры</Link></li>
                <li><Link className="link" to={{ pathname: `/films/`}}>Страны</Link></li>
                <div>
                    <form>
                        <div className="search-form">
                            <input className="search-txt" type="search" name="" placeholder="Нажмите для поиска"/>
                            <a className="search-btn" href="#"></a>
                            <div>
                                <Link to={{ pathname: `/filter/`}}>
                                    <img id="filter-icon" src={filter}/>
                                </Link>
                            </div>
                        </div>
                    </form>
                </div>
                <li className="search-box"></li>
            </ul>
        </nav>
    )
}

export default NavBar;
