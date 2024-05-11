import React from 'react';
import Navbar from '../../components/Navbar/Navbar';
import GigForm from '../../components/GigForm/GigForm';
import GigsBar from '../../components/GigsBar/GigsBar';
import MiniProfileCard from '../../components/MiniProfileCard/MiniProfileCard';
import './PostGig.css';

const PostGig = () => {
  return (
    <>
      <Navbar />
      <div className="post-gig-container">
        <div className="post-gig-content-container">
          <MiniProfileCard />
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
