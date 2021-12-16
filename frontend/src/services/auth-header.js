class Tokens {
    AccessTokenHeader() {
        const user = JSON.parse(localStorage.getItem('user'));

        if (user && user.access) {
            return 'Bearer ' + user.access;
        } else {
            return null;
        }
    }
    RefreshTokenHeader() {
        const user = JSON.parse(localStorage.getItem('user'));

        if (user && user.refresh) {
            return user.refresh;
        } else {
            return null;
        }
    }
    getCurrentUserTokens() {
        return JSON.parse(localStorage.getItem('user'));
    }
}
export default new Tokens();