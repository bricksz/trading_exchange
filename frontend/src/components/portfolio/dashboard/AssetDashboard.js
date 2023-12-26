import React, {Component} from "react";
import {Box, Card, CardActionArea, CardContent, CardHeader, Grid, Typography} from "@mui/material";
import AssetCard from "../assets/AssetCard";


export default class AssetDashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {}
        // this.props.token
        // this.props.equities          // Array
        // this.props.stocks_price      // Dictionary

        this.numberFormat = this.numberFormat.bind(this);
        this.assetGridCard = this.assetGridCard.bind(this);
    }

    numberFormat(value) {
        if (value == null) {
            return null
        }
        return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }

    assetGridCard(equities) {
        // equities.id
        // equities.symbol
        // equities.quantity
        // equities.basis

        if (equities == null) {
            console.log("equities null")
            return
        }
        const equityArray = equities.map( equity => (
            <AssetCard
                equity_id={equity.id}
                symbol={equity.symbol}
                quantity={this.numberFormat(equity.quantity)}
                basis={this.numberFormat(equity.basis)}
                price={this.numberFormat(this.props.stocks_price[equity.symbol])}
                value={this.numberFormat(equity.quantity*this.props.stocks_price[equity.symbol])}
            />
        ));
        return (
            <React.Fragment>
                <Grid item xs={12}>
                    <Card sx={{ borderTop: 1, borderColor: '#E0E0E0' }}>
                        <CardContent>
                            <Grid container spacing={2} direction="row">
                                <Grid item xs={6} sm={3} md={3} lg={3}>
                                    <Typography>
                                        Symbol
                                    </Typography>
                                </Grid>
                                <Grid item xs={0} sm={2} md={2} lg={2}
                                      sx={{ display: { xs: "none", lg: "block", md: "block", sm: "block"} }} >
                                    <Typography>
                                        Shares
                                    </Typography>
                                </Grid>
                                <Grid item xs={0} sm={2} md={2} lg={2}
                                      sx={{ display: { xs: "none", lg: "block", md: "block", sm: "block"} }} >
                                    <Typography>
                                        Price
                                    </Typography>
                                </Grid>
                                <Grid item xs={0} sm={2} md={2} lg={2}
                                      sx={{ display: { xs: "none", lg: "block", md: "block", sm: "block"} }} >
                                    <Typography>
                                        Basis
                                    </Typography>
                                </Grid>
                                <Grid item xs={6} sm={3} md={3} lg={3}>
                                    <Typography>
                                        Value
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12}>
                    { equityArray }
                </Grid>
            </React.Fragment>
        );
    }


    render() {
        return (
            <Box>
                <Card elevation={0} variant="outlined" sx={{ borderRadius: 2 }}>
                    <Grid spacing={0} direction="column">
                        <Grid item xs={12}>
                            <Card>
                                <CardHeader title="Your Assets" />
                            </Card>
                        </Grid>
                        { this.assetGridCard(this.props.equities) }
                    </Grid>
                </Card>
            </Box>
        )
    }
}