import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import IngredientCard from '../components/IngredientCard';
import IngredientPopup from "../components/IngredientPopup";
import { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css"

const sampleIngredient = [
  {
    image: "https://via.placeholder.com/300x150",
    name: "Broccoli",
    diets: ["Vegan", "Keto", "Paleo"],
    intolerances: ["Dairy", "Gluten"],
    servingSize: "100",
    units: ["g", "oz", "cup"],
    nutrition: {
      Calories: { amount: 55, daily: "3%" },
      Fat: { amount: 0.6, daily: "1%" },
      "Saturated Fat": { amount: 0.1, daily: "1%" },
      "Trans Fat": { amount: 0, daily: "0%" },
      Carbohydrates: { amount: 11, daily: "4%" },
      Protein: { amount: 3.7, daily: "7%" },
      Cholesterol: { amount: 0, daily: "0%" },
      Sodium: { amount: 30, daily: "1%" },
      Sugars: { amount: 2.2, daily: "4%" },
      Alcohol: { amount: 0, daily: "0%" },
      Fiber: { amount: 2.6, daily: "10%" },
      Caffein: { amount: 0, daily: "0%" },
      Manganese: { amount: 0.2, daily: "10%" },
      Potassium: { amount: 316, daily: "9%" },
      Magnesium: { amount: 21, daily: "5%" },
      Calcium: { amount: 47, daily: "5%" },
      Copper: { amount: 0.05, daily: "6%" },
      Zinc: { amount: 0.4, daily: "4%" },
      Phosphorus: { amount: 66, daily: "9%" },
      Fluoride: { amount: 1.1, daily: "3%" },
      Choline: { amount: 18.7, daily: "3%" },
      Iron: { amount: 0.7, daily: "4%" },
      "Vitamin A": { amount: 623, daily: "70%" },
      "Vitamin B1": { amount: 0.07, daily: "6%" },
      "Vitamin B2": { amount: 0.12, daily: "9%" },
      "Vitamin B3": { amount: 0.64, daily: "4%" },
      "Vitamin B5": { amount: 0.6, daily: "12%" },
      "Vitamin B6": { amount: 0.21, daily: "12%" },
      "Vitamin B12": { amount: 0, daily: "0%" },
      "Vitamin C": { amount: 89.2, daily: "149%" },
      "Vitamin D": { amount: 0, daily: "0%" },
      "Vitamin E": { amount: 0.78, daily: "5%" },
      "Vitamin K": { amount: 101.6, daily: "127%" },
      Folate: { amount: 63, daily: "16%" },
      "Folic Acid": { amount: 0, daily: "0%" },
      Iodine: { amount: 15, daily: "10%" },
      Selenium: { amount: 2.5, daily: "5%" }
    }
  }
];

const sample = sampleIngredient[0];

const ingredientList = Array.from({ length: 20 }, (_, index) => ({
  ...sample,
  name: `${sample.name} ${index + 1}`
}));

function Ingredients() {
  const [selectedIngredient, setSelectedIngredient] = useState(null);
    // HTML
    return (
    <div className="Ingredients">
      <Navigationbar />
      <SubNavbar pageTitle="Ingredients" />
      <Container fluid className="pt-4" style={{ maxHeight: "calc(100vh - 180px)", overflowY: "auto" }}>
        <Row>
          {ingredientList.map((ingredient, index) => (
            <Col key={index} xs={12} sm={6} md={4} lg={2} xl={2}>
              <IngredientCard {...ingredient} onClick={() => setSelectedIngredient(ingredient)} />
            </Col>
          ))}
        </Row>

        {selectedIngredient && (
        <IngredientPopup ingredient={selectedIngredient} onClose={() => setSelectedIngredient(null)} />
        )}
      </Container>
    </div>
    );
}

export default Ingredients;