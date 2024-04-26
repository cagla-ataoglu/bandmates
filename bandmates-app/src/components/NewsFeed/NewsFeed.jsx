// NewsFeed.js
import React, { useState, useEffect } from 'react';
import Post from '../Post/Post';
import './NewsFeed.css';
import axios from 'axios';

const NewsFeed = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await axios.get('http://localhost:8090/display_posts');
      if (response.data.status === 'success') {
        setPosts(response.data.posts);
      } else {
        console.error('Failed to fetch posts:', response.data.message);
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  return (
    <div className="newsfeed-card">
      <ul className="newsfeed-list"> 
        {/* AFTER CONNECTING THE DATABASE DELETE THIS PART BELOW  AND LEAVE RENDER POSTS*/}
        {[...Array(10)].map((_, index) => (
          <li key={index}>
            <p>Random Post Here</p>
            {index !== 9 && <div className="separator"></div>}
          </li>
        ))}
      </ul>

      {/* Render posts */}
      {posts.map((post, index) => (
        <Post key={index} post={post} />
      ))}
    </div>
  );
};

export default NewsFeed;
