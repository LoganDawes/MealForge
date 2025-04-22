import React, { useState, useEffect } from "react";
import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import IngredientCard from '../components/IngredientCard';
import IngredientPopup from "../components/IngredientPopup";
import { Container, Row, Col, Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css";
import axios_api from "../utils/axiosInstance";

function Ingredients() {
  const [selectedIngredient, setSelectedIngredient] = useState(null);
  const [ingredients, setIngredients] = useState([]); // State to store ingredient search results
  const [loading, setLoading] = useState(false); // Loading state for search results
  const [activeTab, setActiveTab] = useState("search");
  const [offset, setOffset] = useState(0);

  // Function to handle search
  const handleSearch = async (
    searchText = "",
    selectedDiets,
    selectedIntolerances = [],
    sortOption = "",
    sortDirection = "",
    newOffset = 0
  ) => {
    if (activeTab !== "search") return;
    setLoading(true);
    try {
      const response = await axios_api.get(`/search/ingredients`, {
        params: {
          query: searchText,
          intolerances: selectedIntolerances.join(","),
          sort: sortOption,
          sortDirection: sortDirection,
          number: 12,
          offset: newOffset,
        }
      });

      // Fetch detailed data for each ingredient by its ID
      const ingredientDetailsPromises = response.data.results.map(async (ingredient) => {
        const ingredientResponse = await axios_api.get(`/ingredients/${ingredient.id}`, {
          params: { amount: 10, unit: "g" },
          noAuth: true
        });
        return ingredientResponse.data; // Return the detailed ingredient data
      });

      // Wait for all API calls to complete
      const fullIngredients = await Promise.all(ingredientDetailsPromises);

      // Update state with the full ingredient data
      if (newOffset === 0) {
        setIngredients(fullIngredients);
      } else {
        setIngredients((prevIngredients) => [...prevIngredients, ...fullIngredients]); // Append to the list
      }
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
      const response = await axios_api.get(`/user/ingredients/update`, {
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
    setOffset(0);
  };

  // Fetch ingredients when activeTab changes
  useEffect(() => {
    if (activeTab === "search") {
      handleSearch(""); // Trigger search with an empty term
    } else if (activeTab === "saved") {
      fetchSavedIngredients();
    }
  }, [activeTab]);

  // See more results
  const handleSeeMore = () => {
    const newOffset = offset + 12;
    setOffset(newOffset);
    handleSearch("", [], [], "", "", newOffset);
  };

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
          {ingredients.map((ingredient, index) => (
            <Col key={index} xs={12} sm={6} md={4} lg={2} xl={2}>
              <IngredientCard {...ingredient} onClick={() => setSelectedIngredient(ingredient)} />
            </Col>
          ))}
        </Row>
        {activeTab === "search" && (
          <div className="d-flex justify-content-center mt-4">
            {loading ? (
              <div>Loading...</div> // Show Loading... in place of the button
            ) : (
              <Button variant="primary" onClick={handleSeeMore}>
                See more results
              </Button>
            )}
          </div>
        )}
      </Container>

      {selectedIngredient && (
        <IngredientPopup ingredient={selectedIngredient} onClose={() => setSelectedIngredient(null)} />
      )}
    </div>
  );
}

export default Ingredients;