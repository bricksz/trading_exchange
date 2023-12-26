import React, {Component} from "react";
import {Box, Typography} from "@mui/material";

export default class QuoteHeader extends Component {
    constructor(props) {
        super(props);
        // this.props.quote
        // this.props.symbol
        // this.props.company_name

        this.numberFormat = this.numberFormat.bind(this);
    }

    numberFormat(value) {
        if (value !== null) {
            return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
        }
        return value
    }

    render() {
        const quote = this.props.quote
        const symbol = this.props.symbol
        const name = this.props.name
        return (
            <Box>
                <Typography variant="h4">
                    {name}
                </Typography>
                <Typography variant="h4">
                    ${this.numberFormat(quote)}
                </Typography>
            </Box>
        )
    }
}