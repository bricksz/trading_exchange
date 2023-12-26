import React, {Component} from "react";
import {AppBar, Box, Button, Toolbar, Typography, Link} from "@mui/material";

export default class Header extends Component {
    constructor(props) {
        super(props);
        this.state = {
            token: ""
        }
        this.logout = this.logout.bind(this);
    }

    logout() {
        localStorage.removeItem('token');
        if (window) window.location.href = "/"
    }


    render() {
        return (
            <Box>
                <AppBar position="fixed" elevation={0} variant="outlined" sx={{ bgcolor: "#fff" }}>
                    <Toolbar>
                        <Typography  variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            <Link
                                color="text.primary"
                                sx={{ my: 1, mx: 1.5 }}
                                style={{ textDecoration: "none", color: "#2196f3" }}
                                href="/"
                            >
                                Stonks
                            </Link>
                        </Typography>
                        <Box sx={{ mx: 1 }}>
                            <Button href="/trade" sx={{ color: "#2196f3" }}>
                                Trade
                            </Button>
                        </Box>
                        <Box sx={{ mx: 1 }}>
                            {
                                (localStorage.getItem('token') !== null || this.props.token !== null) ?
                                <Button onClick={this.logout} sx={{ color: "#2196f3" }}>
                                    Logout
                                </Button> : null
                            }
                        </Box>
                    </Toolbar>
                </AppBar>
            </Box>
        )
    }
}