import React, { useState } from 'react';
import profilePic from '../../assets/musician_pfp.jpg';
import { MdPermMedia } from "react-icons/md";
import './UploadPost.css';
import axios from 'axios';

const UploadPost = ({ onPostCreated }) => {
    const [content, setContent] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const userId = 'b0bm4rl3y'; // note: to be replaced
            const response = await axios.post('http://localhost:8090/create_post', {
                content,
                user_id: userId
            });
            console.log('Post created:', response.data);
            onPostCreated();
        } catch (error) {
            console.error('Error creating post:', error);
        }
    };

    return (
        <div className="upload-post-container">
            <div className="upload-post-wrapper">
                <div className="upload-post-top-container">
                    <img src={profilePic} alt="profilepic" className="upload-post-profile-pic" />
                    <input type="text" placeholder="What is on your mind?" value={content} onChange={(e) => setContent(e.target.value)} className="upload-post-input" />
                </div>
                <hr className="divider" />
                <div className="bottom">
                    <div className="options">
                        <div className="option">
                            <MdPermMedia className="upload-post-icon"/>
                            <span>Photo or Video</span>
                        </div>
                    </div>
                    <button onClick={handleSubmit} className="upload-post-button">Upload</button>
                </div>
            </div>
        </div>
    );
};

export default UploadPost;
