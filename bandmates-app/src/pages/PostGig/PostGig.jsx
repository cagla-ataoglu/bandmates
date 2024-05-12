import React, { useEffect } from 'react';
import Navbar from '../../components/Navbar/Navbar';
import GigForm from '../../components/GigForm/GigForm';
import GigsBar from '../../components/GigsBar/GigsBar';
import MiniProfileCard from '../../components/MiniProfileCard/MiniProfileCard';
import './PostGig.css';
import { useNavigate } from 'react-router-dom';

const PostGig = () => {
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
      <div className="post-gig-container">
        <div className="post-gig-content-container">
          <MiniProfileCard username={localStorage.getItem('username')}/>
          <GigsBar />
        </div>
        <div className="post-gig-content-container">
          <div className="post-gig-vertical-content">
            <GigForm />
          </div>
        </div>
      </div>
    </>
  );
}

export default PostGig;
