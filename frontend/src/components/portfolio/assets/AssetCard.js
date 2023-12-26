import React, {Component} from "react";
import {Box, Card, CardActionArea, CardContent, Grid, Typography} from "@mui/material";
import {Link} from "react-router-dom";

export default class AssetCard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            // price: null,
        }

        // this.props.token
        // this.props.equity_id
        // this.props.symbol
        // this.props.quantity
        // this.props.basis
        // this.props.price
        // this.props.value

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
                <Card sx={{ borderTop: 1, borderColor: '#E0E0E0' }}>
                    <CardActionArea component="a" href={`/stocks/${this.props.symbol}`}>
                        <CardContent>
                            <Grid container spacing={2} direction="row">
                                {/*Symbol*/}
                                <Grid item xs={6} sm={3} md={3} lg={3}>
                                    <Typography>
                                        {this.props.symbol}
                                    </Typography>
                                </Grid>

                                {/*Shares*/}
                                <Grid item xs={0} sm={2} md={2} lg={2}
                                      sx={{ display: { xs: "none", lg: "block", md: "block", sm: "block"} }} >
                                    <Typography>
                                        {this.props.quantity}
                                    </Typography>
                                </Grid>

                                {/*Price*/}
                                <Grid item xs={0} sm={2} md={2} lg={2}
                                      sx={{ display: { xs: "none", lg: "block", md: "block", sm: "block"} }} >
                                    <Typography>
                                        {this.props.price}
                                    </Typography>
                                </Grid>

                                {/*Basis*/}
                                <Grid item xs={0} sm={2} md={2} lg={2}
                                      sx={{ display: { xs: "none", lg: "block", md: "block", sm: "block"} }} >
                                    <Typography>
                                        {this.props.basis}
                                    </Typography>
                                </Grid>

                                {/*Value*/}
                                <Grid item xs={6} sm={3} md={3} lg={3}>
                                    <Typography>
                                        {this.props.value}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </CardActionArea>
                </Card>
            </React.Fragment>
        )
    }
}