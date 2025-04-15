import React, { useState } from "react";
import { Navbar, Button, Form, InputGroup, Nav, Container } from "react-bootstrap";
import "./Color.css"

const SubNavbar = ({ pageTitle, onSearch, activeTab, onTabChange }) => {
    const [searchText, setSearchText] = useState("");

    const handleSearch = () => {
        onSearch(searchText);
    };

    return (
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
                    <Button variant="outline-secondary" className="me-2">Filter</Button>
                    <Button variant="outline-secondary" className="me-2">Sort</Button>

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
    );
};

export default SubNavbar;
