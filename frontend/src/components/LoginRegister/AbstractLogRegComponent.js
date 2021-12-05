import Input from "react-validation/build/input";
import {email, password, required} from "../../utils";
import CheckButton from "react-validation/build/button";
import "./LoginRegister.css"
const {Component} = require("react");

class AbstractLogRegComponent extends Component {

    onChangeEmail = e => {
        this.setState({
            email: e.target.value
        });
    }

    onChangePassword = e =>{
        this.setState({
            password: e.target.value
        });
    }
    getEmail() {
        return <div className="input-box">
            <label className="input-title" htmlFor="email">Email</label>
            <Input
                type="email"
                className="input"
                name="email"
                value={this.state.email}
                onChange={this.onChangeEmail}
                validations={[required, email]}
            />
        </div>
    }
    getPassword() {
        return <div className="input-box">
            <label  className="input-title" htmlFor="password">Password</label>
            <Input
                type="password"
                className="input"
                name="password"
                value={this.state.password}
                onChange={this.onChangePassword}
                validations={[required, password]}
            />
        </div>
    }
    getSubmitButton(isLog) {
        let text = "Sign up"
        if (isLog) text = "Login"
        return <div>
            <button className="signup-button"
                disabled={this.state.loading}>
                <span>{text}</span>
            </button>
        </div>
    }
    getErrorMessages() {
        return <div>
            {this.state.message && (
                <div>
                    <div
                        role="alert">
                        {this.state.message}
                    </div>
                </div>
            )}
            <CheckButton
                style={{display: "none"}}
                ref={c => {
                    this.checkBtn = c;
                }}
            />
        </div>
    }
}
export default AbstractLogRegComponent