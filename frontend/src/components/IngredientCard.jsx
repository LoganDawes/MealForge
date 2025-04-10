import React from "react";
import { Card, Table } from "react-bootstrap";
import "./IngredientCard.css";

const IngredientCard = ({ image, name, nutrition = {}, diets = [], onClick }) => {
  return (
    <Card className="mb-3" style={{ width: '18rem', cursor: 'pointer' }} onClick={onClick}>
      {/* Image */}
      <Card.Img variant="top" src={image} alt={name} />

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

        <hr />

        {/* Diet Alignments */}
        <div>
          <strong>Diets:</strong>
          <ul className="mb-0 ps-3">
            {diets.map((diet, idx) => (
              <li key={idx}>
                <span className="text-success">✅ </span> {diet}
              </li>
            ))}
          </ul>
        </div>
      </Card.Body>
    </Card>
  );
};

export default IngredientCard;
