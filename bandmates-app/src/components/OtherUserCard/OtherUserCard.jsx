import React, { useState, useEffect } from 'react';
import Post from '../Post/Post';
import './OtherUserCard.css';

const OtherUserCard = ({ username }) => {
    const [profileData, setProfileData] = useState(null);
    const [posts, setPosts] = useState([]);
    const [followers, setFollowers] = useState(0);
    const [followings, setFollowings] = useState(0);
    const [isFollowing, setIsFollowing] = useState(false);

    useEffect(() => {
        const fetchProfileData = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/get_profile`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: username
                    })
                });
                if (response.ok) {
                    const data = await response.json();
                    setProfileData(data)
                    return data;
                } else {
                    console.error(`Failed to fetch profile data for ${username}`);
                }
            } catch (error) {
                console.error('Error fetching profile data:', error);
            }
        };
    
        const fetchPosts = async (username) => {
          try {
            const response = await fetch(`${import.meta.env.VITE_POST_API}/get_posts_by_usernames`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                usernames: [username]
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

        const fetchFollowers = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_FOLLOW_API}/get_followers`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "username": username })
                });
                const data = await response.json();
                if (data.status === 'success') {
                    setFollowers(data.followers.length);
                    setIsFollowing(data.followers.includes(localStorage.getItem('username')));
                } else {
                    console.error('Failed to fetch followers');
                }
            } catch (error) {
                console.error('Error fetching followers:', error);
            }
        };
        
        const fetchFollowings = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_FOLLOW_API}/get_followings`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "username": username })
                });
                const data = await response.json();
                if (data.status === 'success') {
                    setFollowings(data.followings.length);
                } else {
                    console.error('Failed to fetch followings');
                }
            } catch (error) {
                console.error('Error fetching followings:', error);
            }
        }; 
    
        fetchProfileData().then(user => {
          if (user && user.username) {
            fetchPosts(user.username);
            fetchFollowers();
            fetchFollowings();
          }
        });
    }, []);

    const handleFollow = async () => {
        const endpoint = isFollowing ? 'unfollow' : 'follow';
        try {
            const response = await fetch(`${import.meta.env.VITE_FOLLOW_API}/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    follower: localStorage.getItem('username'),
                    following: username
                })
            });
            const data = await response.json();
            if (data.status === 'success') {
                console.log(`${isFollowing ? 'Unfollow' : 'Follow'} successful`);
                if (isFollowing) {
                    setFollowers(prev => prev - 1);
                } else {
                    setFollowers(prev => prev + 1);
                }
                setIsFollowing(!isFollowing);
            } else {
                console.error(`Failed to ${isFollowing ? 'unfollow' : 'follow'} user:`, data.message);
            }
        } catch (error) {
            console.error(`Error ${isFollowing ? 'unfollowing' : 'following'} user:`, error);
        }
    };    

    return (
        <div className="custom-container">
            <div className='pc'>
                <div className="gradiant">
                    <div className="follow-section">Followers: {followers}</div>
                    <div className="follow-section">Following: {followings}</div>
                    <button className="follow-button" onClick={handleFollow}>
                        {isFollowing ? 'Unfollow' : 'Follow'}
                    </button>
                </div>
                <div className="profile-down">
                    {profileData && (
                        <>
                            <img src={profileData.profile_picture} alt="" />
                            <div className="profile-information">{username}</div>
                            <div className="profile-title">Name: {profileData.display_name}</div>
                            <div className="profile-information">Profile type: {profileData.profile_type}</div>
                            <div className="profile-information">Location: {profileData.location}</div>
                            <div className="profile-information">Genres: {profileData.genres}</div>
                            {profileData.profile_type === "band" && profileData.members && (
                                <div className="profile-information">Members: {profileData.members.join(', ')}</div>
                            )}
                            {profileData.profile_type === "musician" && profileData.instrument && (
                                <div className="profile-information">Instruments: {profileData.instruments.join(', ')}</div>
                            )}
                            {profileData.genres && (
                                <div className="profile-information">{profileData.genres.join(', ')}</div>
                            )}
                            {/* <div className="profile-description">{profileData.profile_description}</div> */}
                            {/* <div className="profile-button"><a href={`mailto:${profileData.email}`}>Contact Me</a></div> */}
                        </>
                    )}
                </div>
            </div>
            <div className="posts-card">
                <div className='posts-title'>Posts</div>
                <ul className="posts-list">
                    {posts.map((post, index) => (
                    <li key={post.PostId}>
                        <Post post={post} />
                    </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default OtherUserCard;
