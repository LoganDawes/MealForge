import React from "react";
import { Card, Table } from "react-bootstrap";
import "./IngredientCard.css";
import baseImage from "../assets/mealforge-ingredients-image.png";

const capitalizeFirstLetter = (string) => {
  if (!string) return "";
  return string.charAt(0).toUpperCase() + string.slice(1);
};

const IngredientCard = ({ image, name, nutrition = { nutrients: [] }, onClick }) => {
  console.log("IngredientCard :", { name, image });
  const imageUrl = image
    ? `https://img.spoonacular.com/ingredients_100x100/${image}`
    : baseImage;

  const handleImageError = (event) => {
    event.target.src = baseImage;
    event.target.style.filter = "blur(1px)";
  };

  const nutritionValues = {
    calories: nutrition.nutrients.find(nutrient => nutrient.name === "Calories"),
    fat: nutrition.nutrients.find(nutrient => nutrient.name === "Fat"),
    carbs: nutrition.nutrients.find(nutrient => nutrient.name === "Carbohydrates"),
    protein: nutrition.nutrients.find(nutrient => nutrient.name === "Protein")
  };

  return (
    <Card className="mb-3" style={{ width: '18rem', cursor: 'pointer' }} onClick={onClick}>
      {/* Image */}
      <Card.Img
        variant="top"
        src={imageUrl}
        alt={name}
        className="img-fluid rounded"
        style={{
          objectFit: "contain",
          height: "150px",
          width: "100%",
          filter: image ? "none" : "blur(1px)",
        }}
        onError={handleImageError}
      />

      <Card.Body>
        {/* Name */}
        <Card.Title>{capitalizeFirstLetter(name)}</Card.Title>

        {/* Nutrition Table */}
        <Table size="sm" className="mb-2">
          <thead>
            <tr>
              <th>Name</th>
              <th>Amount</th>
              <th>% Daily</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Calories</td>
              <td>{nutritionValues.calories?.amount ?? "-----"}</td>
              <td>{nutritionValues.calories?.percentOfDailyNeeds ?? "-----"}%</td>
            </tr>
            <tr>
              <td>Fat</td>
              <td>{nutritionValues.fat?.amount ?? "-----"}g</td>
              <td>{nutritionValues.fat?.percentOfDailyNeeds ?? "-----"}%</td>
            </tr>
            <tr>
              <td>Carbs</td>
              <td>{nutritionValues.carbs?.amount ?? "-----"}g</td>
              <td>{nutritionValues.carbs?.percentOfDailyNeeds ?? "-----"}%</td>
            </tr>
            <tr>
              <td>Protein</td>
              <td>{nutritionValues.protein?.amount ?? "-----"}g</td>
              <td>{nutritionValues.protein?.percentOfDailyNeeds ?? "-----"}%</td>
            </tr>
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  );
};

export default IngredientCard;
