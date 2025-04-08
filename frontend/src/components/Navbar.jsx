import React from "react";
import { Link } from "react-router-dom";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "./Color.css"

const Navigationbar = () => {
  return (
    <Navbar bg="light" expand="lg" className="px-3 fixed-top">
      <Container fluid className="d-flex justify-content-between">
        {/* Home Logo */}
        <Navbar.Brand as={Link} to="/">MealForge</Navbar.Brand>
        
        {/* Ingredients & Recipes navigation buttons */}
        <Nav className="mx-auto">
          <Nav.Link as={Link} to="/ingredients">Ingredients</Nav.Link>
          <Nav.Link as={Link} to="/recipes">Recipes</Nav.Link>
        </Nav>
        
        {/* Profile dropdown */}
        <Nav>
          <NavDropdown title={<span className="bi bi-person-circle"></span>} id="profile-dropdown" align="end">
            <NavDropdown.Item as={Link} to="/profile">Profile</NavDropdown.Item>
            <NavDropdown.Item>Switch Account</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item>Logout</NavDropdown.Item>
          </NavDropdown>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default Navigationbar;
