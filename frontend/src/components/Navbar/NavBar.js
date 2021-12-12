import React from 'react';
import '../../App.css';
import "../../../public/logo.svg";
import { Link } from 'react-router-dom'
import Search from "./Search";
import Tokens from "../../services/auth-header";
import AuthService from "../../services/auth.service";

function NavBar(props) {
    const handleLogout = e => {
        AuthService.logout(Tokens.RefreshTokenHeader()).then(
            () => window.location.reload()
        )
    }
    const tokens = Tokens.getCurrentUserTokens();

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
                <li><Link className="link" to={{ pathname: `/genres/`}}>Жанры</Link></li>
                <li><Link className="link" to={{ pathname: `/countries/`}}>Страны</Link></li>
                { tokens?.access ?
                    <ul className="wrapper-logout-favorites">
                        <li>
                        <Link className="link" to={{pathname: `/users/${tokens.id}`}}>Профиль</Link>
                        </li>
                        <li>
                        <button className="link logout-button" onClick={handleLogout}>Выйти</button>
                        </li>
                    </ul>:
                    <li>
                        <Link className="link" to={{pathname: `/login/`}}>Войти</Link>
                    </li>
                }
                <Search {...props}/>
            </ul>
        </nav>
    )
}

export default NavBar;
