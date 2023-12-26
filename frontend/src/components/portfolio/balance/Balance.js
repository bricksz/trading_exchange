import React, {Component} from "react";
import {Box, Typography} from "@mui/material";
import {Title} from "@mui/icons-material";

export default class Balance extends Component {
    constructor(props) {
        super(props);
        this.numberFormat = this.numberFormat.bind(this);
    }

    numberFormat(value) {
        return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }

    render() {
        const balance = this.props.balance
        return (
            <Box>
                <Typography component="h2" variant="h6" color="primary" gutterBottom>
                    Your Balance
                </Typography>
                <Typography component="p" variant="h4">
                    ${this.numberFormat(balance)}
                </Typography>
            </Box>
        )
    }
}