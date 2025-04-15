import React, { useState } from "react";
import { Navbar, Button, Form, InputGroup, Nav, Container } from "react-bootstrap";
import "./Color.css"

const SubNavbar = ({ pageTitle, onSearch }) => {
    // States
    const [activeTab, setActiveTab] = useState("search");
    const [searchText, setSearchText] = useState("");

    const handleSearch = () => {
        onSearch(searchText);
    };

    // HTML
    return (
        <Navbar bg="light" expand="lg" className="mt-5">
            <Container fluid className="d-flex justify-content-between">
                {/* "Search" and "Saved" tabs */}
                <Nav className="me-3">
                    <Nav.Link
                        onClick={() => setActiveTab("search")}
                        className={`px-3 ${activeTab === "search" ? "border-bottom border-primary" : ""}`}
                    >
                        Search
                    </Nav.Link>
                    <Nav.Link
                        onClick={() => setActiveTab("saved")}
                        className={`px-3 ${activeTab === "saved" ? "border-bottom border-primary" : ""}`}
                    >
                        Saved
                    </Nav.Link>
                </Nav>

                {/* Page Title */}
                <h5 className="flex-grow-1 text-center m-0">{pageTitle}</h5>

                {/* Filter, Sort, and Search bar */}
                <div className="d-flex align-items-center">
                    <Button variant="outline-secondary" className="me-2">Filter</Button>
                    <Button variant="outline-secondary" className="me-2">Sort</Button>

                    {/* Search Bar */}
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
