import React, {Component} from "react";
import {Box, Card, Grid, Typography} from "@mui/material";
import Chart from "../../portfolio/chart/Chart";
import QuoteHeader from "../quoteheader/QuoteHeader";

export default class StockChartDashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {}

        // this.props.name
        // this.props.symbol
        // this.props.quote
    }

    render() {
        return (
            <Box sx={{ height: "100%"}}>
                <Card elevation={0} variant="outlined" sx={{ borderRadius: 2, height: "100%" }}>
                    <Grid container spacing={1} direction="column" sx={{ m: "1rem" }}>
                        <Grid item xs={12}>
                            <QuoteHeader
                                name={this.props.name}
                                symbol={this.props.symbol}
                                quote={this.props.quote}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <Chart />
                        </Grid>
                    </Grid>
                </Card>
            </Box>
        )
    }
}