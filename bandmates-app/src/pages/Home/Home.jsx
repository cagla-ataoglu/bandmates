import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import UploadPost from '../../components/UploadPost/UploadPost';
import NewsFeed from '../../components/NewsFeed/NewsFeed';
import Rightbar from '../../components/Rightbar/Rightbar';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      navigate('/login');
    }
  }, [navigate]);

  return (
    <>
      <Navbar />
      <div className="home-container">
        <div className="home-content-container">
          <div className="home-vertical-content">
            <UploadPost/>
            <NewsFeed />
          </div>
        </div>
        <div className="home-content-container">
          <Rightbar />
        </div>
      </div>
    </>
  );
}

export default Home;
