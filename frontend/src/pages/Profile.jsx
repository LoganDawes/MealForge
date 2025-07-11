import React, { useState, useEffect } from "react";
import Navigationbar from "../components/Navbar";
import { Modal, Form, Card, Container, Button, Dropdown } from "react-bootstrap";
import "./Color.css";
import axios_api from "../utils/axiosInstance";
import { useNavigate } from "react-router-dom";

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
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  // Fetch preferences when component mounts
  useEffect(() => {
    const fetchPreferences = async () => {
      try {
        const response = await axios_api.get("/preferences/");
        setSelectedDiets(response.data.diets);
        setSelectedIntolerances(response.data.intolerances);
        setCalorieLimit(response.data.calorie_limit === 9999 ? "" : response.data.calorie_limit);
      } catch (error) {
        console.error("Error fetching preferences:", error);
      }
    };

    fetchPreferences();
  }, []);

  // Update preferences on the backend
  const updatePreferences = async () => {
    try {
      const response = await axios_api.put(
        "/preferences/update/",
        {
          diets: selectedDiets,
          intolerances: selectedIntolerances,
          calorie_limit: calorieLimit === "" ? 9999 : calorieLimit,
        },
      );
      console.log("Preferences updated:", response.data);
      alert("Preferences saved!");
    } catch (error) {
      console.error("Error updating preferences:", error);
    }
  };

  // Handle diet preferences
  const handleAddDiet = (diet) => setSelectedDiets((prev) => [...prev, diet]);
  const handleRemoveDiet = (diet) => setSelectedDiets((prev) => prev.filter((d) => d !== diet));

  // Handle intolerance preferences
  const handleAddIntolerance = (item) => setSelectedIntolerances((prev) => [...prev, item]);
  const handleRemoveIntolerance = (item) => setSelectedIntolerances((prev) => prev.filter((i) => i !== item));

  // Handle calorie limit
  const handleCalorieChange = (e) => {
    const value = e.target.value;
    if (value === "" || /^\d{0,4}$/.test(value)) {
      setCalorieLimit(value);
    }
  };

  // Handle save preferences
  const handleSavePreferences = () => {
    updatePreferences();
  };

  // Handle account deletion
  const handleDeleteAccount = async () => {
    const username = localStorage.getItem("username");
    const refreshToken = localStorage.getItem("refreshToken");

    if (!username || !refreshToken) {
      alert("Missing account information. Please log in again.");
      return;
    }

    const response = await axios_api.post("/unregister/", {
      username,
      password,
      refresh_token: refreshToken,
    });
    console.log("Account deleted:", response.data);
    localStorage.removeItem("accessToken");
    navigate("/"); // Redirect to home page
    navigate(0); // Refresh the page
  };

  // Handle delete account modal
  const handleShowDeleteModal = () => setShowDeleteModal(true);
  const handleCloseDeleteModal = () => setShowDeleteModal(false);

  const handleConfirmDelete = async () => {
    try {
      await handleDeleteAccount(); // Attempt to delete the account
      setShowDeleteModal(false); // Close the modal only if successful
    } catch (error) {
      console.error("Error deleting account:", error);
      const errorMessage = error.response?.data?.message || "Failed to delete account. Please try again.";
      setErrorMessage(errorMessage); // Set the error message to display below the password field
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
              value={calorieLimit === "" ? "" : calorieLimit} // Display empty for "No Limit"
              onChange={handleCalorieChange}
              placeholder="Enter calorie limit"
            />
            {calorieLimit === "" && <small className="text-muted">No Limit</small>} {/* Display "No Limit" as a hint */}
          </Form.Group>

          <Button variant="primary" className="w-100 mt-3" onClick={handleSavePreferences}>
            Save Preferences
          </Button>

          <Button variant="danger" className="w-100 mt-3" onClick={handleShowDeleteModal}>
            Delete Account
          </Button>
        </Card>
      </Container>

      {/* Delete Account Modal */}
      <Modal show={showDeleteModal} onHide={handleCloseDeleteModal} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Account Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>To delete your account, please enter your password:</p>
          <Form.Group controlId="password">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {errorMessage && <small className="text-danger">{errorMessage}</small>}
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseDeleteModal}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleConfirmDelete}>
            Delete Account
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default Profile;
