import React from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { Button, Typography } from "@mui/material";
import Box from "@mui/material/Box";

const Navbar = ({ sessionManager }) => {
  console.log("Nav render");
  const navigate = useNavigate();
  const location = useLocation();

  const logout = () => {
    sessionManager.logout();
    sessionManager.setSessionMessageWrapper("Logged out");
  };

  return (
    <nav
      style={{
        display: "flex",
        alignItems: "center",
        paddingBottom: 10,
        border: "none",
      }}
    >
      <Typography variant="h6">
        <Link to="/" style={{ textDecoration: "none" }}>
          DoseMeRx Support
        </Link>
      </Typography>
      <div style={{ minWidth: 20 }}></div>
      <Box
        sx={{
          flexGrow: 1,
          color: "red",
          border: "none",
        }}
      >
        <Typography
          style={{ fontSize: 12, fontWeight: "bold" }}
          align="center"
        ></Typography>
      </Box>
      <Box sx={{ flexGrow: 0, fontSize: "1em" }}>
        {sessionManager.user?.userID > 0 ? (
          <span>
            <Link
              style={{
                textDecoration: "none",
                color: location.pathname === "/profile" ? "#1976d2" : "gray",
                fontWeight:
                  location.pathname === "/profile" ? "bold" : "normal",
              }}
              to="/profile"
            >
              {sessionManager.user.userName}
            </Link>{" "}
            |{" "}
            <Link
              style={{
                textDecoration: "none",
                color: location.pathname === "/kb" ? "#1976d2" : "gray",
                fontWeight: location.pathname === "/kb" ? "bold" : "normal",
              }}
              to="/kb"
            >
              kb
            </Link>{" "}
            |{" "}
            <Link
              style={{
                textDecoration: "none",
                color: location.pathname === "/history" ? "#1976d2" : "gray",
                fontWeight: location.pathname === "/history" ? "bold" : "normal",
              }}
              to="/history"
            >
              history
            </Link>{" "}
            |{" "}
            <Link
              style={{ textDecoration: "none", color: "gray" }}
              to="#"
              onClick={logout}
            >
              logout
            </Link>
          </span>
        ) : (
          <Link
            style={{ textDecoration: "none", color: "gray" }}
            to="#"
            onClick={() => {
              sessionManager.showLogin();
            }}
          >
            login
          </Link>
        )}
      </Box>
    </nav>
  );
};

export default Navbar;
