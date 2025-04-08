import React, { useState } from "react";
import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import RecipeCard from '../components/RecipeCard';
import RecipePopup from "../components/RecipePopup";
import { Container, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css";

// Sample recipe object
const sampleRecipe = {
  image: "https://via.placeholder.com/300x150", // Replace with actual recipe image URL
  name: "Sample Recipe: Vegan Buddha Bowl",
  recipeLink: "https://www.example.com/recipe", // Replace with actual recipe link
  diets: ["Vegan", "Gluten-Free", "High-Protein", "Low-Carb"],
  intolerances: ["Nuts", "Soy"],
  servingSize: "1 bowl",
  units: ["bowl", "plate", "cup"],
  nutrition: {
    Calories: { amount: 350, daily: "18%" },
    Fat: { amount: 15, daily: "23%" },
    "Saturated Fat": { amount: 3, daily: "15%" },
    "Trans Fat": { amount: 0, daily: "0%" },
    Carbohydrates: { amount: 40, daily: "13%" },
    Protein: { amount: 10, daily: "20%" },
    Cholesterol: { amount: 0, daily: "0%" },
    Sodium: { amount: 400, daily: "17%" },
    Sugars: { amount: 5, daily: "6%" },
    Alcohol: { amount: 0, daily: "0%" },
    Fiber: { amount: 7, daily: "28%" },
    Caffein: { amount: 0, daily: "0%" },
    Manganese: { amount: 2, daily: "100%" },
    Potassium: { amount: 500, daily: "14%" },
    Magnesium: { amount: 50, daily: "12%" },
    Calcium: { amount: 150, daily: "15%" },
    Copper: { amount: 0.5, daily: "56%" },
    Zinc: { amount: 1.2, daily: "11%" },
    Phosphorus: { amount: 200, daily: "20%" },
    Fluoride: { amount: 0, daily: "0%" },
    Choline: { amount: 20, daily: "4%" },
    Iron: { amount: 3, daily: "17%" },
    "Vitamin A": { amount: 500, daily: "56%" },
    "Vitamin B1": { amount: 0.1, daily: "8%" },
    "Vitamin B2": { amount: 0.1, daily: "7%" },
    "Vitamin B3": { amount: 2, daily: "12%" },
    "Vitamin B5": { amount: 1, daily: "20%" },
    "Vitamin B6": { amount: 0.3, daily: "18%" },
    "Vitamin B12": { amount: 0, daily: "0%" },
    "Vitamin C": { amount: 30, daily: "50%" },
    "Vitamin D": { amount: 0, daily: "0%" },
    "Vitamin E": { amount: 4, daily: "10%" },
    "Vitamin K": { amount: 20, daily: "25%" },
    Folate: { amount: 100, daily: "40%" },
    "Folic Acid": { amount: 0, daily: "0%" },
    Iodine: { amount: 15, daily: "10%" },
    Selenium: { amount: 0.5, daily: "5%" },
  },
  ingredients: [
    { name: "Quinoa", saved: false },
    { name: "Chickpeas", saved: true },
    { name: "Spinach", saved: false },
    { name: "Avocado", saved: true },
    { name: "Carrot", saved: false },
    { name: "Cucumber", saved: false },
    { name: "Tahini", saved: false },
    { name: "Lemon Juice", saved: false },
  ],
  steps: [
    "Cook the quinoa according to package instructions.",
    "In a bowl, combine the chickpeas, spinach, and chopped vegetables (avocado, carrot, cucumber).",
    "For the dressing, mix tahini with lemon juice and a little water to thin it out.",
    "Assemble the bowl by layering the quinoa, vegetable mix, and drizzle with tahini dressing.",
    "Top with additional lemon juice, salt, and pepper to taste.",
    "Serve and enjoy your vegan Buddha bowl!"
  ]
};


// Generate list of 20 sample recipes
const recipeList = Array.from({ length: 20 }, (_, index) => ({
  ...sampleRecipe,
  name: `${sampleRecipe.name} ${index + 1}`,
  recipeLink: `${sampleRecipe.recipeLink}?id=${index + 1}`
}));

function Recipes() {
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  return (
    <div className="Recipes">
      <Navigationbar />
      <SubNavbar pageTitle="Recipes" />
      <Container fluid className="pt-4" style={{ maxHeight: "calc(100vh - 180px)", overflowY: "auto" }}>
        <Row>
          {recipeList.map((recipe, index) => (
            <Col key={index} xs={12} md={6} lg={4}>
              <RecipeCard {...recipe} onClick={() => setSelectedRecipe(recipe)} />
            </Col>
          ))}
        </Row>
      </Container>

      {selectedRecipe && (
        <RecipePopup recipe={selectedRecipe} onClose={() => setSelectedRecipe(null)} />
      )}
    </div>
  );
}

export default Recipes;