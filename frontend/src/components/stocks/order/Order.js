import React, {Component} from "react";
import {Box, Button, CircularProgress, Grid, MenuItem, Stack, TextField, Typography} from "@mui/material";
import CheckIcon from '@mui/icons-material/Check';

export default class Order extends Component {
    constructor(props) {
        super(props);
        this.state = {
            token: null,

            symbol: this.props.symbol || "",
            instruction: "BUY",
            order_type: "MKT",
            quantity: 0,
            price: 0.00,

            order_loading: false,
            order_confirmed: false,
        };

        // this.props.token
        // this.props.symbol
        // this.props.quote

        this.orderPriceInput = this.orderPriceInput.bind(this);
        this.submitOrder = this.submitOrder.bind(this);
        this.displayOrderLoading = this.displayOrderLoading.bind(this);
    }

    submitOrder(token) {
        if (!token) {
            console.log("null token:", token);
            return
        }
        if (this.state.quantity <= 0) {
            console.log("must enter positive quantity")
            return
        }
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' +  String(token)
            },
            body: JSON.stringify({
                symbol: this.state.symbol,
                order_type: this.state.order_type,
                instruction: this.state.instruction,
                quantity: this.state.quantity,
                price: this.state.price,
            }),
        };

        this.setState({order_loading: true, order_confirmed:false})
        fetch('/api/order/', requestOptions)
            .then((response) => {
                if (!response.ok) {
                    console.log("Call back error: /api/order/");
                    return
                }
                return response.json();
            })
            .then((res) => {
                this.setState({
                    order_confirmed: true,
                    order_loading: false
                })
                console.log("order success!")
                console.log(res)
            })
            .catch(error => {
                console.error(error);
            });
    }

    displayOrderLoading() {
        if (this.state.order_confirmed) {
            return (
                <CheckIcon color="success" fontSize="medium" sx={{ marginLeft: "0.5rem" }} />
            );
        } else if (this.state.order_loading) {
            return (
                <CircularProgress size={25} sx={{ml: "0.5rem"}} />
            );
        } else {}
    }

    orderPriceInput(input_order_type) {
        if (input_order_type === "LMT") {
            return (
                <React.Fragment>
                    <Typography component="h2" variant="h6" sx={{minWidth: "8rem"}}>
                        Limit Price
                    </Typography>
                    <TextField
                        type="number"
                        size="small"
                        onChange={e => {
                            this.setState({price: e.target.value})
                        }}
                    />
                </React.Fragment>
            );
        } else {
            return (
                <React.Fragment>
                    <Typography component="h2" variant="h6" sx={{minWidth: "8rem", color: "#808080"}} />
                    <TextField
                        disabled
                        hiddenLabel
                        variant="filled"
                        type="number"
                        size="small"
                    />
                </React.Fragment>
            );
        }
    }

    render() {
        return (
            <Box
                component="form"
                sx={{
                    '& .MuiTextField-root': {width: '25ch'},
                }}
                noValidate
                autoComplete="off"
            >
                <Grid container direction="column" spacing={2}>
                    <Grid item xs={12}>
                        <Stack direction="row" spacing={1} alignItems="center">
                            <Typography component="h2" variant="h6" sx={{minWidth: "8rem"}}>
                                Instruction
                            </Typography>
                            <TextField
                                size="small"
                                select
                                value={this.state.instruction}
                                onChange={e => {
                                    this.setState({instruction: e.target.value})
                                }}
                            >
                                <MenuItem key="BUY" value="BUY">
                                    BUY
                                </MenuItem>
                                <MenuItem key="SELL" value="SELL">
                                    SELL
                                </MenuItem>
                            </TextField>
                        </Stack>
                    </Grid>
                    <Grid item xs={12}>
                        <Stack direction="row" spacing={1} alignItems="center">
                            <Typography component="h2" variant="h6" sx={{minWidth: "8rem"}}>
                                Order Type
                            </Typography>
                            <TextField
                                size="small"
                                select
                                value={this.state.order_type}
                                onChange={e => {
                                    this.setState({order_type: e.target.value})
                                }}
                            >
                                <MenuItem key="Market" value="MKT">
                                    Market
                                </MenuItem>
                                <MenuItem key="Limit" value="LMT">
                                    Limit
                                </MenuItem>
                            </TextField>
                        </Stack>
                    </Grid>
                    <Grid item xs={12}>
                        <Stack direction="row" spacing={1} alignItems="center">
                            <Typography variant="h6" sx={{minWidth: "8rem"}}>
                                Shares
                            </Typography>
                            <TextField
                                type="number"
                                size="small"
                                onChange={e => {
                                    this.setState({quantity: e.target.value})
                                }}
                            />
                        </Stack>
                    </Grid>

                    <Grid item xs={12}>
                        <Stack direction="row" spacing={1} alignItems="center">
                            { this.orderPriceInput(this.state.order_type) }
                        </Stack>
                    </Grid>

                    <Grid item xs={12}>
                        <Stack direction="row" spacing={1} alignItems="center">
                            <Typography fontSize={16} variant="h6" sx={{minWidth: "8rem"}} color="primary">
                                Market Price
                            </Typography>
                            <Typography>
                                ${this.props.quote}
                            </Typography>
                        </Stack>
                    </Grid>

                    <Grid item xs={12}>
                        <Stack direction="row" spacing={1} alignItems="center">
                            <Typography component="h2" variant="h6" sx={{minWidth: "8rem", color: "#808080"}} />
                            <Button
                                variant="contained"
                                onClick={() => this.submitOrder(this.props.token)}
                            >
                                Submit Order
                            </Button>
                            <Box>
                                { this.displayOrderLoading() }
                            </Box>
                        </Stack>
                    </Grid>
                </Grid>
            </Box>
        );
    }
}