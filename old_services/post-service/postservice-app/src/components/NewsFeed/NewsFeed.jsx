// NewsFeed.js
import React, { useState, useEffect } from 'react';
import UploadPost from '../UploadPost/UploadPost';
import Post from '../Post/Post';
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

  const handlePostCreated = (newPost) => {
    setPosts(prevPosts => [...prevPosts, newPost]);
  };

  return (
    <div style={{ flex: 5.5 }}>
      <UploadPost onPostCreated={handlePostCreated} />
      {/* Render posts */}
      {posts.map((post, index) => (
        <Post key={index} post={post} />
      ))}
    </div>
  );
};

export default NewsFeed;
