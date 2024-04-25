import './App.css';
import Home from './pages/Home/Home';
import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login/Login'
import Register from './pages/Register/Register';
import FriendProfileCard from './components/FriendProfileCard/FriendProfileCard';

function App() {

  return (
    <Routes>
      <Route path="/" element={<Home />}/>
      <Route path="/register" element={<Register />}/>
      <Route path="/login" element={<Login />}/>
      <Route path="/user" element={<FriendProfileCard/>}/>
    </Routes>
  )
}

export default App
