import React, { useState, useEffect } from "react";
import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import RecipeCard from '../components/RecipeCard';
import RecipePopup from "../components/RecipePopup";
import { Container, Row, Col, Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css";
import axios_api from "../utils/axiosInstance";

function Recipes() {
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [selectedDiets, setSelectedDiets] = useState([]);
  const [recipes, setRecipes] = useState([]); // State to store recipe search results
  const [loading, setLoading] = useState(false); // Loading state for search results
  const [activeTab, setActiveTab] = useState("search");
  const [offset, setOffset] = useState(0);

  // Function to fetch user ingredients
  const fetchUserIngredients = async () => {
    try {
      const response = await axios_api.get(`/user/ingredients/update`);
      return response.data.ingredients.map((ingredient) => ingredient.name);
    } catch (error) {
      console.error("Error fetching user ingredients:", error);
      return [];
    }
  };

  const handleFilterChange = (updatedDiets) => {
    setSelectedDiets(updatedDiets); // Update selected diets
  };

  // Function to handle search
  const handleSearch = async (
    searchText = "",
    selectedDiets = [],
    selectedIntolerances = [],
    sortOption = "",
    sortDirection = "",
    newOffset = 0,
  ) => {
    setLoading(true);

    let includeIngredients = [];

    if (sortOption === "max-used-ingredients" || sortOption === "min-missing-ingredients") {
      const ingredients = await fetchUserIngredients();
      includeIngredients = ingredients.join(",");
    }

    try {
      const response = await axios_api.get(`/search/recipes`, {
        params: {
          query: searchText,
          diet: selectedDiets.join(","),
          intolerances: selectedIntolerances.join(","),
          sort: sortOption,
          sortDirection: sortDirection,
          includeIngredients: includeIngredients,
          fillIngredients: true,
          addRecipeNutrition: true,
          addRecipeInstructions: true,
          number: 12,
          offset: newOffset,
        }
      });
      if (newOffset === 0) {
        setRecipes(response.data.results);
      } else {
        setRecipes((prevRecipes) => [...prevRecipes, ...response.data.results]); // Append to the list
      }
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
      const response = await axios_api.get(`/user/recipes/update`);
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
    setOffset(0);
    setRecipes([]);
    setLoading(true);
  };

  // Fetch recipes when activeTab changes
  useEffect(() => {
    if (activeTab === "search") {
      handleSearch(""); // Trigger search with an empty term
    } else if (activeTab === "saved") {
      fetchSavedRecipes();
    }
  }, [activeTab]);

  // See more results
  const handleSeeMore = () => {
    const newOffset = offset + 12;
    setOffset(newOffset);
    handleSearch("", selectedDiets, [], "", "", newOffset);
  };

  return (
    <div className="Recipes">
      <Navigationbar />
      <SubNavbar
        pageTitle="Recipes"
        onSearch={handleSearch}
        activeTab={activeTab}
        onTabChange={handleTabChange}
        onFilterChange={handleFilterChange}
      />

      <Container fluid className="pt-4" style={{ maxHeight: "calc(100vh - 180px)", overflowY: "auto" }}>
        {activeTab === "saved" ? (
          loading ? (
            <div className="d-flex justify-content-center align-items-center" style={{ height: "100%" }}>
              <p className="text-center text-muted">Loading...</p>
            </div>
          ) : recipes.length === 0 ? (
            <div className="d-flex justify-content-center align-items-center" style={{ height: "100%" }}>
              <p className="text-center text-muted">
                No saved recipes yet! Press <strong>+</strong> on a recipe to save it here.
              </p>
            </div>
          ) : (
            <Row>
              {recipes.map((recipe, index) => (
                <Col key={index} xs={12} md={6} lg={4}>
                  <RecipeCard
                    {...recipe}
                    usedIngredients={recipe.usedIngredients}
                    selectedDiets={selectedDiets}
                    onClick={() => setSelectedRecipe(recipe)}
                  />
                </Col>
              ))}
            </Row>
          )
        ) : (
          <>
            <Row>
              {recipes.map((recipe, index) => (
                <Col key={index} xs={12} md={6} lg={4}>
                  <RecipeCard
                    {...recipe}
                    usedIngredients={recipe.usedIngredients}
                    selectedDiets={selectedDiets}
                    onClick={() => setSelectedRecipe(recipe)}
                  />
                </Col>
              ))}
            </Row>
            <div className="d-flex justify-content-center mt-4">
              {loading ? (
                <div>Loading...</div> // Show Loading... in place of the button
              ) : (
                <Button variant="primary" onClick={handleSeeMore}>
                  See more results
                </Button>
              )}
            </div>
          </>
        )}
      </Container>

      {selectedRecipe && (
        <RecipePopup
          recipe={selectedRecipe}
          onClose={() => setSelectedRecipe(null)}
          selectedDiets={selectedDiets} // Pass selected diets
          usedIngredients={selectedRecipe.usedIngredients || []} // Pass used ingredients
        />
      )}
    </div>
  );
}

export default Recipes;