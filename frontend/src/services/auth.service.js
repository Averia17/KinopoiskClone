import axios from "axios";
import Tokens from "./auth-header";

const API_URL = "http://localhost:8080/api/";

class AuthService {
    login(email, password) {
        return axios
            .post(API_URL + "login/", {
                email,
                password
            })
            .then(response => {
                if (response.data.access) {
                    localStorage.setItem("user", JSON.stringify(response.data));
                }
                return response.data;
            });
    }

    logout(refresh) {
        return axios
            .post(API_URL + "refresh-token/", {
                    refresh
                })
            .then(response => {
                localStorage.removeItem("user");
                return response.data;
            });
    }

    register(email, password) {
        return axios.post(API_URL + "register/", {
            email,
            password
        });
    }

    // get information about current user
    getCurrentUser() {
        return axios
            .get(API_URL, {headers: {'Authorization': Tokens.AccessTokenHeader()}})
            .then(response => {
                return response.data
            });
    }
}

export default new AuthService();