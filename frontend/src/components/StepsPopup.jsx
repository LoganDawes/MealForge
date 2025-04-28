import React, { useState, useEffect } from "react";
import { Card, ListGroup, Button } from "react-bootstrap";
import IngredientPopup from "./IngredientPopup";
import axios_api from "../utils/axiosInstance"; // Import axios instance
import "./StepsPopup.css";

const StepsPopup = ({ step, recipeIngredients, onClose }) => {
    const [selectedIngredient, setSelectedIngredient] = useState(null); // State for selected ingredient
    const [ingredientDetails, setIngredientDetails] = useState(null); // State for fetched ingredient details

    const normalizeName = (name) => name.toLowerCase().replace(/[^a-z0-9]/g, ""); // Normalize names for comparison

    const isSimilarName = (name1, name2) => {
        const normalized1 = normalizeName(name1);
        const normalized2 = normalizeName(name2);
        return (
            normalized1.includes(normalized2) || normalized2.includes(normalized1) // Substring match
        );
    };

    const handleClickOutside = (e) => {
        if (e.target.classList.contains("popup-overlay")) onClose();
    };

    const handleEquipmentImageError = (event) => {
        event.target.style.display = "none"; // Hide the image if it fails to load
    };

    // Ensure step.ingredients is defined
    const mappedIngredients = (step.ingredients || []).map((stepIngredient) => {
        // Try to match by id first
        let matchedIngredient = recipeIngredients.find((ingredients) => ingredients.id === stepIngredient.id);

        // If no match by id, try to match by similar name
        if (!matchedIngredient) {
            matchedIngredient = recipeIngredients.find((ingredients) =>
                isSimilarName(ingredients.name, stepIngredient.name)
            );
        }

        // Map the ingredient
        const mappedIngredient = matchedIngredient
            ? {
                id: matchedIngredient.id,
                name: matchedIngredient.name,
                amount: matchedIngredient.amount,
                unit: matchedIngredient.unit,
                clickable: true,
            }
            : { ...stepIngredient, clickable: false }; // If no match, mark as not clickable

        console.log("Mapped Ingredient:", mappedIngredient); // Debugging log
        return mappedIngredient;
    });

    console.log("Mapped Ingredients:", mappedIngredients); // Debugging log

    // Fetch ingredient details when an ingredient is selected
    useEffect(() => {
        const fetchIngredientDetails = async () => {
            console.log("Fetching ingredient details for:", selectedIngredient);
            if (!selectedIngredient) return;

            try {
                const ingredientResponse = await axios_api.get(`/ingredients/${selectedIngredient.id}`, {
                    params: { amount: selectedIngredient.amount, unit: selectedIngredient.unit },
                    noAuth: true,
                });
                console.log("Fetched ingredient details:", ingredientResponse.data);
                setIngredientDetails(ingredientResponse.data); // Set fetched details
            } catch (error) {
                console.error("Error fetching ingredient details:", error);
            }
        };

        fetchIngredientDetails();
    }, [selectedIngredient]);

    return (
        <div className="popup-overlay" onClick={handleClickOutside}>
            <Card className="popup-card">
                {/* Header */}
                <div className="popup-header d-flex justify-content-between align-items-center">
                    <div className="d-flex align-items-center">
                        <h1 className="step-number">{step.number}</h1>
                        <p className="step-description">{step.step}</p>
                    </div>
                    <Button variant="outline-danger" onClick={onClose}>
                        X
                    </Button>
                </div>

                {/* Content */}
                <div className="popup-content d-flex">
                    {/* Left Column: Ingredients */}
                    <div className="popup-column">
                        <h5>Ingredients</h5>
                        <div className="scrollable-list">
                            {mappedIngredients.length > 0 ? (
                                <ListGroup>
                                    {mappedIngredients.map((ingredient, idx) => (
                                        <ListGroup.Item
                                            key={idx}
                                            className={ingredient.clickable ? "clickable" : ""}
                                            onClick={() => {
                                                if (ingredient.clickable) {
                                                    console.log("Setting selected ingredient:", ingredient); // Debugging log
                                                    setSelectedIngredient({
                                                        id: ingredient.id,
                                                        name: ingredient.name,
                                                        amount: ingredient.amount,
                                                        unit: ingredient.unit,
                                                    }); // Set selected ingredient
                                                }
                                            }}
                                            style={{
                                                cursor: ingredient.clickable ? "pointer" : "default",
                                                color: ingredient.clickable ? "inherit" : "gray",
                                            }}
                                        >
                                            {ingredient.amount && ingredient.unit
                                                ? `${ingredient.amount} ${ingredient.unit} ${ingredient.name}`
                                                : ingredient.name}
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>
                            ) : (
                                <p>No ingredients on this step</p>
                            )}
                        </div>
                    </div>

                    {/* Right Column: Equipment */}
                    <div className="popup-column">
                        <h5>Equipment</h5>
                        <div className="scrollable-list">
                            {step.equipment?.length > 0 ? (
                                <ListGroup>
                                    {step.equipment.map((equipment, idx) => (
                                        <ListGroup.Item key={idx}>
                                            <div>{equipment.name}</div>
                                            {equipment.image && (
                                                <img
                                                    src={equipment.image}
                                                    alt={equipment.name}
                                                    className="img-fluid rounded mt-2"
                                                    style={{ maxWidth: "100px" }}
                                                    onError={handleEquipmentImageError} // Hide image if it fails to load
                                                />
                                            )}
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>
                            ) : (
                                <p>No equipment on this step</p>
                            )}
                        </div>
                    </div>
                </div>
            </Card>

            {/* Render IngredientPopup if ingredient details are fetched */}
            {ingredientDetails && (
                <IngredientPopup
                    ingredient={ingredientDetails}
                    onClose={() => {
                        setSelectedIngredient(null); // Reset selectedIngredient
                        setIngredientDetails(null); // Reset ingredientDetails
                    }}
                />
            )}
        </div>
    );
};

export default StepsPopup;