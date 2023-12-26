import React, {Component} from "react";
import {Box, Card, CircularProgress, Grid, Typography} from "@mui/material";
import { useParams } from "react-router-dom";
import StockChartDashboard from "./dashboard/StockChartDashboard";
import OrderDashboard from "./dashboard/OrderDashboard";
import StockAssetDashboard from "./dashboard/StockAssetDashboard";
import Announcements from "../announcements/Announcements";

export function withRouter(Children) {
    return(props) => {
        const match  = {params: useParams()};
        return <Children {...props} match = {match}/>
    }
}

// export default class Stocks extends Component {
class Stocks extends Component {
    constructor(props) {
        super(props);
        this.state = {
            token: this.props.token,

            name: null,
            description: null,
            shares_outstanding: null,
            symbol: null,
            quote: null,
            active: false,

            quantity: null,
            basis: null,
            options: [],
            loading_stock: true,
        };

        // stock = {
        //     "name": "Apple",
        //     "description": "",
        //     "shares_outstanding": 300000000,
        //     "symbol": "AAPL",
        //     "quote": 67.98,
        //     "active": true
        // }
        // equity = {
        //     "id": 66,
        //     "symbol": "AAPL",
        //     "quantity": 107,
        //     "basis": 50.63,
        //     "user_securities_account": 1
        // }

        // this.props.token
        // this.props.symbol

        this.symbol = this.props.match.params.symbol;
        this.getUserEquities = this.getUserEquities.bind(this);
        this.getStockSymbol = this.getStockSymbol.bind(this);
        this.getLocalToken = this.getLocalToken.bind(this);
        this.displayLoading = this.displayLoading.bind(this);

        this.getLocalToken();
    }

     getLocalToken() {
        const token = localStorage.getItem('token') || this.props.token
        this.setState({token: token});
        return token
    }

    componentDidMount() {
        this.interval = setInterval(() => this.getStockSymbol(this.symbol), 1500);
        this.interval = setInterval(() => this.getUserEquities(this.props.token, this.symbol), 1500)
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    getUserEquities(token, symbol) {
        if (!token) {
            console.log("null token:", token);
            return
        }
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' +  String(token)
            },
        };
        fetch('/api/equities/?symbol=' + String(symbol), requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/equities/?symbol=");
                    return
                }
                return response.json();
            })
            .then((data) => {
                if (data) {
                    this.setState({
                        quantity: data.quantity,
                        basis: data.basis,
                    });
                }
            })
            .catch(error => {
                console.error(error);
            });
    }

    getStockSymbol(symbol) {
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': 'Token ' +  String(token)
            },
        };
        fetch('/api/symbol/?symbol=' + String(symbol).toUpperCase(), requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/symbol/");
                    return
                }
                return response.json();
            })
            .then((data) => {
                if (data) {
                    this.setState({
                        name: data.name,
                        description: data.description,
                        shares_outstanding: data.shares_outstanding,
                        symbol: data.symbol,
                        quote: data.quote,
                        active: data.active,

                        loading_stock: false,
                    })
                }
            })
            .catch(error => {
                console.error(error);
            });
    }

    displayLoading() {
        return (
            <Grid container alignItems="center" justify="center">
                <Grid item container xs={12} justifyContent="center" alignItems="center"
                      style={{
                          minHeight: "30rem"
                      }}>
                    <CircularProgress size={75} />
                </Grid>
            </Grid>
        );
    }

    render() {
        return (
            <Box sx={{ minHeight: "90vh", mt: "10vh"}}>
                {
                    this.state.loading_stock ? this.displayLoading() :
                    <Grid container spacing={3} sx={{px: "2rem", py: "1.5rem"}}>
                        <Grid item xs={12} sm={12} md={12} lg={12}>
                            <Grid container spacing={3} direction="row">
                                <Grid item xs={12} sm={12} md={6} lg={6}>
                                    <StockChartDashboard
                                        name={this.state.name}
                                        symbol={this.state.symbol}
                                        quote={this.state.quote}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={12} md={6} lg={6}>
                                    <OrderDashboard
                                        token={this.props.token}
                                        symbol={this.state.symbol}
                                        quote={this.state.quote}
                                    />
                                </Grid>
                            </Grid>
                        </Grid>
                        <Grid item xs={12} sm={12} md={12} lg={12}>
                            <StockAssetDashboard
                                quote={this.state.quote}
                                symbol={this.state.symbol}
                                quantity={this.state.quantity}
                                basis={this.state.basis}
                                options={this.state.options}
                            />
                        </Grid>
                        <Grid item xs={12} sm={12} md={12} lg={12}>
                            <Announcements/>
                        </Grid>
                    </Grid>
                }
            </Box>
        )
    }
}

export default withRouter(Stocks);