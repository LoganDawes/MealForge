import React from "react";
import { Link } from "react-router-dom";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "./Color.css"

const Navigationbar = () => {
  const isLoggedIn = !!localStorage.getItem("accessToken");

  return (
    <Navbar bg="light" expand="lg" className="px-3 fixed-top">
      <Container fluid className="d-flex justify-content-between">
        <Navbar.Brand as={Link} to="/">MealForge</Navbar.Brand>

        <Nav className="mx-auto">
          <Nav.Link as={Link} to="/ingredients">Ingredients</Nav.Link>
          <Nav.Link as={Link} to="/recipes">Recipes</Nav.Link>
        </Nav>

        <Nav>
          <NavDropdown title={<span className="bi bi-person-circle"></span>} id="profile-dropdown" align="end">
            {isLoggedIn ? (
              <>
                <NavDropdown.Item as={Link} to="/profile">Profile</NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/login">Switch Account</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={() => {
                  localStorage.removeItem("accessToken");
                  window.location.reload(); // or use navigation to redirect
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
