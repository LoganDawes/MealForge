import React from "react";
import { Card, Table } from "react-bootstrap";
import "./RecipeCard.css";

const RecipeCard = ({
  image,
  name,
  recipeLink,
  nutrition = {},
  ingredients = [],
  diets = [],
  onClick
}) => {
  return (
    <Card className="mb-3 d-flex flex-row" style={{ height: "350px" }} onClick={onClick}>
      {/* Left side: Image, Link, Diets */}
      <div style={{ width: "30%", minWidth: "200px" }} className="p-2 d-flex flex-column justify-content-between">
        <img src={image} alt={name} className="img-fluid rounded" style={{ objectFit: "cover", height: "150px" }} />
        
        {/* Recipe Link */}
        <a href={recipeLink} className="text-truncate d-block mt-2" title={recipeLink} target="_blank" rel="noopener noreferrer">
          {recipeLink}
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

      {/* Right side: Name, Nutrition, Ingredients */}
      <Card.Body className="d-flex flex-column" style={{ overflow: "hidden" }}>
        <div>
          <Card.Title>{name}</Card.Title>

          <Table size="sm" className="mb-2">
                    <thead>
                      <tr>
                        <th>Macro</th>
                        <th>Amount</th>
                        <th>% Daily</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Calories</td>
                        <td>{nutrition?.Calories?.amount ?? "-----"}</td>
                        <td>{nutrition?.Calories?.daily ?? "-----"}</td>
                      </tr>
                      <tr>
                        <td>Fat</td>
                        <td>{nutrition?.Fat?.amount ?? "-----"}g</td>
                        <td>{nutrition?.Fat?.daily ?? "-----"}</td>
                      </tr>
                      <tr>
                        <td>Carbs</td>
                        <td>{nutrition?.Carbohydrates?.amount ?? "-----"}g</td>
                        <td>{nutrition?.Carbohydrates?.daily ?? "-----"}</td>
                      </tr>
                      <tr>
                        <td>Protein</td>
                        <td>{nutrition?.Protein?.amount ?? "-----"}g</td>
                        <td>{nutrition?.Protein?.daily ?? "-----"}</td>
                      </tr>
                    </tbody>
                  </Table>
        </div>

        {/* Ingredients */}
        <div style={{ overflow: "hidden", flexShrink: 0 }}>
        <strong>Ingredients – {ingredients.length}</strong>
        <ul className="mb-0 ps-3">
            {ingredients.slice(0, 3).map((ing, idx) => (
            <li key={idx}>
                {ing.saved ? "✅" : "⬜️"} {ing.name}
            </li>
            ))}
            {ingredients.length > 3 && <li>...</li>}
        </ul>
        </div>
      </Card.Body>
    </Card>
  );
};

export default RecipeCard;
