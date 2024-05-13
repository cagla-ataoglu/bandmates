import React, { useState, useEffect } from 'react';
import profilePic from '../../assets/musician_pfp.jpg'; // Ensure this path is correct for your profile picture
import { MdPermMedia } from 'react-icons/md';
import './UploadPost.css';

const UploadPost = () => {
    const [file, setFile] = useState(null);
    const [description, setDescription] = useState('');
    const [previewUrl, setPreviewUrl] = useState('');

    useEffect(() => {
        return () => {
            if (previewUrl) {
                URL.revokeObjectURL(previewUrl);
            }
        };
    }, [previewUrl]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file) {
            alert('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('content', file);
        formData.append('description', description);

        const token = localStorage.getItem('access_token');
        if (!token) {
            console.error('No access token provided.');
            return;
        }

        try {
            const response = await fetch(`${import.meta.env.VITE_POST_API}/create_post`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const data = await response.json();
            console.log('Post created:', data);

            if (data.status === 'success') {
                window.location.reload();
            } else {
                console.error('Failed to create post:', data.message);
            }
        } catch (error) {
            console.error('Error creating post:', error);
        }
    };

    const uploadFile = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFile(file);
            setPreviewUrl(URL.createObjectURL(file));
        }
    };

    return (
        <div className="upload-post-container">
            <div className="upload-post-wrapper">
                <div className="upload-post-top-container">
                    <img src={profilePic} alt="profile pic" className="upload-post-profile-pic" />
                    <textarea placeholder="What is on your mind?" value={description} onChange={(e) => setDescription(e.target.value)} className="upload-post-input" />
                </div>
                {previewUrl && (
                    <div className="preview-container">
                        {file && file.type.startsWith('video/') ? (
                            <video controls src={previewUrl} className="upload-post-preview"></video>
                        ) : (
                            <img src={previewUrl} alt="Preview" className="upload-post-preview" />
                        )}
                    </div>
                )}
                <hr className="divider" />
                <div className="bottom">
                    <label className="options">
                        <div className="option">
                            <MdPermMedia className="upload-post-icon" />
                            <span>Choose Photo or Video</span>
                            <input type="file" accept="image/*,video/*" onChange={uploadFile} style={{ display: 'none' }} />
                        </div>
                    </label>
                    <button onClick={handleSubmit} className="upload-post-button">Upload</button>
                </div>
            </div>
        </div>
    );
};

export default UploadPost;
