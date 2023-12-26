import React, {Component} from "react";
import {Typography} from "@mui/material";

export default class Footer extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <footer className="footer" style={{ background: "#f0f0f0", padding: "1rem" }}>
                <Typography variant="h6" align="center" gutterBottom>
                    Footer
                </Typography>
                <Typography variant="subtitle1" align="center" color="textSecondary" component="p">
                    Footer Information goes here.
                </Typography>
            </footer>
        )
    }
}