import './App.css';
import Home from './pages/Home/Home';
import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login/Login'
import Register from './pages/Register/Register';
import Profile from './pages/Profile/Profile';
import SearchGigs from './pages/SearchGigs/SearchGigs';
import PostGig from './pages/PostGig/PostGig';
import OtherUser from './pages/OtherUser/OtherUser';

function App() {

  return (
    <Routes>
      <Route path="/" element={<Home />}/>
      <Route path="/register" element={<Register />}/>
      <Route path="/login" element={<Login />}/>
      <Route path="/profile" element={<Profile />}/>
      <Route path="/gigs" element={<SearchGigs />}/>
      <Route path="/post_gig" element={<PostGig />}/>
      <Route path="/users/:username" element={<OtherUser />}/>
    </Routes>
  )
}

export default App
