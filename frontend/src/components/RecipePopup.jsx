import React, { useEffect, useState } from "react";
import { Card, Table, Button, Form, ListGroup } from "react-bootstrap";
import IngredientPopup from "../components/IngredientPopup";
import StepsPopup from "./StepsPopup";
import axios_api from "../utils/axiosInstance";
import baseImage from "../assets/mealforge-recipes-image.png";

const nutrientList = [
  "Calories", "Fat", "Saturated Fat", "Trans Fat", "Carbohydrates", "Protein", "Cholesterol",
  "Sodium", "Sugars", "Alcohol", "Fiber", "Caffein", "Manganese", "Potassium", "Magnesium",
  "Calcium", "Copper", "Zinc", "Phosphorus", "Fluoride", "Choline", "Iron", "Vitamin A", "Vitamin B1",
  "Vitamin B2", "Vitamin B3", "Vitamin B5", "Vitamin B6", "Vitamin B12", "Vitamin C", "Vitamin D",
  "Vitamin E", "Vitamin K", "Folate", "Folic Acid", "Iodine", "Selenium"
];

const indented = ["Saturated Fat", "Trans Fat"];

const capitalizeFirstLetter = (string) => {
  if (!string) return "";
  return string.charAt(0).toUpperCase() + string.slice(1);
};

// Mapping function to normalize diets
const normalizeDiet = (diet) => {
  const dietMapping = {
    "gluten free": "Gluten Free",
    "ketogenic": "Ketogenic",
    "lacto ovo vegetarian": "Vegetarian",
    "vegan": "Vegan",
    "pescetarian": "Pescetarian",
    "paleolithic": "Paleo",
    "primal": "Primal",
    "fodmap friendly": "Low FODMAP",
    "whole 30": "Whole30"
  };
  return dietMapping[diet.toLowerCase()] || diet; // Default to original if no match
};

