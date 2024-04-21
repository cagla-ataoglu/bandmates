import './App.css';
import Home from './pages/Home/Home';
import { Routes, Route } from 'react-router-dom';
import Register from './pages/Register/Register';

function App() {

  return (
    <Routes>
      <Route path="/" element={<Home />}/>
      <Route path="/register" element={<Register />}/>
    </Routes>
  )
}

export default App
