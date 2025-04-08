import Navigationbar from '../components/Navbar';
import "bootstrap/dist/css/bootstrap.min.css";
import "./Color.css"

function Login() {
    // HTML
    return (
    <div className="Login">
      <Navigationbar />
      <h1 className="mb-3 text-primary">Login Page</h1>
    </div>
    );
}

export default Login;