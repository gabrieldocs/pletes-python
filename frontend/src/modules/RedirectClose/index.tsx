import React from "react";
import { Box, Button, Container, Grid, Typography } from "@mui/material";
import { useLocation } from "react-router-dom";

export default function RedirectClose() {
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const accessToken = searchParams.get('access_token');
    React.useEffect(() => {
        if (accessToken) {
            localStorage.setItem("accessToken", accessToken);
            // Refresh the original window
            window.opener.location.reload();

            // Attempt to close the window
            window.close();
        }
    }, [accessToken])

    // Function to close the window
    const handleCloseWindow = () => {
        window.close();
    };

    return (
        <>
            <Container>
                <Grid container>
                    <Grid item md={12}>
                        <Box p={3} sx={{
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "center",
                            alignItems: "center"
                        }}>
                            <Typography variant="h5">All right, you can continue from here</Typography>
                            <Button variant="contained" disableElevation onClick={handleCloseWindow}>Close window</Button>
                        </Box>
                    </Grid>
                </Grid>
            </Container>
        </>
    )
}