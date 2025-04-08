import React, { useState } from "react";
import Navigationbar from "../components/Navbar";
import { Form, Card, Container, Button, Dropdown } from "react-bootstrap";
import "./Color.css";

const dietOptions = [
  "Gluten Free", "Ketogenic", "Vegetarian", "Lacto-vegetarian", "Ovo-vegetarian",
  "Vegan", "Pescetarian", "Paleo", "Primal", "Low fodmap", "Whole30"
];

const intoleranceOptions = [
  "Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood",
  "Sesame", "Shellfish", "Soy", "Sulfite", "Tree nut", "Wheat"
];

const PreferenceList = ({ title, options, selected, onAdd, onRemove }) => {
  const availableOptions = options.filter((opt) => !selected.includes(opt));

  return (
    <div className="mb-4">
      <h6>{title}</h6>
      <ul className="list-group mb-2">
        {selected.map((item) => (
          <li
            key={item}
            className="list-group-item d-flex justify-content-between align-items-center"
          >
            {item}
            <Button
              variant="outline-danger"
              size="sm"
              onClick={() => onRemove(item)}
            >
              ×
            </Button>
          </li>
        ))}
      </ul>
      {availableOptions.length > 0 && (
        <Dropdown>
          <Dropdown.Toggle variant="secondary" size="sm">
            Add {title.slice(0, -1)}
          </Dropdown.Toggle>
          <Dropdown.Menu>
            {availableOptions.map((opt) => (
              <Dropdown.Item key={opt} onClick={() => onAdd(opt)}>
                {opt}
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
      )}
    </div>
  );
};

const Profile = () => {
  const [selectedDiets, setSelectedDiets] = useState([]);
  const [selectedIntolerances, setSelectedIntolerances] = useState([]);
  const [calorieLimit, setCalorieLimit] = useState("");

  const handleAddDiet = (diet) => setSelectedDiets((prev) => [...prev, diet]);
  const handleRemoveDiet = (diet) =>
    setSelectedDiets((prev) => prev.filter((d) => d !== diet));

  const handleAddIntolerance = (item) =>
    setSelectedIntolerances((prev) => [...prev, item]);
  const handleRemoveIntolerance = (item) =>
    setSelectedIntolerances((prev) => prev.filter((i) => i !== item));

  const handleCalorieChange = (e) => {
    const value = e.target.value;
    if (/^\d{0,4}$/.test(value)) {
      setCalorieLimit(value);
    }
  };

  return (
    <>
      <Navigationbar />
      <Container className="d-flex justify-content-center align-items-start pt-5" style={{ minHeight: "100vh" }}>
        <Card style={{ width: "100%", maxWidth: "500px" }} className="p-4 shadow mt-5">
          <h3 className="text-center mb-3">Profile</h3>
          <h5 className="mb-4">User Preferences</h5>

          <PreferenceList
            title="Diets"
            options={dietOptions}
            selected={selectedDiets}
            onAdd={handleAddDiet}
            onRemove={handleRemoveDiet}
          />

          <PreferenceList
            title="Intolerances"
            options={intoleranceOptions}
            selected={selectedIntolerances}
            onAdd={handleAddIntolerance}
            onRemove={handleRemoveIntolerance}
          />

          <Form.Group controlId="calorieLimit">
            <Form.Label>Calorie Limit:</Form.Label>
            <Form.Control
              type="number"
              min="0"
              max="9999"
              value={calorieLimit}
              onChange={handleCalorieChange}
              placeholder="Enter calorie limit"
            />
          </Form.Group>
        </Card>
      </Container>
    </>
  );
};

export default Profile;
