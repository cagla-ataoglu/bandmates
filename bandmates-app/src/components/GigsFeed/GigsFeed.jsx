import React, { useState, useEffect } from 'react';
import Post from '../Post/Post';
import './GigsFeed.css';

const GigsFeed = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await fetch('http://localhost:8082/get_git_postings', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      if (data.status === 'success') {
        const sortedPosts = data.posts.sort((a, b) => new Date(b.Timestamp) - new Date(a.Timestamp));
        setPosts(sortedPosts);
      } else {
        console.error('Failed to fetch posts:', data.message);
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  return (
    <div className="gigsfeed-card">
        <h1>Available Gigs</h1>
      <ul className="gigs-list"> 
        {posts.map((post, index) => (
          <li key={post.PostId}>
            <Post post={post} />
            {index !== posts.length - 1 && <div className="separator"></div>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GigsFeed;
