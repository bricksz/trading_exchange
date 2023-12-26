import React, {Component} from "react";
import {Card, CardActionArea, CardActions, CardContent, CardHeader, Typography} from "@mui/material";
import * as PropTypes from "prop-types";

function CardAction(props) {
    return null;
}

CardAction.propTypes = {children: PropTypes.node};
export default class AnnouncementCard extends Component {
    constructor(props) {
        super(props);

        // this.props.title
        // this.props.body
        // this.props.url
    }

    render() {
        const title = this.props.title || "Announcement Title"
        const body = this.props.body || "Announcement information goes here."
        const url = this.props.url || "Click"
        return (
            <React.Fragment>
                <Card elevation={0} variant="outlined" sx={{ borderRadius: 2 }}>
                    <CardHeader title={title}/>
                    <CardContent>
                        <Typography>
                            {body}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        <CardActionArea sx={{ borderRadius: 2 }}>
                            <Typography sx={{ mx: "1rem", my: "0.5rem" }}>
                                {url}
                            </Typography>
                        </CardActionArea>
                    </CardActions>
                </Card>
            </React.Fragment>
        )
    }
}