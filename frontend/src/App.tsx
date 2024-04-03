//import { useState } from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import './App.css'
import Home from './pages/Home'
import Login from './pages/Login'
import Explore from './pages/Explore'
import Cart from './pages/Cart'
import Register from "./pages/Register";
import AdminDashboard from "./pages/AdminDashboard";
import EditBooks from './pages/EditBooks'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  //const [count, setCount] = useState(0)

  return (
    <>
      <Router>
        <Routes>
          <Route path="/*" element={<Login />} />
          <Route path="/Home" element={<Home />} />
          <Route path="/Explore" element={<Explore />} />
          <Route path="/Cart" element={<Cart />} />
          <Route path="/Register" element={<Register />} />
          <Route path="/AdminDashboard" element={<AdminDashboard />} />
          <Route path="/EditBooks" element={<EditBooks/>}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
