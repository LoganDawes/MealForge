import React, { useState } from "react";
import Navigationbar from "../components/Navbar";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Form, Button, Card, Container, OverlayTrigger, Popover } from "react-bootstrap";
import "./Color.css";
import axios_api from "../utils/axiosInstance";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    // Detect if the password and confirm password fields match
    if (formData.password !== formData.confirmPassword) {
      setErrorMessage("Passwords do not match");
      return;
    }

    // Validate password requirements
    const passwordRegex = /^(?=.*\d).{8,}$/; // At least 8 characters and includes a number
    if (!passwordRegex.test(formData.password)) {
      setErrorMessage("Password must be at least 8 characters long and include a number");
      return;
    }

    try {
      // Register user
      await axios_api.post("/register/", {
        username: formData.username,
        email: formData.email,
        password: formData.password
      }, {
        noAuth: true,
      });

      // Automatically log in
      const loginRes = await axios_api.post("/login/", {
        username: formData.username,
        password: formData.password
      }, {
        noAuth: true,
      });

      localStorage.setItem("username", formData.username);

      localStorage.setItem("accessToken", loginRes.data.access_token);
      localStorage.setItem("refreshToken", loginRes.data.refresh_token);

      navigate("/");
      navigate(0);
    } catch (error) {
      console.error("Registration/Login Error:", error);

      if (error.response) {
        // Backend returned a response
        const errorData = error.response.data;
        if (errorData.username) {
          setErrorMessage("Username is in use");

        } else if (errorData.email) {
          const emailError = errorData.email[0];
          if (emailError.includes("Invalid email address")) {
            setErrorMessage("Email is invalid");
          } else if (emailError.includes("already in use")) {
            setErrorMessage("Email is in use");
          } else {
            setErrorMessage("Email error: " + emailError);
          }

        } else {
          setErrorMessage(errorData.detail || "Registration failed");
        }
      } else if (error.request) {
        // Request was made but no response
        setErrorMessage("No response from server.");
      } else {
        // Something else
        setErrorMessage("An unexpected error occurred");
      }
    }
  };

  // Render location of any errors
  const renderErrorMessage = (field) => {
    if (field === "username" && errorMessage === "Username is in use") {
      return <small className="text-danger">{errorMessage}</small>;
    }
    if (field === "email" && (errorMessage === "Email is in use" || errorMessage === "Email is invalid")) {
      return <small className="text-danger">{errorMessage}</small>;
    }
    if (field === "password" && errorMessage === "Password must be at least 8 characters long and include a number") {
      return <small className="text-danger">{errorMessage}</small>;
    }
    if (field === "confirmPassword" && errorMessage === "Passwords do not match") {
      return <small className="text-danger">{errorMessage}</small>;
    }
    if (field === "general" && !["Username is in use", "Email is in use", "Email is invalid", "Passwords do not match", "Password must be at least 8 characters long and include a number"].includes(errorMessage)) {
      return <small className="text-danger d-block text-center mb-3">{errorMessage}</small>;
    }
    return null;
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
            {renderErrorMessage("general")}
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
              {renderErrorMessage("username")}
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
              {renderErrorMessage("email")}
            </Form.Group>
            <Form.Group controlId="password" className="mb-3">
              <Form.Label>Password</Form.Label>
              <OverlayTrigger
                trigger="focus"
                placement="bottom"
                overlay={
                  <Popover id="password-requirements">
                    <Popover.Body>
                      <ul style={{ margin: 0, paddingLeft: "20px" }}>
                        <li>Password must be 8+ characters</li>
                        <li>Password must include a number</li>
                      </ul>
                    </Popover.Body>
                  </Popover>
                }
              >
                <Form.Control
                  name="password"
                  type="password"
                  placeholder="Enter password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              </OverlayTrigger>
              {renderErrorMessage("password")}
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
              {renderErrorMessage("confirmPassword")}
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
