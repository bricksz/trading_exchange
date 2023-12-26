import React, {Component} from "react";
import {Box, Card, Divider, Grid, Stack, Typography} from "@mui/material";



export default class OptionCard extends Component {
    constructor(props) {
        super(props);
        this.state = {}

        this.numberFormat = this.numberFormat.bind(this);
    }

    numberFormat(value) {
        if (value == null) {
            return null
        }
        return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }


    render() {
        return (
            <React.Fragment>
                <Card elevation={0} variant="outlined" sx={{ borderRadius: 2, height: "100%" }} >
                    <Grid container spacing={1} direction="column" sx={{ m: "1rem" }}>
                        <Grid item xs={12}>
                            <Typography variant="h4">
                                Options
                            </Typography>
                            <Divider sx={{ my: "1rem" }}/>
                        </Grid>
                        <Grid item xs={12}>
                            <Grid container direction="row">
                                <Grid item xs={3}>
                                    <Stack direction="column">
                                        <Typography fontSize={14} variant="h6">
                                            Options
                                        </Typography>
                                        <Typography>
                                            5
                                        </Typography>
                                    </Stack>
                                </Grid>
                                <Grid item xs={3}>
                                    <Typography fontSize={14} variant="h6">
                                        Value
                                    </Typography>
                                    <Typography>
                                        ${this.numberFormat(1168.00)}
                                    </Typography>
                                </Grid>
                                <Grid item xs={3}>
                                    <Typography fontSize={14} variant="h6">
                                        Total P/L
                                    </Typography>
                                    <Typography>
                                        ${this.numberFormat(-3060.50)} (-72.21%)
                                    </Typography>
                                </Grid>
                                <Grid item xs={3}>
                                    <Typography fontSize={14} variant="h6">
                                        Collateral
                                    </Typography>
                                    <Typography>
                                        ${this.numberFormat(19900)}
                                    </Typography>
                                </Grid>
                            </Grid>
                            <Divider sx={{ my: "1rem" }}/>
                            <Grid item xs={12}>
                                {/*option card array goes here*/}
                            </Grid>
                        </Grid>
                    </Grid>
                </Card>
            </React.Fragment>
        )
    }
}