import React, { Component } from "react";
import {Alert, AlertTitle, Box, Button, Grid, Paper, Snackbar, Stack, TextField, Typography} from "@mui/material";
import {Link} from "react-router-dom";

export default class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: "",
            alert_error_open: false,
        };
        this.login = this.login.bind(this);
        this.handleAlertClose = this.handleAlertClose.bind(this);
        this.alertMessageError = this.alertMessageError.bind(this);
        this.redirectLogin = this.redirectLogin.bind(this);
        this.redirectLogin();
    }

    login() {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password,
            }),
        };

        fetch('/api/auth/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/auth/");
                    return JSON.stringify({ token: null})
                }
                return response.json();
            })
            .then((res) => {
                this.props.userLogin(res.token);
                localStorage.setItem('token', res.token);
                if (typeof res.token == 'undefined') {
                    this.setState({
                        alert_error_open: true
                    });
                    localStorage.removeItem('token');
                    console.log("login auth failed");
                } else {
                    console.log("login auth success");
                }
            })
            .catch(error => {
                console.error(error);
            });

        // version 2
        fetch('/api/auth/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    // leave call back function insert here
                    console.log("Call back error: /api/auth/");
                    // return JSON.stringify({ token: null})
                }
                if (response.status >= 400) {
                    return response.text().then(text => { throw new Error(text) })
                }
                return response.json();
            })
            .then((res) => {
                this.props.userLogin(res.token);
                localStorage.setItem('token', res.token);
            })
            .catch(error => {
                // this.setState({
                //     error_msg: String(error),
                //     error_alert: true,
                // })

                console.error(error);

                if (typeof res.token == 'undefined') {
                    this.setState({
                        alert_error_open: true
                    });
                    localStorage.removeItem('token');
                    console.log("login auth failed");
                } else {
                    console.log("login auth success");
                }
            });
    }

    redirectLogin() {
        const token = localStorage.getItem('token') || null
        if (token) {
            this.props.userLogin(token);
        }
    }

    handleAlertClose(event, reason) {
        if (reason === 'clickaway') {
            return;
        }
        this.setState({alert_error_open: false});
    }

    alertMessageError() {
        return (
            <Snackbar open={this.state.alert_error_open} autoHideDuration={6000} onClose={this.handleAlertClose}>
                <Alert
                    anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
                    onClose={this.handleAlertClose}
                    severity="error"
                >
                    Login Failed!
                </Alert>
            </Snackbar>
        );
    }

    render() {
        return (
            <Box sx={{ minHeight: "90vh"}}>
                <Grid container
                      spacing={0} align="center" justifyContent="center" direction="column"
                      sx={{ minHeight: "90vh", bgcolor: "#f0f0f0" }}
                >
                    <Grid item sx={{ mx: "auto" }}>
                        <Paper elevation={2}>
                            <Grid sx={{ py: "2rem", px: "1.5rem"}}>
                                <Grid item xs={12} sm={12} md={12} lg={12} sx={{ mb: "1rem", color: "#2196f3" }}>
                                    <Typography gutterBottom variant="h6" component="h2" style={{ wordWrap: "break-word" }}>
                                        Sign in to Stonks
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12} sx={{ mb: "1rem" }}>
                                    <TextField
                                        label="Username"
                                        variant="outlined"
                                        defaultValue=""
                                        fullWidth
                                        onChange={e => { this.setState({ username: e.target.value }) }}
                                        onKeyPress={(e) => {if (e.key === "Enter") {this.login()}}}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12} sx={{ mb: "1rem" }}>
                                    <TextField
                                        type="password"
                                        label="Password"
                                        variant="outlined"
                                        defaultValue=""
                                        fullWidth
                                        onChange={e => { this.setState({ password: e.target.value }) }}
                                        onKeyPress={(e) => {if (e.key === "Enter") {this.login()}}}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12} >
                                    <Stack direction="row" spacing={1} sx={{ mt: "1rem", ml: "0.5rem" }}>
                                        <Box component={Stack} direction="column" justifyContent="center" sx={{  mr: "1rem" }}>
                                            <Typography>
                                                Dont have account? <Link to="/register">Register Here</Link>
                                            </Typography>
                                        </Box>
                                        <Button
                                            variant="contained"
                                            onClick={this.login}
                                        >
                                            Sign in
                                        </Button>
                                    </Stack>
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12}>
                                    { this.alertMessageError() }
                                </Grid>
                            </Grid>
                        </Paper>
                    </Grid>
                </Grid>
            </Box>
        );
    }
}