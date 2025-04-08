import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css"

function Recipes() {
    // HTML
    return (
    <div className="Recipes">
      <Navigationbar />
      <SubNavbar pageTitle="Recipes" />
      <h1 className="mb-3 text-primary">Recipes Page</h1>
    </div>
    );
}

export default Recipes;