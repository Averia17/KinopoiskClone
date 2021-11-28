import React, { Component } from 'react';
import '../../App.css';
import "../../../public/logo.svg";
import { Link } from 'react-router-dom'

class NavBar extends Component {
    render() {
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
                    <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                    <div>
                        <input className="search-txt" type="search" name="" placeholder="Нажмите для поиска"/>
                        <a className="search-btn" href="#"></a>
                    </div>
                    <li className="search-box"></li>
                </ul>
            </nav>
        )
    }
}

export default NavBar;
