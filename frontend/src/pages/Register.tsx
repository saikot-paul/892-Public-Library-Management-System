import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../assets/Login.css";
import axios from "axios";

const Register: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string>("");
  const navigate = useNavigate();

  const baseURL = "http://localhost:5173/";

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!email || !username || !password) {
      setError("Email, password, or username has invalid format please try again");
      return;
    }

    try {
      const response = await axios.post(baseURL + "signup", {
        email: email,
        username: username,
        password: password,
      });

      if (response.status === 200 && response.data.success === true) {
        // Registration successful, redirect to login page
        navigate("/");
      } else {
        setError(response.data.message || "Unknown error occurred");
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <div className="top-bar">
        <h1 className="title">
          Simply<span className="colored-words">Plan.</span>
        </h1>
      </div>
      <div className="login-container">
        <h2>Register</h2>
        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              className="input-field"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              className="input-field"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit" className="register-button">
            Register
          </button>
          <label>
            Already have an account? Login{" "}
            <Link to="/">
              <span className="colored-words">here.</span>
            </Link>
          </label>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
};

export default Register;
