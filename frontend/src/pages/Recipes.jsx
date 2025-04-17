import React, { useState, useEffect } from "react";
import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import RecipeCard from '../components/RecipeCard';
import RecipePopup from "../components/RecipePopup";
import { Container, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css";
import axios_api from "../utils/axiosInstance";

function Recipes() {
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [selectedDiets, setSelectedDiets] = useState([]);
  const [recipes, setRecipes] = useState([]); // State to store recipe search results
  const [loading, setLoading] = useState(false); // Loading state for search results
  const [activeTab, setActiveTab] = useState("search");

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
    sortDirection = ""
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
        onFilterChange={handleFilterChange}
      />

      <Container fluid className="pt-4" style={{ maxHeight: "calc(100vh - 180px)", overflowY: "auto" }}>
        <Row>
          {loading ? (
            <div>Loading...</div>
          ) : (
            recipes.map((recipe, index) => (
              <Col key={index} xs={12} md={6} lg={4}>
                <RecipeCard {...recipe}
                  usedIngredients={recipe.usedIngredients}
                  selectedDiets={selectedDiets}
                  onClick={() => setSelectedRecipe(recipe)} />
              </Col>
            ))
          )}
        </Row>
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