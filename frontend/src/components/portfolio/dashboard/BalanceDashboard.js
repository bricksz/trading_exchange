import React, {Component} from "react";
import {Box, Card, Grid, Typography} from "@mui/material";
import Balance from "../balance/Balance";
import Chart from "../chart/Chart";

export default class BalanceDashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {}

        // this.props.cash_balance
        // this.props.equities          // Array
        // this.props.stocks_price      // Dictionary

        this.calculateTotalBalance = this.calculateTotalBalance.bind(this);
    }

    calculateTotalBalance() {
        let total_balance = this.props.cash_balance
        const stocks_price = this.props.stocks_price
        const equities = this.props.equities

        if (equities !== null) {
            equities.map( equity => (
                total_balance += (equity.quantity * stocks_price[equity.symbol])
            ))
        }
        return total_balance
    }

    render() {
        const balance = this.calculateTotalBalance()
        return (
            <Box>
                <Card elevation={0} variant="outlined" sx={{ borderRadius: 2 }}>
                    <Grid container spacing={1} direction="column" sx={{ m: "1rem" }}>
                        <Grid item xs={12}>
                            <Balance balance={balance}/>
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