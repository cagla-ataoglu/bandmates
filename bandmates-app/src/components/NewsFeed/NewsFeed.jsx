import React, { useState, useEffect } from 'react';
import Post from '../Post/Post';
import './NewsFeed.css';

const NewsFeed = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await fetch('http://localhost:8090/display_posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      if (data.status === 'success') {
        setPosts(data.posts);
      } else {
        console.error('Failed to fetch posts:', data.message);
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  return (
    <div className="newsfeed-card">
      <ul className="newsfeed-list"> 
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

export default NewsFeed;
