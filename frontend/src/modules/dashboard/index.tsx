import { Cached, DriveFolderUpload, Help } from "@mui/icons-material";
import {
  Box,
  Button,
  Container,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  LinearProgress,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
import axios from "axios";
import React, { Fragment, useEffect, useState } from "react";

const BASE_URL = "http://localhost:8000";

export default function Dashboard(): React.ReactNode {
  const [selectedFile, setSelectedFile] = useState<any>(null);
  const [uploadProgress, setUploadProgress] = useState<any>(0);
  const [uploading, setUploading] = useState(false);

  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  const [terminal, setTerminal] = useState<any>("");

  useEffect(() => {
    if (localStorage.getItem("accessToken")) setIsAuthenticated(true);
  }, [() => localStorage.getItem("accessToken")]);

  const handleLogin = async () => {
    try {
      // Open popup window for authentication
      const popup = window.open(
        "http://localhost:8000/login",
        "GitHub Authentication",
        "width=600,height=400"
      );
      if (!popup) {
        throw new Error("Popup blocked. Please enable popups for this site.");
      }

      // Listen for messages from popup window
      window.addEventListener("message", (event) => {
        if (
          event.origin === "http://localhost:8000" &&
          event.data.access_token
        ) {
          // Save access token to localStorage
          localStorage.setItem("accessToken", event.data.access_token);
          // Close popup window
          popup.close();
        }
      });
    } catch (error) {
      console.error(error);
    }
  };

  const handleFileChange = (event: any) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (selectedFile) {
      try {
        setUploading(true);
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("name", "trial-of-combat-zl");
        formData.append("description", "This is another repository");
        // Do not append rarFilePath here

        const response = await axios.post(
          BASE_URL + "/projects/github/receive-push",
          formData,
          {
            onUploadProgress: (progressEvent) => {
              const progress = Math.round(
                (progressEvent.loaded / progressEvent.total) * 100
              );
              setUploadProgress(progress);
            },
          }
        );

        console.log("Upload successful", response.data);
      } catch (error) {
        console.error("Error uploading file", error);
      } finally {
        setUploading(false);
      }
    } else {
      console.log("No file selected");
    }
  };

  return (
    <Fragment>
      <Container maxWidth={"xl"}>
        <Grid container spacing={2} gap={2}>
          <Grid
            item
            md={5}
            sx={{
              minHeight: "60vh",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flexDirection: "column",
            }}
          >
            <Box
              sx={{
                display: isAuthenticated ? "none" : "",
              }}
            >
              <Button onClick={handleLogin}>Login to Github</Button>
            </Box>
            <Box
              p={2}
              mb={2}
              sx={{
                width: "100%",
                // border: "solid thin blue",
                border: "solid navy 3px",
                boxShadow: "6px 6px navy",
                borderRadius: "12px",
              }}
            >
              <Box
                sx={{
                  textAlign: "left",
                }}
              >
                <Typography variant="h5">✨ Create Project</Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>
                  Select the project you would like to work with
                </Typography>
              </Box>

              <FormControl fullWidth sx={{ mt: 3 }}>
                <InputLabel id="demo-simple-select-label">
                  Select language
                </InputLabel>
                <Select
                  value={0}
                  label={"Select language"}
                  labelId={"demo-simple-select-label"}
                >
                  <MenuItem value={0}>Java</MenuItem>
                  <MenuItem value={1}>Python</MenuItem>
                  <MenuItem value={1}>Go Lang</MenuItem>
                </Select>
              </FormControl>

              {/* Hidden input element */}
              <input
                type="file"
                style={{ display: "none" }}
                onChange={handleFileChange}
                id="upload-button"
              />
              {/* Clickable area */}
              <label htmlFor="upload-button">
                <Box
                  mt={5}
                  p={3}
                  mb={5}
                  sx={{
                    cursor: "pointer",
                    border: "dashed thin blue",
                    borderRadius: "10px",
                    textAlign: "center",
                  }}
                >
                  {/* <TouchApp sx={{ width: "64px", height: "64px", m: 3, color: "blue" }} /> */}
                  <DriveFolderUpload
                    sx={{ width: "64px", height: "64px", m: 3, color: "blue" }}
                  />
                  <Typography variant="body1">
                    Drag and drop files here or click to select file
                  </Typography>
                </Box>
              </label>

              {selectedFile && (
                <Box mt={2} mb={3}>
                  <Typography variant="subtitle1" sx={{ mb: 2, color: "gray" }}>
                    {selectedFile.name}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={uploadProgress}
                  />
                </Box>
              )}

              {uploading && (
                <Typography variant="body1">Uploading...</Typography>
              )}

              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "flex-start",
                    alignItems: "center",
                    gap: "12px",
                    color: "gray",
                  }}
                >
                  <Help />
                  <Typography>Help center</Typography>
                </Box>
                <Box>
                  <Button>Cancel</Button>
                  <Button
                    variant="contained"
                    disableElevation
                    onClick={handleUpload}
                  >
                    Submit
                  </Button>
                </Box>
              </Box>
            </Box>
            <Typography variant="caption" sx={{ color: "gray", mt: 1 }}>
              A project is a codebase that can be deployed and buit within the
              project context
            </Typography>
          </Grid>
          <Grid item md={6}>
            <Box
              sx={{
                m: 1,
                p: 2,
                backgroundColor: "navy",
                borderRadius: "12px",
                color: "white",
              }}
            >
              <Typography
                variant="h4"
                sx={{ fontWeight: "bold", color: "white" }}
              >
                Result
                <IconButton
                  onClick={async () => {
                    await axios
                      .get(
                        "http://localhost:8000/projects/container/file-content/",
                        {
                          params: {
                            image_name: "sample",
                            tag: "latest",
                            file_path: "./test-output.txt",
                          },
                        }
                      )
                      .then((res) => {
                        setTerminal(res.data);
                        console.log(res.data);
                      })
                      .finally(() => {
                        alert("Aqui");
                      });
                  }}
                >
                  <Cached sx={{ color: "white" }} />
                </IconButton>
              </Typography>
              <pre>
                <code style={{ fontSize: "1.1em" }}>{terminal}</code>
              </pre>
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Fragment>
  );
}
