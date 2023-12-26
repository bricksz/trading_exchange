import React, {Component} from "react";
import {Box, Card, CardActionArea, CardContent, CardHeader, Divider, Grid, Typography} from "@mui/material";
import AssetCard from "../../portfolio/assets/AssetCard";
import StockCard from "../asset/StockCard";
import OptionCard from "../asset/OptionCard";


export default class StockAssetDashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {}

        // this.props.token
        // this.props.equity        // Dict
        // this.props.quote

        // equity = {
        //     "id": 66,
        //     "symbol": "AAPL",
        //     "quantity": 107,
        //     "basis": 50.63,
        //     "user_securities_account": 1
        // }

        this.numberFormat = this.numberFormat.bind(this);
        this.assetGridCard = this.assetGridCard.bind(this);
    }

    numberFormat(value) {
        if (value == null) {
            return null
        }
        return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }

    // Do not use
    assetGridCard(equity) {
        // equity.id
        // equity.symbol
        // equity.quantity
        // equity.basis

        if (equity == null) {
            console.log("equity null")
            return
        }
        return (
            <React.Fragment>
                <Grid item xs={12}>
                    <Card sx={{ borderTop: 0, borderColor: '#E0E0E0' }}>
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
                    <AssetCard
                        equity_id={equity.id}
                        symbol={equity.symbol}
                        quantity={this.numberFormat(equity.quantity)}
                        basis={this.numberFormat(equity.basis)}
                        price={this.numberFormat(this.props.stock_quote)}
                        value={this.numberFormat(equity.quantity*this.props.stock_quote)}
                    />
                </Grid>
            </React.Fragment>
        );
    }


    render() {
        return (
        <Box>
            {/*<Card elevation={0} variant="outlined" sx={{ borderRadius: 2 }}>*/}
            {/*    <Grid spacing={0} direction="column">*/}
            {/*        { this.assetGridCard(this.props.equity) }*/}
            {/*    </Grid>*/}
            {/*</Card>*/}

            <Grid container spacing={3} direction="columns">
                <Grid item xs={12}>
                    <StockCard
                        quote={this.props.quote}
                        symbol={this.props.symbol}
                        quantity={this.props.quantity}
                        basis={this.props.basis}
                        options={this.props.options}
                    />
                </Grid>
                <Divider />
                <Grid item xs={12}>
                    <OptionCard />
                </Grid>
            </Grid>
        </Box>
        )
    }
}