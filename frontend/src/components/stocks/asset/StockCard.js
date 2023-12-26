import React, {Component} from "react";
import {Box, Card, Divider, Grid, Stack, Typography} from "@mui/material";



export default class StockCard extends Component {
    constructor(props) {
        super(props);
        this.state = {}

        // this.props.quote
        // this.props.symbol
        // this.props.quantity
        // this.props.basis
        // this.props.options       // Dict

        this.numberFormat = this.numberFormat.bind(this);
    }

    numberFormat(value) {
        if (value == null) {
            return null
        }
        return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }

    render() {
        const mark_value = this.props.quantity*this.props.quote
        const total_pl = mark_value - (this.props.quantity*this.props.basis)
        return (
            <React.Fragment>
                <Grid container spacing={3} direction="row">

                    {/*Mark Value & P/L Card*/}
                    <Grid item xs={4}>
                        <Card elevation={0} variant="outlined" sx={{ borderRadius: 2, height: "100%" }} >
                            <Grid container spacing={0} direction="column" sx={{ m: "2rem" }}>
                                <Grid item xs={12}>
                                    <Typography fontSize={16}>
                                        Mark Value
                                    </Typography>
                                </Grid>
                                <Grid item xs={12}>
                                    <Typography variant="h6">
                                        ${this.numberFormat(mark_value)}
                                    </Typography>
                                </Grid>
                                <Grid item xs={12}>
                                    <Divider sx={{ my: "0.5rem" }} />
                                    <Stack direction="row" spacing={1} alignItems="center">
                                        <Typography fontSize={14} sx={{ minWidth: "6rem" }}>
                                            Total P/L
                                        </Typography>
                                        <Typography fontSize={14}>
                                            ${this.numberFormat(total_pl)}
                                        </Typography>
                                    </Stack>
                                </Grid>
                            </Grid>
                        </Card>
                    </Grid>

                    {/*Basis & Shares Card*/}
                    <Grid item xs={4}>
                        <Card elevation={0} variant="outlined" sx={{ borderRadius: 2, height: "100%" }} >
                            <Grid container spacing={0} direction="column" sx={{ m: "2rem" }}>
                                <Grid item xs={12}>
                                    <Typography fontSize={16}>
                                        Average Basis
                                    </Typography>
                                </Grid>
                                <Grid item xs={12}>
                                    <Typography variant="h6">
                                        ${this.numberFormat(this.props.basis)}
                                    </Typography>
                                </Grid>
                                <Grid item xs={12}>
                                    <Divider sx={{ my: "0.5rem" }} />
                                    <Stack direction="row" spacing={1} alignItems="center">
                                        <Typography fontSize={14} sx={{ minWidth: "6rem" }}>
                                            Shares
                                        </Typography>
                                        <Typography fontSize={14}>
                                            {this.numberFormat(this.props.quantity)}
                                        </Typography>
                                    </Stack>
                                </Grid>
                            </Grid>
                        </Card>
                    </Grid>

                    <Grid item xs={4}>
                    </Grid>
                </Grid>
            </React.Fragment>
        )
    }
}