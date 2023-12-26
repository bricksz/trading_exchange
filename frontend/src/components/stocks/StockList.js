import React, {Component} from "react";
import {Box, Card, CircularProgress, Grid, Typography} from "@mui/material";
import { useParams } from "react-router-dom";
import StockChartDashboard from "./dashboard/StockChartDashboard";
import OrderDashboard from "./dashboard/OrderDashboard";
import StockAssetDashboard from "./dashboard/StockAssetDashboard";
import Announcements from "../announcements/Announcements";
import AssetCard from "../portfolio/assets/AssetCard";


export default class StockList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            token: this.props.token,
            stocks: [],
        };

        // stocks = [{
        //     "name": "Apple",
        //     "description": "",
        //     "shares_outstanding": 300000000,
        //     "symbol": "AAPL",
        //     "quote": 64.1,
        //     "active": true
        // }, ...]

        // this.props.token

        this.getStockList = this.getStockList.bind(this);
        this.stocksGridCard = this.stocksGridCard.bind(this);

        this.getStockList()
    }


    getStockList() {
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': 'Token ' +  String(token)
            },
        };
        fetch('/api/stock-list/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/stock-list/");
                    return
                }
                return response.json();
            })
            .then((data) => {
                if (data) {
                    this.setState({
                        stocks: data
                    });
                }
            })
            .catch(error => {
                console.error(error);
            });
    }

    stocksGridCard(stocks) {
        if (!stocks) {
            console.log("null stocks:", stocks);
            return
        }
        const stocksArray = stocks.map( stock => (
            <Box>
                <Typography>
                    Stock Name: {stock.name}
                </Typography>
                <Typography>
                    Stock Description: {stock.description}
                </Typography>
                <Typography>
                    Shares Outstanding: {stock.shares_outstanding}
                </Typography>
                <Typography>
                    Symbol: {stock.symbol}
                </Typography>
                <Typography>
                    Quote: {stock.quote}
                </Typography>
            </Box>
        ));
        return (
            <React.Fragment>
                {stocksArray}
            </React.Fragment>
        );
    }

    render() {
        return (
            <Box sx={{ minHeight: "90vh", mt: "10vh"}}>
                {this.stocksGridCard(this.state.stocks)}
            </Box>
        )
    }
}