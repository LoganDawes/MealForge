import Navigationbar from '../components/Navbar';
import "bootstrap/dist/css/bootstrap.min.css";
import "./Home.css"
import "./Color.css"
import { Link } from "react-router-dom";

function Home() {
    // HTML
    return (
        <div className="Home">
            <Navigationbar />
            <div className="content">
                <h1>MealForge</h1>
                <p>Maintaining and balancing a nutritional diet is a huge challenge for health-conscious people who want to improve their well-being and find meals that align with their personal diets. Many meal-planning apps can fail to consider the specific nutritional requirements that go into each recipe and can lead to extended periods of research for something that should be simple.
                    MealForge aims to address this, and offer recipes based on user-defined ingredients and dietary restrictions.</p>
                <Link to="/ingredients">
                    <button className="btn btn-primary">Get Started</button>
                </Link>
            </div>
        </div>
    );
}

export default Home;