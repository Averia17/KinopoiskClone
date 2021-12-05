import {isEmail} from "validator";
import React from "react";

export const required = value => {
    if (!value) {
        return (
            <div role="alert">
                This field is required!
            </div>
        );
    }
};


export const email = value => {
    if (!isEmail(value)) {
        return (
            <div role="alert">
                This is not a valid email.
            </div>
        );
    }
};


export const password = value => {
    if (value.length < 8) {
        return (
            <div role="alert">
                The password must be longer than 8 characters.
            </div>
        );
    }
};

export const confirmPassword = (value, password) => {
    if (value !== password) {
        return (
            <div role="alert">
                Passwords in two inputs are not equals.
            </div>
        );
    }
};
