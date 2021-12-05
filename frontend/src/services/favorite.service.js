import Tokens from "./auth-header";
import axios from "axios";

export const handleMoveToFavorite = (key, favorite, func) => {
    const accessToken = Tokens.AccessTokenHeader();
    let method = "POST";
    if (favorite) method = "DELETE";
    axios({
        method: method,
        url: `http://localhost:8080/api/books/favorites/`,
        headers: {
            'Content-type': 'application/json',
            'Authorization': accessToken
        },
        data: {
            book_id: key
        }

    }).then((response) => {
        func(response.data.favorite)
        }
    ).catch(error => {
            if (error.request?.status === 401) {
                alert("You need to login")
            }
            else
                console.log(error)
        }
    )
}