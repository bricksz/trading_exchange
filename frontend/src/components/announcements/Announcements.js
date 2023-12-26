import React, {Component} from "react";
import {Box, Card, CardActionArea, CardContent, CardHeader, Grid, Typography} from "@mui/material";
import AnnouncementCard from "./AnnouncementCard";

export default class Announcements extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Box>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <AnnouncementCard />
                    </Grid>
                    <Grid item xs={12}>
                        <AnnouncementCard title="Where did my money go?" body="DESPAIR" />
                    </Grid>
                    <Grid item xs={12}>
                        <AnnouncementCard title="Wage cuck workers" body="Clueless" />
                    </Grid>
                </Grid>
            </Box>
        )
    }
}