import React, {Component} from "react";
import {Box, Typography} from "@mui/material";

export default class Chart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: []
        }
    }

    render() {
        return (
            <React.Fragment>
                <Box>
                    <Typography>
                        Giant chart goes here.
                    </Typography>
                    <Typography>
                        Giant chart goes here.
                    </Typography>
                    <Typography>
                        Giant chart goes here.
                    </Typography>
                    <Typography>
                        Giant chart goes here.
                    </Typography>
                    <Typography>
                        Giant chart goes here.
                    </Typography>
                </Box>
            </React.Fragment>
        )
    }
}