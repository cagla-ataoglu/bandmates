import './App.css';
import Home from './pages/Home/Home';
import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login/Login'
import Register from './pages/Register/Register';
import Profile from './pages/Profile/Profile';

function App() {

  return (
    <Routes>
      <Route path="/" element={<Home />}/>
      <Route path="/register" element={<Register />}/>
      <Route path="/login" element={<Login />}/>
      <Route path="/profile" element={<Profile />}/>
    </Routes>
  )
}

export default App
