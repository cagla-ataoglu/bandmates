import React, { useState, useEffect } from 'react';
import Post from '../Post/Post';
import './NewsFeed.css';

const NewsFeed = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchFollowings = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_FOLLOW_API}/get_followings`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: localStorage.getItem('username')
          })
        });

        const data = await response.json();
        if (data.status === 'success') {
          return data.followings;
        } else {
          throw new Error('Failed to fetch followings: ' + data.message);
        }
      } catch (error) {
        console.error('Error fetching followings:', error);
      }
    };

    const fetchPosts = async (followings) => {
      try {
        const response = await fetch(`${import.meta.env.VITE_POST_API}/get_posts_by_usernames`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            usernames: followings
          })
        });

        const data = await response.json();
        if (data.status === 'success') {
          const sortedPosts = data.posts.sort((a, b) => new Date(b.Timestamp) - new Date(a.Timestamp));
          setPosts(sortedPosts);
        } else {
          throw new Error('Failed to fetch posts: ' + data.message);
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchFollowings().then(followings => {
      if (followings && followings.length > 0) {
        fetchPosts(followings);
      }
    });
  }, []);

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
