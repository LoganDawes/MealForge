import Navigationbar from '../components/Navbar';
import "bootstrap/dist/css/bootstrap.min.css";

function Profile() {
    // HTML
    return (
    <div className="Profile">
      <Navigationbar />
      <h1 className="mb-3 text-primary">Profile Page</h1>
    </div>
    );
}

export default Profile;