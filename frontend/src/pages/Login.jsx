import React, { useState } from "react";
import Navigationbar from "../components/Navbar";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container } from "react-bootstrap";
import "./Color.css";
import axios from "axios";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("/api/login/", {
        username: username,
        password: password
      });

      localStorage.setItem("username", username);

      localStorage.setItem("accessToken", res.data.access_token);
      localStorage.setItem("refreshToken", res.data.refresh_token);

      navigate("/");

    } catch (error) {
      console.error("Login Error:", error);
      const msg = error.response?.data?.detail || "Login failed";
      alert(msg);
    }
  };

  return (
    <>
      <Navigationbar />
      <Container className="d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
        <Card style={{ width: "100%", maxWidth: "400px", marginTop: "80px" }} className="p-4 shadow">
          <h3 className="text-center mb-3">Log in</h3>
          <p className="text-center">
            <Link to="/register">Create an account</Link>
          </p>
          <Form onSubmit={handleLogin}>
            <Form.Group controlId="username" className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="password" className="mb-4">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100">
              Log in
            </Button>
          </Form>
        </Card>
      </Container>
    </>
  );
};

export default Login;
