import React, { useEffect, useState } from "react";
import { Card, Table, Button, Form } from "react-bootstrap";
import axios from "axios";
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
  const [amount, setAmount] = useState(ingredient.amount || 1);
  const [unit, setUnit] = useState(ingredient.unit || "unit");
  const [nutrition, setNutrition] = useState(ingredient.nutrition || { nutrients: [] });

  const imageUrl = ingredient.image ? `https://img.spoonacular.com/ingredients_100x100/${ingredient.image}` : '';

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (e.target.classList.contains("popup-overlay")) onClose();
    };
    window.addEventListener("click", handleClickOutside);
    return () => window.removeEventListener("click", handleClickOutside);
  }, [onClose]);

  // Fetch updated nutrition when amount or unit changes
  useEffect(() => {
    const fetchNutrition = async () => {
      try {
        const res = await axios.get(`/api/ingredients/${ingredient.id}`, {
          params: { amount, unit }
        });
        setNutrition(res.data.nutrition);
      } catch (err) {
        console.error("Failed to fetch updated nutrition:", err);
      }
    };

    fetchNutrition();
  }, [amount, unit, ingredient.id]);

  return (
    <div className="popup-overlay">
      <Card className="popup-card d-flex flex-row">
        {/* Left: Image + Info */}
        <div className="popup-left">
          <img src={imageUrl} alt={ingredient.name} />
        </div>

        {/* Right: Details */}
        <Card.Body className="popup-right">
          <div className="d-flex justify-content-between align-items-start">
            <h3>{ingredient.name}</h3>
            <div className="d-flex align-items-center gap-2">
              <Button variant="success">+</Button>
              <Button variant="outline-danger" onClick={onClose}>X</Button>
            </div>
          </div>

          <Form.Group className="d-flex gap-2 mt-3">
            <Form.Label className="pt-2">Unit:</Form.Label>
            <Form.Control
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              style={{ width: "80px" }}
            />
            <Form.Select
              style={{ width: "120px" }}
              value={unit}
              onChange={(e) => setUnit(e.target.value)}
            >
              {ingredient.possibleUnits.map((u, idx) => (
                <option key={idx} value={u}>{u}</option>
              ))}
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
                {nutrientList.map((nutrient, idx) => {
                  const data = nutrition.nutrients.find(n => n.name === nutrient);
                  return (
                    <tr key={idx}>
                      <td className={indented.includes(nutrient) ? "ps-4" : ""}>{nutrient}</td>
                      <td>{data?.amount ?? "-----"}</td>
                      <td>{data?.percentOfDailyNeeds ?? "-----"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
};

export default IngredientPopup;
