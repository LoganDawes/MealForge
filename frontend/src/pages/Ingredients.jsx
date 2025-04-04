import Navigationbar from '../components/Navbar';
import SubNavbar from "../components/SubNavbar";
import "bootstrap/dist/css/bootstrap.min.css";

function Ingredients() {
    // HTML
    return (
    <div className="Ingredients">
      <Navigationbar />
      <SubNavbar pageTitle="Ingredients" />
      <h1 className="mb-3 text-primary">Ingredients Page</h1>
    </div>
    );
}

export default Ingredients;