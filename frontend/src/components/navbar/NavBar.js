import React, { Component } from 'react';
import '../../App.css';
import { Link } from 'react-router-dom'

class NavBar extends Component {
    render() {
        return (
            <div className="navbar font-style">
                <div>
                    <img src="../../assets/logo.svg"/>
                </div>
                <ul className="navbar-items">
                    <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                    <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                    <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                    <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                    <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                    <li><Link className="link" to={{ pathname: `/films/`}}>Фильмы</Link></li>
                </ul>
            </div>
        )
    }
}

export default NavBar;
