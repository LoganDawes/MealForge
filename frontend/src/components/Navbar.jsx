import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "./Color.css"
import mealforgeLogo from "../assets/mealforge-logo.png";
import ingredientsLogo from "../assets/mealforge-ingredients.png";
import recipesLogo from "../assets/mealforge-recipes.png";

const Navigationbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isLoggedIn = !!localStorage.getItem("accessToken");
  const username = localStorage.getItem("username");

  return (
    <Navbar style={{ backgroundColor: "#461bb2" }} expand="lg" className="px-3 fixed-top">
      <Container fluid className="d-flex justify-content-between">
        <Navbar.Brand as={Link} to="/" style={{ color: "white", display: "flex", alignItems: "center" }}>
          <img
            src={mealforgeLogo}
            alt="MealForge Logo"
            style={{ height: "30px", marginRight: "8px" }}
          />
          <span style={{ fontSize: "1.25rem" }}>MealForge</span>
        </Navbar.Brand>

        <Nav className="mx-auto">
          <Nav.Link
            as={Link}
            to="/ingredients"
            style={{
              color: "white",
              display: "flex", alignItems: "center",
              fontWeight: location.pathname === "/ingredients" ? "bold" : "normal",
              marginRight: "24px",
            }}
          >
            <img
              src={ingredientsLogo}
              alt="Ingredients Logo"
              style={{ height: "25px", marginRight: "8px" }}
            />
            Ingredients
          </Nav.Link>
          <Nav.Link
            as={Link}
            to="/recipes"
            style={{
              color: "white",
              display: "flex",
              alignItems: "center",
              fontWeight: location.pathname === "/recipes" ? "bold" : "normal",
            }}
          >
            <img
              src={recipesLogo}
              alt="Recipes Logo"
              style={{ height: "25px", marginRight: "8px" }}
            />
            Recipes
          </Nav.Link>
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
