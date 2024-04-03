import React, { useState } from "react";
import { Routes, Route, useNavigate, Link } from "react-router-dom";
import { app } from "./firebaseConfig";
//import "./assets/Login.css";
import "../assets/Login.css";
import { getAuth } from "firebase/auth";
import { signInWithEmailAndPassword } from "firebase/auth/cordova";
import { FirebaseError } from "firebase/app";
import Home from "./Home";
import Register from "./Register";


const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const gotoHome = (uid: string) => {
    navigate("/Explore", { state: { uid: uid } });
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

      if (user) { // Removed condition for email verification
        const uid = user.uid;
        gotoHome(uid);
      }

    } catch (e) {
      if (e instanceof FirebaseError) {
        switch (e.code) {
          case "auth/invalid-email":
            setError("Invalid email address.");
            break;
          case "auth/user-disabled":
            setError("User has been disabled.");
            break;
          case "auth/invalid-login-credentials":
            setError("Invalid login credentials.");
            break;
          case "auth/user-not-found":
            setError("User not found.");
            break;
          case "auth/wrong-password":
            setError("Incorrect password.");
            break;
          case "auth/network-request-failed":
            setError("Network error.");
            break;
          case "auth/too-many-requests":
            setError("Too many attempts. Try again later.");
            break;
          case "auth/operation-not-allowed":
            setError("Operation not allowed.");
            break;
          default:
            console.error("Error signing in: ", e.code);
        }
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
          </Routes>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
};

export default Login;
