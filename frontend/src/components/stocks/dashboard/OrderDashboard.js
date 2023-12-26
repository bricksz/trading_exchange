import React, {Component} from "react";
import {Box, Card, Divider, Grid, Typography} from "@mui/material";
import Order from "../order/Order";

export default class OrderDashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {}

        // this.props.token
        // this.props.symbol
        // this.props.quote
    }

    render() {
        return (
            <Box sx={{ height: "100%"}}>
                <Card elevation={0} variant="outlined" sx={{ borderRadius: 2, height: "100%" }}>
                    <Grid container spacing={1} direction="column" sx={{ m: "1rem" }}>
                        <Grid item xs={12}>
                            <Order
                                token={this.props.token}
                                symbol={this.props.symbol}
                                quote={this.props.quote}
                            />
                        </Grid>
                        <Divider sx={{ my: "1rem" }}/>
                        <Grid item xs={12}>
                        </Grid>
                    </Grid>
                </Card>
            </Box>
        )
    }
}