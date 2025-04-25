import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "./Color.css"

const Navigationbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("accessToken");
  const username = localStorage.getItem("username");

  return (
    <Navbar style={{ backgroundColor: "#461bb2" }} expand="lg" className="px-3 fixed-top">
      <Container fluid className="d-flex justify-content-between">
        <Navbar.Brand as={Link} to="/" style={{ color: "white" }}>MealForge</Navbar.Brand>

        <Nav className="mx-auto">
          <Nav.Link as={Link} to="/ingredients" style={{ color: "white" }}>Ingredients</Nav.Link>
          <Nav.Link as={Link} to="/recipes" style={{ color: "white" }}>Recipes</Nav.Link>
        </Nav>

        <Nav>
          {isLoggedIn ? (
            <Nav.Link as={Link} to="/profile" style={{ color: "white" }}>{username}</Nav.Link>
          ) : (
            <Nav.Link as={Link} to="/login" style={{ color: "white" }}>Log In</Nav.Link>
          )}
          <NavDropdown title={<span className="bi bi-person-circle" style={{ color: "white" }}></span>} id="profile-dropdown" align="end">
            {isLoggedIn ? (
              <>
                <NavDropdown.Item as={Link} to="/profile">Profile</NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/login">Switch Account</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={() => {
                  localStorage.removeItem("accessToken");
                  navigate("/");
                }}>Logout</NavDropdown.Item>
              </>
            ) : (
              <>
                <NavDropdown.Item as={Link} to="/login">Log In</NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/register">Sign Up</NavDropdown.Item>
              </>
            )}
          </NavDropdown>
        </Nav>
      </Container>
    </Navbar>
  );
};
export default Navigationbar;
