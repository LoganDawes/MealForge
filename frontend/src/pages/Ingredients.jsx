import React, { useState, useEffect } from "react";
import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import IngredientCard from '../components/IngredientCard';
import IngredientPopup from "../components/IngredientPopup";
import { Container, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css";
import axios from 'axios';

function Ingredients() {
  const [selectedIngredient, setSelectedIngredient] = useState(null);
  const [ingredients, setIngredients] = useState([]); // State to store ingredient search results
  const [loading, setLoading] = useState(false); // Loading state for search results
  const [activeTab, setActiveTab] = useState("search");

  // Function to handle search
  const handleSearch = async (searchTerm) => {
    if (activeTab !== "search") return;
    setLoading(true);
    try {
      // 1. Fetch ingredient IDs based on search term
      const response = await axios.get(`/api/search/ingredients`, {
        params: {
          query: searchTerm
        }
      });

      // 2. Fetch detailed data for each ingredient by its ID
      const ingredientDetailsPromises = response.data.results.map(async (ingredient) => {
        const ingredientResponse = await axios.get(`/api/ingredients/${ingredient.id}`);
        return ingredientResponse.data; // Return the detailed ingredient data
      });

      // Wait for all API calls to complete
      const fullIngredients = await Promise.all(ingredientDetailsPromises);

      // 3. Update state with the full ingredient data
      setIngredients(fullIngredients);
    } catch (error) {
      console.error("Error fetching ingredients:", error);
    }
    setLoading(false);
  };

  const fetchSavedIngredients = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setIngredients([]); // Set ingredients to an empty array if no token is available
      return;
    }
  
    setLoading(true);
    try {
      const response = await axios.get(`/api/user/ingredients`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setIngredients(response.data.ingredients);
    } catch (err) {
      console.error("Failed to load saved ingredients:", err);
      setIngredients([]); // Set ingredients to an empty array in case of an error
    }
    setLoading(false);
  };

  // Handle tab change
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  // Fetch ingredients when activeTab changes
  useEffect(() => {
    if (activeTab === "search") {
      handleSearch(""); // Trigger search with an empty term
    } else if (activeTab === "saved") {
      fetchSavedIngredients();
    }
  }, [activeTab]);

  return (
    <div className="Ingredients">
      <Navigationbar />
      <SubNavbar
        pageTitle="Ingredients"
        onSearch={handleSearch}
        activeTab={activeTab}
        onTabChange={handleTabChange}
      />

      <Container fluid className="pt-4" style={{ maxHeight: "calc(100vh - 180px)", overflowY: "auto" }}>
        <Row>
          {loading ? (
            <div>Loading...</div>
          ) : (
            ingredients.map((ingredient, index) => (
              <Col key={index} xs={12} sm={6} md={4} lg={2} xl={2}>
                <IngredientCard {...ingredient} onClick={() => setSelectedIngredient(ingredient)} />
              </Col>
            ))
          )}
        </Row>
      </Container>

      {selectedIngredient && (
        <IngredientPopup ingredient={selectedIngredient} onClose={() => setSelectedIngredient(null)} />
      )}
    </div>
  );
}

export default Ingredients;