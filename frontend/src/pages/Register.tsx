import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
//import { AuthenticationContext } from '../context/AuthenticationContext';
import "../assets/Login.css";
//import axios from "axios";

const Register: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleRegister = async () => {
    const auth = getAuth();
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      // Registration successful
      const user = userCredential.user;
      console.log("Registration successful:", user);
      // Redirect or perform other actions upon successful registration
      navigate("/Explore"); // Example redirect to dashboard
    } catch (error) {
      //const errorCode = error.code;
      //const errorMessage = error.message;
      //console.error("Registration error:", errorCode, errorMessage);
      //setError(errorMessage); // Set error message to display to the user
    }
  };

  return (
    <div className="login-container">
      <h2>Register</h2>
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
