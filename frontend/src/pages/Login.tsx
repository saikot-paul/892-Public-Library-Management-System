import React, { useState } from "react";
import { Routes, Route, useNavigate, Link } from "react-router-dom";
import { app } from "./firebaseConfig";
import { getAuth } from "firebase/auth";
import { signInWithEmailAndPassword } from "firebase/auth/cordova";
import { FirebaseError } from "firebase/app";
import Home from "./Home";
import Register from "./Register";
import AdminDashboard from "./AdminDashboard";
import axios from "axios";

const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const gotoHome = async (uid: string) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/users/${uid}`);
      const userData = response.data.userInfo; // Access userInfo object
      if (userData.isAdmin) {
        navigate("/adminDashboard", { state: { uid: uid } });
      } else {
        navigate("/Explore", { state: { uid: uid } });
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const handleFirebaseError = (errorCode: string) => {
    switch (errorCode) {
      case "auth/invalid-email":
        return "Invalid email address.";
      case "auth/user-disabled":
        return "User has been disabled.";
      case "auth/user-not-found":
        return "User not found.";
      case "auth/wrong-password":
        return "Incorrect password.";
      case "auth/network-request-failed":
        return "Network error.";
      case "auth/too-many-requests":
        return "Too many attempts. Try again later.";
      case "auth/operation-not-allowed":
        return "Operation not allowed.";
      default:
        return "An error occurred. Please try again.";
    }
  };

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      if (!email || !password) {
        setError("Missing email/password");
        return;
      }
      const auth = getAuth(app);
      const userCreds = await signInWithEmailAndPassword(auth, email, password);
      const user = userCreds.user;

      if (user) {
        const uid = user.uid;
        gotoHome(uid);
      }

    } catch (e) {
      if (e instanceof FirebaseError) {
        setError(handleFirebaseError(e.code));
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    }
  };

  return (
    <div>
      <div className="top-bar">
      </div>
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
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
            <label>Password:</label>
            <input
              type="password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit" className="login-button">
            Login
          </button>
          <label>
            Dont have an account? Create one{" "}
            <Link to="/register">
              <span className="colored-words">now.</span>
            </Link>
          </label>
          <Routes>
            <Route path="/Explore" element={<Home />} />
            <Route path="/Register" element={<Register />} />
            {/* Add a route for admin dashboard */}
            <Route path="/adminDashboard" element={<AdminDashboard />} />
          </Routes>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
};

export default Login;
