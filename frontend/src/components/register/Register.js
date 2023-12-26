import React, { Component } from "react";
import {Alert, AlertTitle, Box, Button, Grid, Paper, Snackbar, Stack, TextField, Typography} from "@mui/material";
import {Link} from "react-router-dom";

export default class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: "",
            alert_success_open: false,
            alert_error_open: false,
        };
        this.register = this.register.bind(this);
        this.handleAlertClose = this.handleAlertClose.bind(this);
        this.alertMessageSuccess = this.alertMessageSuccess.bind(this);
        this.alertMessageError = this.alertMessageError.bind(this);
    }

    register() {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password,
            }),
        };

        fetch('/api/users/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    this.setState({alert_error_open: true});
                    console.log("Call back error: /api/users/");
                } else {
                    this.setState({alert_success_open: true});
                }
                return response;
            })
            .then((res) => {
                if (res.ok) {return fetch('/api/auth/', requestOptions)}
                return res;
            })
            .then(res => {
                if (!res.ok) {return JSON.stringify({ token: null})}
                return res.json();
            })
            .then((res) => {
                this.props.userLogin(res.token);
                localStorage.setItem('token', res.token);
                if (typeof res.token == 'undefined') {
                    localStorage.removeItem('token');
                    console.log("login auth failed");
                } else {
                    console.log("login auth success");
                    window.location.href = "/"
                }
            })
            .catch(error => {
                console.error(error);
            });
    }

    handleAlertClose(event, reason) {
        if (reason === 'clickaway') {
            return;
        }
        this.setState({alert_success_open: false});
        this.setState({alert_error_open: false});
    }

    alertMessageSuccess() {
        return (
            <Snackbar open={this.state.alert_success_open} autoHideDuration={6000} onClose={this.handleAlertClose}>
                <Alert
                    anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
                    onClose={this.handleAlertClose}
                    severity="success"
                >
                    Register Success!
                </Alert>
            </Snackbar>
        );
    }

    alertMessageError() {
        return (
            <Snackbar open={this.state.alert_error_open} autoHideDuration={6000} onClose={this.handleAlertClose}>
                <Alert
                    anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
                    onClose={this.handleAlertClose}
                    severity="error"
                >
                    Register Failed!
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
                                        Register
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12} sx={{ mb: "1rem" }}>
                                    <TextField
                                        label="Username"
                                        variant="outlined"
                                        defaultValue=""
                                        fullWidth
                                        onChange={e => { this.setState({ username: e.target.value }) }}
                                        onKeyPress={(e) => {if (e.key === "Enter") {this.register()}}}
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
                                        onKeyPress={(e) => {if (e.key === "Enter") {this.register()}}}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12} >
                                    <Stack direction="row" spacing={1} sx={{ mt: "1rem", ml: "0.5rem" }}>
                                        <Box component={Stack} direction="column" justifyContent="center" sx={{  mr: "1rem" }}>
                                            <Typography>
                                                Have an account? <Link to="/login">Login Here</Link>
                                            </Typography>
                                        </Box>
                                        <Button
                                            variant="contained"
                                            onClick={this.register}
                                        >
                                            Register
                                        </Button>
                                    </Stack>
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12}>
                                    { this.alertMessageError() }
                                    { this.alertMessageSuccess() }
                                </Grid>
                            </Grid>
                        </Paper>
                    </Grid>
                </Grid>
            </Box>
        );
    }
}