const RecipePopup = ({ recipe, onClose, setRecipes, selectedDiets = [], usedIngredients = [] }) => {
  const {
    id,
    image,
    title,
    sourceUrl,
    nutrition = { nutrients: [], ingredients: [] },
    diets = [],
    analyzedInstructions = [],
    servings = "",
  } = recipe;

  const [isSaved, setIsSaved] = useState(false);
  const [selectedIngredient, setSelectedIngredient] = useState(null);
  const [selectedStep, setSelectedStep] = useState(null);
  const [ingredientDetails, setIngredientDetails] = useState(null);

  const isLoggedIn = !!localStorage.getItem("accessToken");

  const imageUrl = image
    ? image
    : baseImage;

  const handleImageError = (event) => {
    event.target.src = baseImage;
    event.target.style.filter = "blur(1px)";
  };

  // Fetch ingredient details when an ingredient is selected
  useEffect(() => {
    const fetchIngredientDetails = async () => {
      console.log("Fetching ingredient details for:", selectedIngredient);
      if (!selectedIngredient) return;

      console.log(selectedIngredient.id);
      console.log(selectedIngredient.name);
      console.log(selectedIngredient.amount);
      console.log(selectedIngredient.unit);

      try {
        const ingredientResponse = await axios_api.get(`/ingredients/${selectedIngredient.id}`, {
          params: { amount: selectedIngredient.amount, unit: selectedIngredient.unit },
          noAuth: true,
        });
        console.log(ingredientResponse.data);
        setIngredientDetails(ingredientResponse.data); // Set fetched details
      } catch (error) {
        console.error("Error fetching ingredient details:", error);
      }
    };

    fetchIngredientDetails();
  }, [selectedIngredient]);

  // Normalize diets to match selectedDiets format
  const normalizedDiets = diets.map(normalizeDiet);

  // Sort diets: selectedDiets first
  const sortedDiets = [...normalizedDiets].sort((a, b) => {
    const aIsSelected = selectedDiets.includes(a);
    const bIsSelected = selectedDiets.includes(b);
    return bIsSelected - aIsSelected; // Selected diets come first
  });

  // Extract IDs of used ingredients for quick lookup
  const usedIngredientIds = usedIngredients.map((ingredient) => ingredient.id);

  // Function to save the recipe
  const handleSaveRecipe = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      alert("You must be logged in to save recipes.");
      return;
    }

    try {
      await axios_api.post(
        "/user/recipes/",
        { recipe },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      alert("Recipe saved successfully!");
      setIsSaved(true);

      setRecipes((prevRecipes) => {
        if (prevRecipes.some((savedRecipe) => savedRecipe.id === recipe.id)) {
          return prevRecipes;
        }
        return [...prevRecipes, recipe];
      });
    } catch (error) {
      console.error("Error saving recipe:", error);
      alert("Failed to save the recipe. Please try again.");
    }
  };

  // Function to remove the recipe
  const handleRemoveRecipe = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      alert("You must be logged in to remove recipes.");
      return;
    }

    try {
      await axios_api.delete(
        "/user/recipes/",
        {
          data: { recipe_id: id },
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      alert("Recipe removed successfully!");
      setIsSaved(false);

      setRecipes((prevRecipes) =>
        prevRecipes.filter((savedRecipe) => savedRecipe.id !== recipe.id)
      );
    } catch (error) {
      console.error("Error removing recipe:", error);
      alert("Failed to remove the recipe. Please try again.");
    }
  };

  useEffect(() => {
    const checkIfSaved = async () => {
      const token = localStorage.getItem("accessToken");
      if (!token) return;

      try {
        const response = await axios_api.get("/user/recipes/");

        // Check if the recipe ID exists in the saved recipes
        const savedRecipes = response.data.recipes || [];
        const isRecipeSaved = savedRecipes.some((savedRecipe) => savedRecipe.id === id);
        setIsSaved(isRecipeSaved); // Update state based on whether the recipe is saved
      } catch (error) {
        console.error("Error checking if recipe is saved:", error);
      }
    };

    checkIfSaved();
  }, [id]);

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (e.target.classList.contains("popup-overlay")) onClose();
    };
    window.addEventListener("click", handleClickOutside);
    return () => window.removeEventListener("click", handleClickOutside);
  }, [onClose]);

  return (
    <div className="popup-overlay">
      <Card className="popup-card d-flex flex-row" style={{ width: "90%", maxWidth: "1200px", height: "80vh" }}>
        {/* Left Column: Image + Info */}
        <div className="popup-left p-3" style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center" }}>
          {/* Image */}
          <img src={imageUrl} alt={title} className="img-fluid rounded mb-3" style={{ maxWidth: "100%", height: "auto" }} onError={handleImageError} />

          {/* Source Link */}
          <div className="mb-2" style={{ width: "100%", textAlign: "center" }}>
            <a href={sourceUrl} target="_blank" rel="noopener noreferrer" style={{ display: "block", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {sourceUrl}
            </a>
          </div>

          {/* Diets List */}
          <div style={{ width: "100%", textAlign: "center" }}>
            <strong>Diets:</strong>
            <ul className="mb-0 ps-3">
              {sortedDiets.map((diet, idx) => (
                <li key={idx}>
                  {selectedDiets.includes(diet) ? "✅" : "⬜️"} {diet}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Middle and Right Columns Container */}
        <div className="d-flex flex-row" style={{ flex: 2, padding: "1rem", display: "flex", height: "100%" }}>
          {/* Middle Column: Nutrition Table */}
          <div className="popup-nutrition" style={{ flex: 1, paddingRight: "10px", display: "flex", flexDirection: "column", marginBottom: "0", height: "100%" }}>
            <div className="d-flex justify-content-between align-items-start">
              <h3>{capitalizeFirstLetter(title)}</h3>
            </div>

            {/* Serving Size */}
            <div className="d-flex align-items-center gap-2 mt-3">
              <Form.Label className="mb-0">Serving Size:</Form.Label>
              <span>{servings}</span>
            </div>

            {/* Stretch the table container to fill available space */}
            <div className="table-scroll" style={{ minHeight: "600px", overflowY: "auto" }}>
              <Table striped bordered hover size="sm">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Amount</th>
                    <th>% Daily</th>
                  </tr>
                </thead>
                <tbody>
                  {nutrientList.map((nutrient, idx) => (
                    <tr key={idx}>
                      <td className={indented.includes(nutrient) ? "ps-4" : ""}>{nutrient}</td>
                      <td>{nutrition.nutrients.find(n => n.name === nutrient)?.amount ?? "-----"}</td>
                      <td>{nutrition.nutrients.find(n => n.name === nutrient)?.percentOfDailyNeeds ?? "-----"}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          </div>

          {/* Right Column: Ingredients (top half) and Steps (bottom half) */}
          <div className="popup-details" style={{ flex: 1, paddingLeft: "20px", display: "flex", flexDirection: "column" }}>
            {/* Save/Remove + Close Buttons */}
            <div className="d-flex justify-content-end gap-2 mb-3">
              {isLoggedIn && (
                isSaved ? (
                  <Button variant="danger" onClick={handleRemoveRecipe}>-</Button>
                ) : (
                  <Button variant="success" onClick={handleSaveRecipe}>+</Button>
                )
              )}
              <Button variant="outline-danger" onClick={onClose}>X</Button>
            </div>

            {/* Ingredients Section */}
            <div style={{ flex: 1, overflowY: "auto" }}>
              <strong>Ingredients – {nutrition.ingredients.length}</strong>
              <ListGroup className="mb-3">
                {nutrition.ingredients.map((ing, idx) => {
                  // Ensure the ingredient has the required properties
                  const ingredientData = {
                    id: ing.id,
                    name: ing.name,
                    amount: ing.amount || 10, // Default to 10 if amount is missing
                    unit: ing.unit || "g",   // Default to "g" if unit is missing
                  };

                  return (
                    <ListGroup.Item
                      key={idx}
                      className="d-flex justify-content-between"
                      onClick={() => {
                        console.log("Setting selected ingredient:", ingredientData); // Log the ingredient being set
                        setSelectedIngredient(ingredientData); // Set selected ingredient with proper structure
                      }}
                      style={{ cursor: "pointer" }} // Add pointer cursor for better UX
                    >
                      <span>
                        {usedIngredientIds.includes(ing.id) ? "✅" : "⬜️"} {ingredientData.amount}{" "}
                        {ingredientData.unit}{" "}
                        {ingredientData.name}
                      </span>
                    </ListGroup.Item>
                  );
                })}
              </ListGroup>
            </div>

            {/* Recipe Steps Section */}
            <div style={{ flex: 1, overflowY: "auto", marginTop: "20px" }}>
              <strong>Steps:</strong>
              <ListGroup as="ol" numbered>
                {analyzedInstructions[0]?.steps.map((step, idx) => (
                  <ListGroup.Item
                    key={idx}
                    onClick={() => setSelectedStep(step)}
                    style={{ cursor: "pointer" }}
                  >
                    {step.step}
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </div>
          </div>
        </div>
      </Card>

      {/* Render IngredientPopup if an ingredient is selected */}
      {ingredientDetails && (
        <IngredientPopup
          ingredient={ingredientDetails}
          onClose={() => {
            setSelectedIngredient(null); // Reset selectedIngredient
            setIngredientDetails(null); // Reset ingredientDetails
          }}
        />
      )}
      {/* Render StepsPopup if a step is selected */}
      {selectedStep && (
        <StepsPopup
          step={selectedStep}
          recipeIngredients={nutrition.ingredients} // Pass recipe ingredients
          onClose={() => setSelectedStep(null)} // Close StepsPopup
        />
      )}
    </div>
  );
};

export default RecipePopup;