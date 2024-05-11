import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import GigsFeed from '../../components/GigsFeed/GigsFeed';
import GigsBar from '../../components/GigsBar/GigsBar';
import SearchGigsBar from '../../components/SearchGigsBar/SearchGigsBar';
import MiniProfileCard from '../../components/MiniProfileCard/MiniProfileCard';
import './SearchGigs.css';

const SearchGigs = () => {
  const navigate = useNavigate();

  const handlePostClick = () => {
      navigate('/post_gig');
  };

  return (
    <>
      <Navbar />
      <div className="gigs-container">
        <div className="gigs-content-container">
          <MiniProfileCard />
          <GigsBar />
          <button className="gigs-container button"  onClick={handlePostClick}>
                        Post a Gig
            </button>
        </div>
        <div className="gigs-content-container">
          <div className="gigs-vertical-content">
            <GigsFeed />
          </div>
        </div>
        <div className="gigs-content-container">
          <SearchGigsBar />
        </div>
      </div>
    </>
  );
}

export default SearchGigs;
