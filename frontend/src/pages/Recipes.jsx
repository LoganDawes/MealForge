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
  const [activeTab, setActiveTab] = useState("search");

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

  // Function to fetch saved recipes
  const fetchSavedRecipes = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setRecipes([]); // Set recipes to an empty array if no token is available
      return;
    }

    setLoading(true);
    try {
      const response = await axios.get(`/api/user/recipes`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setRecipes(response.data.recipes); // Assuming the API returns a list of saved recipes
    } catch (err) {
      console.error("Failed to load saved recipes:", err);
      setRecipes([]); // Set recipes to an empty array in case of an error
    }
    setLoading(false);
  };

  // Handle tab change
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  // Fetch recipes when activeTab changes
  useEffect(() => {
    if (activeTab === "search") {
      handleSearch(""); // Trigger search with an empty term
    } else if (activeTab === "saved") {
      fetchSavedRecipes();
    }
  }, [activeTab]);

  return (
    <div className="Recipes">
      <Navigationbar />
      <SubNavbar
        pageTitle="Recipes"
        onSearch={handleSearch}
        activeTab={activeTab}
        onTabChange={handleTabChange}
      />

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