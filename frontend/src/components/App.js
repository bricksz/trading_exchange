import React, { Component, Fragment } from "react";
import { render } from "react-dom";
import {Box, Typography} from "@mui/material";

import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";

import Footer from "./layout/Footer";
import Header from "./layout/Header";
import Home from "./home/Home";
import Login from "./login/Login";
import Register from "./register/Register";
import Stocks from "./stocks/Stocks"
import StockList from "./stocks/StockList";


export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            token: null,
        };
        this.userLogin = this.userLogin.bind(this);
        this.setToken = this.setToken.bind(this);
        this.getLocalToken = this.getLocalToken.bind(this);

        this.getLocalToken();
    }

    getLocalToken() {
        const token = localStorage.getItem('token') || this.props.token
        this.setToken(token);
        return token
    }

    setToken(e) {
        this.setState({
            token: e,
        });
    }

    userLogin(tok) {
        this.setToken(tok);
        if (window.location.pathname === "/login") {
            window.location.href = "/"
        }
    }

    // async componentDidMount() {
    //     this.getLocalToken();
    // }

    render() {
        return (
            <Box>
                <BrowserRouter>
                    <Fragment>
                        <Header token={this.state.token} />
                        <Box>
                            <Routes>
                                <Route exact path="/" element={
                                    this.state.token ?
                                        (<Home token={this.state.token} />) : (<Login userLogin={this.userLogin}/>)
                                } />
                                <Route path="/login" element={<Login userLogin={this.userLogin}/>} />
                                <Route path="/register" element={<Register userLogin={this.userLogin}/>} />
                                <Route path="/stocks/:symbol" element={
                                    this.state.token ?
                                        (<Stocks token={this.state.token} />) : (<Login userLogin={this.userLogin}/>)
                                } />
                                <Route path="/trade" element={
                                    this.state.token ?
                                        (<StockList token={this.state.token} />) : (<Login userLogin={this.userLogin}/>)
                                } />
                            </Routes>
                        </Box>
                        <Footer />
                    </Fragment>
                </BrowserRouter>
            </Box>
        )
    }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
