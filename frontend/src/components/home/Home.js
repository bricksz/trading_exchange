import React, {Component} from "react";
import {Box, CircularProgress, Grid, Typography} from "@mui/material";
import Announcements from "../announcements/Announcements";
import BalanceDashboard from "../portfolio/dashboard/BalanceDashboard";
import AssetDashboard from "../portfolio/dashboard/AssetDashboard";

export default class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            type: null,
            cash_balance: 0,
            equity: null,           // Array
            equities: null,         // Array
            stocks_price: {},     // Dictionary

            loading_usa: true,
            loading_equities: true,
        };
        // this.props.token
        this.getUserSecuritiesAccount = this.getUserSecuritiesAccount.bind(this);
        this.getUserEquities = this.getUserEquities.bind(this);
        this.getUserStocks = this.getUserStocks.bind(this);
        this.displayLoading = this.displayLoading.bind(this);

        this.getUserSecuritiesAccount();
    }

    componentDidMount() {
        this.interval = setInterval(() => this.getUserSecuritiesAccount(this.props.token), 1500);
        this.interval = setInterval(() => this.getUserEquities(this.props.token), 1500);
        this.interval = setInterval(() => this.getUserStocks(this.props.token), 1500);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    getUserSecuritiesAccount(token) {
        if (!token) {
            console.log("Token UserSecuritiesAccount", token);
            return
        }
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' +  String(token)
            },
            // body: JSON.stringify({}),
        };
        fetch('/api/account/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/account/");
                    return
                }
                return response.json();
            })
            .then((data) => {
                if (data) {
                    this.setState({
                        type: data.type,
                        cash_balance: data.cash_balance,
                        equity: data.equity,

                        loading_usa: false,
                    });
                }
            })
            .catch(error => {
                console.error(error);
            });
    }

    getUserEquities(token) {
        if (!token) {
            console.log("Token Equities", token);
            return
        }
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' +  String(token)
            },
        };
        fetch('/api/equities/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/equities/");
                    return
                }
                return response.json();
            })
            .then((data) => {
                if (data) {
                    this.setState({
                        equities: data,

                        loading_equities: false,
                    });
                }
            })
            .catch(error => {
                console.error(error);
            });
    }

    getUserStocks(token) {
        if (!token) {
            console.log("Token UserStocks", token);
            return
        }
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' +  String(token)
            },
        };
        fetch('/api/stocks/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/equities/");
                    return
                }
                return response.json();
            })
            .then((data) => {
                if (data) {
                    const stocks_price = {};
                    for (let i=0;i<data.length;i++) {
                        stocks_price[data[i].symbol] = data[i].quote
                    }
                    this.setState({
                        stocks_price: stocks_price,
                    });
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
                          minHeight: "28rem"
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
                    this.state.loading_usa || this.state.loading_equities ? this.displayLoading() :
                    <Grid container spacing={3} sx={{px: "2rem", py: "1.5rem"}}>
                        <Grid item xs={12} sm={12} md={9} lg={9}>
                            <Box>
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <BalanceDashboard
                                            cash_balance={this.state.cash_balance}
                                            equities={this.state.equities}
                                            stocks_price={this.state.stocks_price}
                                        />
                                    </Grid>
                                    <Grid item xs={12}>
                                        <AssetDashboard
                                            token={this.props.token}
                                            equities={this.state.equities}
                                            stocks_price={this.state.stocks_price}
                                        />
                                    </Grid>
                                </Grid>
                            </Box>

                        </Grid>
                        <Grid item xs={12} sm={12} md={3} lg={3}>
                            <Announcements/>
                        </Grid>
                    </Grid>
                }
            </Box>
        )
    }
}