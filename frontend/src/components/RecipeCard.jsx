import React from "react";
import { Card, Table } from "react-bootstrap";
import "./RecipeCard.css";

const RecipeCard = ({
  image,
  title,
  sourceUrl,
  nutrition = { nutrients: [], ingredients: [] },
  diets = [],
  onClick
}) => {
  const nutritionValues = {
    calories: nutrition.nutrients.find(nutrient => nutrient.name === "Calories"),
    fat: nutrition.nutrients.find(nutrient => nutrient.name === "Fat"),
    carbs: nutrition.nutrients.find(nutrient => nutrient.name === "Carbohydrates"),
    protein: nutrition.nutrients.find(nutrient => nutrient.name === "Protein")
  };

  return (
    <Card className="mb-3 d-flex flex-row" style={{ height: "350px" }} onClick={onClick}>
      {/* Left side: Image, Link, Diets */}
      <div style={{ width: "30%", minWidth: "200px" }} className="p-2 d-flex flex-column justify-content-between">
        <img src={image} alt={title} className="img-fluid rounded" style={{ objectFit: "cover", height: "150px" }} />

        {/* Recipe Link */}
        <a href={sourceUrl} className="text-truncate d-block mt-2" title={sourceUrl} target="_blank" rel="noopener noreferrer">
          {sourceUrl}
        </a>

        {/* Diet Alignments */}
        <div className="mt-1">
          <strong>Diets:</strong>
          <ul className="mb-0 ps-3">
            {diets.map((diet, idx) => (
              <li key={idx}><span className="text-success">✅</span> {diet}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Right side: Title, Nutrition, Ingredients */}
      <Card.Body className="d-flex flex-column" style={{ overflow: "hidden" }}>
        <div>
          <Card.Title>{title}</Card.Title>

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
        </div>

        {/* Ingredients */}
        <div style={{ overflow: "hidden", flexShrink: 0 }}>
          <strong>Ingredients – {nutrition.ingredients.length}</strong>
          <ul className="mb-0 ps-3">
            {nutrition.ingredients.slice(0, 3).map((ing, idx) => (
              <li key={idx}>
                {ing.saved ? "✅" : "⬜️"} {ing.name}
              </li>
            ))}
            {nutrition.ingredients.length > 3 && <li>...</li>}
          </ul>
        </div>
      </Card.Body>
    </Card>
  );
};

export default RecipeCard;
