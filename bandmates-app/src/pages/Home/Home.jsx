import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import UploadPost from '../../components/UploadPost/UploadPost';
import NewsFeed from '../../components/NewsFeed/NewsFeed';
import Leftbar from '../../components/Leftbar/Leftbar';
import Rightbar from '../../components/Rightbar/Rightbar';
import MessageBox from '../../components/MessageBox/MessageBox';
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
        <Leftbar />
        <div className="home-content-container">
          <div className="home-vertical-content">
            <UploadPost/>
            <NewsFeed />
          </div>
        </div>
        <div className="home-content-container">
          <Rightbar />
        </div>
        <MessageBox />
      </div>
    </>
  );
}

export default Home;
