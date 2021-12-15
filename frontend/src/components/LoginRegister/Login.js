import React from "react";
import Form from "react-validation/build/form";
import AuthService from "../../services/auth.service";
import {Link} from "react-router-dom";
import AbstractLogRegComponent from "./AbstractLogRegComponent";
import "./LoginRegister.css"


class Login extends AbstractLogRegComponent {
    state = {
        email: this.props.location?.state?.email,
        password: this.props.location?.state?.password,
        loading: false,
        message: ""
    }

    handleLogin = e => {
        e.preventDefault();

        this.setState({
            message: "",
            loading: true
        });

        this.form.validateAll();

        if (this.checkBtn.context._errors.length === 0) {
            AuthService.login(this.state.email, this.state.password).then(
                () => {
                    this.props.history.push("/");
                    window.location.reload();
                },
                error => {
                    let resMessage =
                        (error.response &&
                            error.response.data &&
                            error.response.data.message) ||
                        error.message ||
                        error.toString();

                    if (error.response.status === 401) {
                        resMessage = "Email or password are not correct"
                    }
                    this.setState({
                        loading: false,
                        message: resMessage
                    });
                }
            );
        } else {
            this.setState({
                loading: false
            });
        }
    }

    render() {
        return (
            <div className="login-wrapper">
                <Form
                    onSubmit={this.handleLogin}
                    ref={c => {
                        this.form = c;
                    }}>
                    <div className="form-wrapper">

                        {this.getEmail()}
                        {this.getPassword()}
                        <div className="link-to-register">
                            <Link to={{pathname: `/register/`}}>Register</Link>
                        </div>
                        {this.getSubmitButton(true)}
                        {this.getErrorMessages()}
                    </div>
                </Form>
            </div>
        );
    }
}

export default Login;