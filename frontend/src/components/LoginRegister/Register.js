import React from "react";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import AuthService from "../../services/auth.service";
import {required, confirmPassword} from "../../utils"
import AbstractLogRegComponent from "./AbstractLogRegComponent"
import "./LoginRegister.css"

class Register extends AbstractLogRegComponent {
    state = {
        email: "",
        password: "",
        confirmPassword: "",
        successful: false,
        message: ""
    }

    onChangeConfirmPassword = e => {
        this.setState({
            confirmPassword: e.target.value
        });
    }

    handleRegister = e =>{
        e.preventDefault();

        this.setState({
            message: "",
            successful: false
        });

        this.form.validateAll();

        if (this.checkBtn.context._errors.length === 0) {
            AuthService.register(
                this.state.email,
                this.state.password
            ).then(
                response => {
                    this.setState({
                        message: response.data.message,
                        successful: true
                    });
                    this.props.history.push({pathname: '/login',
                                            state:{ email: this.state.email,
                                                    password:this.state.password}
                                            })
                },
                error => {
                    let resMessage =
                        (error.response &&
                            error.response.data &&
                            error.response.data.message) ||
                        error.message ||
                        error.toString();
                    if (error.response.status === 400)
                    {
                        resMessage = "Not acceptable email or password"
                    }
                    this.setState({
                        successful: false,
                        message: resMessage
                    });
                }
            );
        }
    }

    render() {
        return (
            <div className="login-wrapper">
                <Form
                    onSubmit={this.handleRegister}
                    ref={c => {
                        this.form = c;
                    }}>
                    {!this.state.successful && (
                        <div className="form-wrapper">
                            {this.getEmail()}
                            {this.getPassword()}
                            <div className="input-box">
                                <label className="input-title" htmlFor="confirmPassword">Confirm Password</label>
                                <Input
                                    className="input"
                                    type="password"
                                    name="confirmPassword"
                                    value={this.state.confirmPassword}
                                    onChange={this.onChangeConfirmPassword}
                                    validations={[required, (value) => confirmPassword(value, this.state.password)]}
                                />
                            </div>
                            {this.getSubmitButton(false)}

                        </div>
                    )}

                    {this.getErrorMessages()}

                </Form>
            </div>
        );
    }
}

export default Register;