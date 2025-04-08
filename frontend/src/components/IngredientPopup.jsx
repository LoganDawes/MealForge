import React, { useEffect } from "react";
import { Card, Table, Button, Form } from "react-bootstrap";
import "./IngredientPopup.css";

const nutrientList = [
  "Calories", "Fat", "Saturated Fat", "Trans Fat", "Carbohydrates", "Protein", "Cholesterol",
  "Sodium", "Sugars", "Alcohol", "Fiber", "Caffein", "Manganese", "Potassium", "Magnesium",
  "Calcium", "Copper", "Zinc", "Phosphorus", "Fluoride", "Choline", "Iron", "Vitamin A", "Vitamin B1",
  "Vitamin B2", "Vitamin B3", "Vitamin B5", "Vitamin B6", "Vitamin B12", "Vitamin C", "Vitamin D",
  "Vitamin E", "Vitamin K", "Folate", "Folic Acid", "Iodine", "Selenium"
];

const indented = ["Saturated Fat", "Trans Fat"];

const IngredientPopup = ({ ingredient, onClose }) => {
  const { image, name, diets = [], intolerances = [], nutrition = {}, servingSize = "", units = [] } = ingredient;

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
      <Card className="popup-card d-flex flex-row">
        {/* Left: Image + Info */}
        <div className="popup-left p-3">
          <img src={image} alt={name} className="img-fluid rounded mb-3" />
          <div><strong>Diets:</strong> {diets.join(", ")}</div>
          <div><strong>Intolerances:</strong> {intolerances.join(", ")}</div>
        </div>

        {/* Right: Details */}
        <Card.Body className="popup-right">
          <div className="d-flex justify-content-between align-items-start">
            <h3>{name}</h3>
            <div className="d-flex align-items-center gap-2">
              <Button variant="success">+</Button>
              <Button variant="outline-danger" onClick={onClose}>X</Button>
            </div>
          </div>

          <Form.Group className="d-flex gap-2 mt-3">
            <Form.Label className="pt-2">Serving Size:</Form.Label>
            <Form.Control type="text" defaultValue={servingSize} style={{ width: "80px" }} />
            <Form.Select style={{ width: "120px" }}>
              {units.map((u, idx) => <option key={idx}>{u}</option>)}
            </Form.Select>
          </Form.Group>

          <div className="table-scroll mt-3">
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
                    <td>{nutrition[nutrient]?.amount ?? "-----"}</td>
                    <td>{nutrition[nutrient]?.daily ?? "-----"}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
};

export default IngredientPopup;
