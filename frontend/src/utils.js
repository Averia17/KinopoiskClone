import {isEmail} from "validator";
import React from "react";

export const required = value => {
    if (!value) {
        return (
            <div role="alert">
                Это обязательно поле!
            </div>
        );
    }
};


export const email = value => {
    if (!isEmail(value)) {
        return (
            <div role="alert">
                Некорректный email
            </div>
        );
    }
};


export const password = value => {
    if (value.length < 8) {
        return (
            <div role="alert">
                Пароль должен быть длиннее 8 символов
            </div>
        );
    }
};

export const confirmPassword = (value, password) => {
    if (value !== password) {
        return (
            <div role="alert">
               Пароли не совпадают
            </div>
        );
    }
};

export const rating = value => {
    if (value > 10 || value < 0) {
        return (
            <div role="alert">
                Рейтинг должен быть от 0 до 10
            </div>
        );
    }
};


export const year = value => {
    if (value > 2030 || value < 0) {
        return (
            <div role="alert">
                Год должен быть от 0 до 2030
            </div>
        );
    }
    if (!Number.isInteger(value)) {
        return (
            <div role="alert">
                Введите целое значение
            </div>
        );
    }
};


