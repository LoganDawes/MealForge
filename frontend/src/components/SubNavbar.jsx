import React, { useState } from "react";
import { Navbar, Button, Form, InputGroup, Nav, Container, Dropdown, Row, Col } from "react-bootstrap";
import "./Color.css";

const DIET_CHOICES = [
    "Gluten Free", "Ketogenic", "Vegetarian", "Lacto-Vegetarian", "Ovo-Vegetarian",
    "Vegan", "Pescetarian", "Paleo", "Primal", "Low FODMAP", "Whole30"
];

const INTOLERANCE_CHOICES = [
    "Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood", "Sesame",
    "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat"
];

const SORT_OPTIONS = [
    "popularity", "price", "time", "random", "max-used-ingredients", "min-missing-ingredients",
    "alcohol", "caffeine", "copper", "energy", "calories", "calcium", "carbohydrates",
    "cholesterol", "total-fat", "trans-fat", "saturated-fat", "fiber", "protein", "sugar"
];

const SubNavbar = ({ pageTitle, onSearch, activeTab, onTabChange, onFilterChange }) => {
    const [searchText, setSearchText] = useState("");
    const [selectedDiets, setSelectedDiets] = useState([]);
    const [selectedIntolerances, setSelectedIntolerances] = useState([]);
    const [showFilterDropdown, setShowFilterDropdown] = useState(false);
    const [showSortDropdown, setShowSortDropdown] = useState(false);
    const [sortOption, setSortOption] = useState("");
    const [sortDirection, setSortDirection] = useState("desc");

    const handleSearch = () => {
        onSearch(searchText, selectedDiets, selectedIntolerances, sortOption, sortDirection);
    };

    const toggleSelection = (item, list, setList) => {
        const updatedList = list.includes(item)
            ? list.filter((i) => i !== item)
            : [...list, item];
        setList(updatedList);

        // Notify parent about filter changes
        if (setList === setSelectedDiets) {
            onFilterChange(updatedList); // Pass updated diets to parent
        }
    };

    const totalFilters = selectedDiets.length + selectedIntolerances.length;

    return (
        <>
            <Navbar bg="light" expand="lg" className="mt-5">
                <Container fluid className="d-flex justify-content-between">
                    <Nav className="me-3">
                        <Nav.Link
                            onClick={() => onTabChange("search")}
                            className={`px-3 ${activeTab === "search" ? "active-tab" : ""}`}
                            style={{ color: "black" }}
                        >
                            Search
                        </Nav.Link>
                        <Nav.Link
                            onClick={() => onTabChange("saved")}
                            className={`px-3 ${activeTab === "saved" ? "active-tab" : ""}`}
                            style={{ color: "black" }}
                        >
                            Saved
                        </Nav.Link>
                    </Nav>

                    <h5 className="flex-grow-1 text-center m-0">{pageTitle}</h5>

                    <div className="d-flex align-items-center">
                        {/* Filter Dropdown */}
                        <Dropdown
                            show={showFilterDropdown}
                            onToggle={(isOpen) => setShowFilterDropdown(isOpen)}
                        >
                            <Dropdown.Toggle
                                variant="outline-secondary"
                                className="me-2"
                                style={{ whiteSpace: "nowrap" }}
                            >
                                Filter {totalFilters > 0 && `(${totalFilters})`}
                            </Dropdown.Toggle>

                            <Dropdown.Menu className="p-3" style={{ minWidth: "300px" }}>
                                <Row>
                                    <Col>
                                        <h6>Diets</h6>
                                        {DIET_CHOICES.map((diet) => (
                                            <Form.Check
                                                key={diet}
                                                type="checkbox"
                                                label={diet}
                                                checked={selectedDiets.includes(diet)}
                                                onChange={() => toggleSelection(diet, selectedDiets, setSelectedDiets)}
                                            />
                                        ))}
                                    </Col>
                                    <Col>
                                        <h6>Intolerances</h6>
                                        {INTOLERANCE_CHOICES.map((intolerance) => (
                                            <Form.Check
                                                key={intolerance}
                                                type="checkbox"
                                                label={intolerance}
                                                checked={selectedIntolerances.includes(intolerance)}
                                                onChange={() => toggleSelection(intolerance, selectedIntolerances, setSelectedIntolerances)}
                                            />
                                        ))}
                                    </Col>
                                </Row>
                            </Dropdown.Menu>
                        </Dropdown>

                        {/* Sort Dropdown */}
                        <Dropdown
                            show={showSortDropdown}
                            onToggle={(isOpen) => setShowSortDropdown(isOpen)}
                        >
                            <Dropdown.Toggle
                                variant="outline-secondary"
                                className="me-2"
                                style={{ whiteSpace: "nowrap" }}
                            >
                                Sort {sortOption && (sortDirection === "asc" ? "↑" : "↓")}
                            </Dropdown.Toggle>

                            <Dropdown.Menu className="p-3" style={{ minWidth: "200px" }}>
                                <div className="d-flex justify-content-between align-items-center mb-2">
                                    <Button
                                        variant="outline-secondary"
                                        size="sm"
                                        className="mb-2 w-100"
                                        onClick={() =>
                                            setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"))
                                        }
                                    >
                                        {sortDirection === "asc" ? "Ascending" : "Descending"}
                                    </Button>
                                </div>
                                <Button
                                    variant="outline-danger"
                                    size="sm"
                                    className="mb-2 w-100"
                                    onClick={() => setSortOption("")}
                                >
                                    Clear
                                </Button>
                                <hr />
                                {SORT_OPTIONS.map((option) => (
                                    <Form.Check
                                        key={option}
                                        type="radio"
                                        name="sortOptions"
                                        label={option}
                                        checked={sortOption === option}
                                        onChange={() => setSortOption(option)}
                                    />
                                ))}
                            </Dropdown.Menu>
                        </Dropdown>

                        <InputGroup>
                            <Form.Control
                                type="text"
                                placeholder="Search..."
                                value={searchText}
                                onChange={(e) => setSearchText(e.target.value)}
                            />
                            <Button variant="primary" onClick={handleSearch}>Search</Button>
                            <Button variant="outline-secondary" onClick={() => setSearchText("")}>Clear</Button>
                        </InputGroup>
                    </div>
                </Container>
            </Navbar>
        </>
    );
};

export default SubNavbar;