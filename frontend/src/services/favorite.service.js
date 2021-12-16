import Tokens from "./auth-header";
import axios from "axios";

export const handleMoveToFavorite = (key, favorite) => {
    const accessToken = Tokens.AccessTokenHeader();
    let method = "POST";
    let url = `http://localhost:8080/api/favorites/`
    let data =  {id: key}
    if (favorite) {
        method = "DELETE";
        url = `http://localhost:8080/api/favorites/${key}/`
        data = {}
    }
    return axios({
        method: method,
        url: url,
        headers: {
            'Content-type': 'application/json',
            'Authorization': accessToken
        },
        data: data
    })
}