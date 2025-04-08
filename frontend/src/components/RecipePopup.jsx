import React, { useEffect } from "react";
import { Card, Table, Button, Form, ListGroup } from "react-bootstrap";

const nutrientList = [
  "Calories", "Fat", "Saturated Fat", "Trans Fat", "Carbohydrates", "Protein", "Cholesterol",
  "Sodium", "Sugars", "Alcohol", "Fiber", "Caffein", "Manganese", "Potassium", "Magnesium",
  "Calcium", "Copper", "Zinc", "Phosphorus", "Fluoride", "Choline", "Iron", "Vitamin A", "Vitamin B1",
  "Vitamin B2", "Vitamin B3", "Vitamin B5", "Vitamin B6", "Vitamin B12", "Vitamin C", "Vitamin D",
  "Vitamin E", "Vitamin K", "Folate", "Folic Acid", "Iodine", "Selenium"
];

const indented = ["Saturated Fat", "Trans Fat"];

const RecipePopup = ({ recipe, onClose }) => {
  const {
    image,
    name,
    diets = [],
    intolerances = [],
    nutrition = {},
    ingredients = [],
    steps = [],
    recipeLink = "",
    servingSize = "",
    units = []
  } = recipe;

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
        <div className="popup-left p-3" style={{ flex: 1 }}>
          <img src={image} alt={name} className="img-fluid rounded mb-3" />
          <div>
            <a href={recipeLink} target="_blank" rel="noopener noreferrer" style={{ display: "block", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {recipeLink}
            </a>
          </div>
          <div><strong>Diets:</strong> {diets.join(", ")}</div>
          <div><strong>Intolerances:</strong> {intolerances.join(", ")}</div>
        </div>

        {/* Middle and Right Columns Container */}
        <div className="d-flex flex-row" style={{ flex: 2, padding: "1rem", display: "flex", height: "100%" }}>
          {/* Middle Column: Nutrition Table */}
          <div className="popup-nutrition" style={{ flex: 1, paddingRight: "10px", display: "flex", flexDirection: "column", marginBottom: "0", height: "100%" }}>
            <div className="d-flex justify-content-between align-items-start">
                <h3>{name}</h3>
            </div>

            <Form.Group className="d-flex gap-2 mt-3">
                <Form.Label className="pt-2">Serving Size:</Form.Label>
                <Form.Control type="text" defaultValue={servingSize} style={{ width: "80px" }} />
                <Form.Select style={{ width: "120px" }}>
                {units.map((u, idx) => <option key={idx}>{u}</option>)}
                </Form.Select>
            </Form.Group>

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
                        <td>{nutrition[nutrient]?.amount ?? "-----"}</td>
                        <td>{nutrition[nutrient]?.daily ?? "-----"}</td>
                    </tr>
                    ))}
                </tbody>
                </Table>
            </div>
            </div>


          {/* Right Column: Ingredients (top half) and Steps (bottom half) */}
          <div className="popup-details" style={{ flex: 1, paddingLeft: "20px", display: "flex", flexDirection: "column" }}>
            {/* Save + Close Buttons */}
            <div className="d-flex justify-content-end gap-2 mb-3">
              <Button variant="success">+</Button>
              <Button variant="outline-danger" onClick={onClose}>X</Button>
            </div>

            {/* Ingredients Section */}
            <div style={{ flex: 1, overflowY: "auto" }}>
              <strong>Ingredients – {ingredients.length}</strong>
              <ListGroup className="mb-3">
                {ingredients.map((ing, idx) => (
                  <ListGroup.Item key={idx} className="d-flex justify-content-between">
                    <span>{ing.saved ? "✅" : "⬜️"} {ing.name}</span>
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </div>

            {/* Recipe Steps Section */}
            <div style={{ flex: 1, overflowY: "auto", marginTop: "20px" }}>
              <strong>Steps:</strong>
              <ListGroup as="ol" numbered>
                {steps.map((step, idx) => (
                  <ListGroup.Item key={idx}>{step}</ListGroup.Item>
                ))}
              </ListGroup>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default RecipePopup;
