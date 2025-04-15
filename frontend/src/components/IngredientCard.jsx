import React from "react";
import { Card, Table } from "react-bootstrap";
import "./IngredientCard.css";

const IngredientCard = ({ image, name, nutrition = { nutrients: [] }, onClick }) => {
  const imageUrl = image ? `https://img.spoonacular.com/ingredients_100x100/${image}` : '';

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
        style={{ objectFit: "contain", height: "150px", width: "100%" }}
      />

      <Card.Body>
        {/* Name */}
        <Card.Title>{name}</Card.Title>

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
