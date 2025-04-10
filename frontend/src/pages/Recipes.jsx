import React, { useState, useEffect } from "react";
import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import RecipeCard from '../components/RecipeCard';
import RecipePopup from "../components/RecipePopup";
import { Container, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css";
import axios from 'axios';

function Recipes() {
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [recipes, setRecipes] = useState([]); // State to store recipe search results
  const [loading, setLoading] = useState(false); // Loading state for search results

  // Function to handle search
  const handleSearch = async (searchTerm) => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/search/recipes`, {
        params: {
          query: searchTerm,
          addRecipeNutrition: true,
          addRecipeInstructions: true
        }
      });
      setRecipes(response.data.results); // Update the state with the search results
    } catch (error) {
      console.error("Error fetching recipes:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    handleSearch(""); // Fetch recipes with an empty search term initially
  }, []);

  return (
    <div className="Recipes">
      <Navigationbar />
      <SubNavbar pageTitle="Recipes" onSearch={handleSearch} />
      
      <Container fluid className="pt-4" style={{ maxHeight: "calc(100vh - 180px)", overflowY: "auto" }}>
        <Row>
          {loading ? (
            <div>Loading...</div>
          ) : (
            recipes.map((recipe, index) => (
              <Col key={index} xs={12} md={6} lg={4}>
                <RecipeCard {...recipe} onClick={() => setSelectedRecipe(recipe)} />
              </Col>
            ))
          )}
        </Row>
      </Container>

      {selectedRecipe && (
        <RecipePopup recipe={selectedRecipe} onClose={() => setSelectedRecipe(null)} />
      )}
    </div>
  );
}

export default Recipes;