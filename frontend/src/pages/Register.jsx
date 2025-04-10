import React, { useState } from "react";
import Navigationbar from "../components/Navbar";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container } from "react-bootstrap";
import "./Color.css";
import axios from "axios";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    
    // Detect if the password and confirm password fields match
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    try {
      // Register user
      await axios.post("/api/register/", {
        username: formData.username,
        email: formData.email,
        password: formData.password
      });

      // Automatically log in
      const loginRes = await axios.post("/api/login/", {
        username: formData.username,
        password: formData.password
      });

      localStorage.setItem("username", formData.username);

      localStorage.setItem("accessToken", loginRes.data.access);
      localStorage.setItem("refreshToken", loginRes.data.refresh);

      navigate("/");
    } catch (error) {
      console.error("Registration/Login Error:", error);
    
      if (error.response) {
        // Backend returned a response
        console.error("Response data:", error.response.data);
        console.error("Status code:", error.response.status);
        alert(error.response.data.detail || "Registration failed");
      } else if (error.request) {
        // Request was made but no response
        console.error("No response received:", error.request);
        alert("No response from server. Check API gateway address.");
      } else {
        // Something else
        console.error("Error setting up request:", error.message);
        alert("An unexpected error occurred");
      }
    }
  };

  return (
    <>
      <Navigationbar />
      <Container className="d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
        <Card style={{ width: "100%", maxWidth: "400px", marginTop: "80px" }} className="p-4 shadow">
          <h3 className="text-center mb-3">Sign up</h3>
          <p className="text-center">
            <Link to="/login">Already have an account</Link>
          </p>
          <Form onSubmit={handleRegister}>
            <Form.Group controlId="username" className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                name="username"
                type="text"
                placeholder="Enter username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </Form.Group>
            <Form.Group controlId="email" className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                name="email"
                type="email"
                placeholder="Enter email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </Form.Group>
            <Form.Group controlId="password" className="mb-3">
              <Form.Label>Password</Form.Label>
              <Form.Control
                name="password"
                type="password"
                placeholder="Enter password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </Form.Group>
            <Form.Group controlId="confirmPassword" className="mb-4">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                name="confirmPassword"
                type="password"
                placeholder="Confirm password"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100">
              Sign up
            </Button>
          </Form>
        </Card>
      </Container>
    </>
  );
};

export default Register;
