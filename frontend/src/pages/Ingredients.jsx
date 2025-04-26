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
  const [query, setQuery] = useState(""); // State to store the search query
  const [selectedIntolerances, setSelectedIntolerances] = useState([]); // State to store selected intolerances
  const [sortOption, setSortOption] = useState(""); // State to store selected sort option
  const [sortDirection, setSortDirection] = useState(""); // State to store selected sort direction
  const [ingredients, setIngredients] = useState([]); // State to store ingredient search results
  const [loading, setLoading] = useState(false); // Loading state for search results
  const [activeTab, setActiveTab] = useState("search");
  const [offset, setOffset] = useState(0);
  const [noMoreResultsMessage, setNoMoreResultsMessage] = useState(""); // State to store "No more results" message

  // Function to handle search
  const handleSearch = async (
    searchText = "",
    selectedDiets,
    selectedIntolerances = [],
    sortOption = "",
    sortDirection = "",
    calorieLimit,
    newOffset = 0
  ) => {

    console.log("Page - Intolerances:", selectedIntolerances);
    if (activeTab !== "search") return;

    if (newOffset === 0) {
      setIngredients([]);
      setLoading(true);
    } else {
      setLoading(true);
    }

    console.log("Query Params:", {
      query: searchText,
      intolerances: selectedIntolerances.join(","),
      sort: sortOption,
      sortDirection: sortDirection,
      number: 12,
      offset: newOffset,
    });
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

      // Handle "No more results" and "No results found" cases
      if (response.data.totalResults === 0) {
        setNoMoreResultsMessage("No results found for this query");
      } else if (response.data.results.length < 12) {
        setNoMoreResultsMessage("No more results");
      } else {
        setNoMoreResultsMessage(""); // Reset message if there are more results
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
    setIngredients([]);
    setLoading(true);
  };

  const handleFilterChange = ({ query, intolerances, sortOption, sortDirection }) => {
    setQuery(query || "");
    setSelectedIntolerances(intolerances || []);
    setSortOption(sortOption || "");
    setSortDirection(sortDirection || "");
    setOffset(0);

    console.log("Updated filters:", {
      intolerances,
    });
  };

  useEffect(() => {
    if (activeTab === "saved") {
      fetchSavedIngredients();
    }
  }, [activeTab]);

  // See more results
  const handleSeeMore = () => {
    const newOffset = offset + 12;
    setOffset(newOffset);
    handleSearch(query, [], selectedIntolerances, sortOption, sortDirection, "", newOffset);
  };

  return (
    <div className="Ingredients">
      <Navigationbar />
      <SubNavbar
        pageTitle="Ingredients"
        onSearch={handleSearch}
        activeTab={activeTab}
        onTabChange={handleTabChange}
        onFilterChange={handleFilterChange}
        setLoading={setLoading}
      />

      <Container fluid className="pt-4" style={{ maxHeight: "calc(100vh - 180px)", overflowY: "auto" }}>
        {activeTab === "saved" ? (
          loading ? (
            <div className="d-flex justify-content-center align-items-center" style={{ height: "100%" }}>
              <p className="text-center text-muted">Loading...</p>
            </div>
          ) : ingredients.length === 0 ? (
            <div className="d-flex justify-content-center align-items-center" style={{ height: "100%" }}>
              <p className="text-center text-muted">
                No saved ingredients yet! Press <strong>+</strong> on an ingredient to save it here.
              </p>
            </div>
          ) : (
            <Row>
              {ingredients.map((ingredient, index) => (
                <Col key={index} xs={12} sm={6} md={4} lg={2} xl={2}>
                  <IngredientCard {...ingredient} onClick={() => setSelectedIngredient(ingredient)} />
                </Col>
              ))}
            </Row>
          )
        ) : (
          <>
            <Row>
              {ingredients.map((ingredient, index) => (
                <Col key={index} xs={12} sm={6} md={4} lg={2} xl={2}>
                  <IngredientCard {...ingredient} onClick={() => setSelectedIngredient(ingredient)} />
                </Col>
              ))}
            </Row>
            <div className="d-flex justify-content-center mt-4">
              {loading ? (
                <div>Loading...</div> // Show Loading... in place of the button
              ) : noMoreResultsMessage ? (
                <div>{noMoreResultsMessage}</div> // Show the message
              ) : (
                <Button variant="primary" onClick={handleSeeMore}>
                  See more results
                </Button>
              )}
            </div>
          </>
        )}
      </Container>

      {selectedIngredient && (
        <IngredientPopup
          ingredient={selectedIngredient}
          onClose={() => setSelectedIngredient(null)}
          setIngredients={setIngredients}
        />
      )}
    </div>
  );
}

export default Ingredients;