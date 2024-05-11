import React from 'react';
import Navbar from '../../components/Navbar/Navbar';
import UploadPost from '../../components/UploadPost/UploadPost';
import NewsFeed from '../../components/NewsFeed/NewsFeed';
import Leftbar from '../../components/Leftbar/Leftbar';
import Rightbar from '../../components/Rightbar/Rightbar';
import MessageBox from '../../components/MessageBox/MessageBox';
import './Home.css';

const Home = () => {
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
