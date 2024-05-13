import React, { useState, useEffect } from 'react';
import GigPost from '../GigPost/GigPost';
import './GigsFeed.css';

const GigsFeed = ({ posts = [] }) => {

  return (
    <div className="gigsfeed-card">
        <h1>Available Gigs</h1>
      <ul className="gigs-list"> 
        {posts.map((gig, index) => (
          <li key={gig.GigId}>
            <GigPost post={gig} />
            {index !== posts.length - 1 && <div className="separator"></div>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GigsFeed;
