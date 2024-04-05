import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
import axios from "axios";
import "../assets/Login.css";

const Register: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");
  const [contactNumber, setContactNumber] = useState<string>("");
  const [postalCode, setPostalCode] = useState<string>("");
  const [error] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const auth = getAuth();
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const uid = userCredential.user.uid;
      console.log("Registration successful. User UID:", uid);

      // Make a POST request to create user in backend with additional fields
      const response = await axios.post("http://127.0.0.1:8000/users", {
        first_name: firstName,
        last_name: lastName,
        contact_number: contactNumber,
        postal_code: postalCode,
        email,
        is_admin: false, // Adjust as needed
        uid
      });

      if (response.status === 200) {
        // Clear form data after successful registration
        setEmail('');
        setPassword('');
        setFirstName('');
        setLastName('');
        setContactNumber('');
        setPostalCode('');
        navigate("/Explore");
      } else {
        console.error('Failed to register user');
      }
    } catch (error) {
      //setError(error.message);
      console.error('Error registering user:', error);
    }
  };

  return (
    <div className="login-container">
      <h2>Register</h2>
      <div className="form-group">
        <input
          type="text"
          placeholder="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
        />
      </div>
      <div className="form-group">
        <input
          type="text"
          placeholder="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
        />
      </div>
      <div className="form-group">
        <input
          type="text"
          placeholder="Contact Number"
          value={contactNumber}
          onChange={(e) => setContactNumber(e.target.value)}
        />
      </div>
      <div className="form-group">
        <input
          type="text"
          placeholder="Postal Code"
          value={postalCode}
          onChange={(e) => setPostalCode(e.target.value)}
        />
      </div>
      <div className="form-group">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className="form-group">
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      {error && <div className="error-message">{error}</div>}
      <div className="form-group">
        <button onClick={handleRegister}>Register</button>
      </div>
      <p>
        Already have an account? <Link to="/">Login</Link>
      </p>
    </div>
  );
};

export default Register;
