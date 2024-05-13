import React, { useState, useEffect, useRef } from 'react';
import { MdOutlineMoreVert } from 'react-icons/md';
import "./Post.css"
import {
  S3Client,
  GetObjectCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const Post = ({ post }) => {
  const { username, Timestamp, description, url } = post;
  const [optionsVisible, setOptionsVisible] = useState(false);
  const [editVisible, setEditVisible] = useState(false);
  const [editPostDraft, setPostDraft] = useState(description);
  const [contentUrl, setContentUrl] = useState('');
  const searchRef = useRef(null);

  useEffect(() =>{
    async function fetchSignedUrl() {
      var s3Client = null;
      if (import.meta.env.VITE_ENV == 'production') {
        s3Client = new S3Client({
          region: import.meta.env.VITE_AWS_DEFAULT_REGION, 
          credentials: {
            accessKeyId: import.meta.env.VITE_AWS_ACCESS_KEY_ID, 
            secretAccessKey: import.meta.env.VITE_AWS_SECRET_ACCESS_KEY
        }});
        const bucketName = 'bandmates-media-storage';
        console.log('url:', url);
        const parts = url.split('/');
        const key = parts[parts.length - 1];
        const command = new GetObjectCommand({Bucket: bucketName, Key: key });
        const signed_url = await getSignedUrl(s3Client, command, { expiresIn: 15 * 60 });
        setContentUrl(signed_url);
      } else {
        setContentUrl(url);
      }
    }
    fetchSignedUrl();
  }, []);

  const deletePost = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_POST_API}/delete_post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          post_id: post.PostId
        })
      });

      const data = await response.json();
      if (response.ok) {
        console.log('Post deleted.');
        window.location.reload();
      } else {
        console.log('Failed to delete post. ' + data.message);
      }

    } catch (error) {
      console.log(`Error deleting post with id ${post.PostId}`);
    }
  };

  const editPostDescription = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_POST_API}/edit_post_description`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          post_id: post.PostId,
          description: editPostDraft
        })
      });

      const data = await response.json()
      if (response.ok) {
        console.log('Post description edited.');
        window.location.reload();
      } else {
        console.log('Failed to edit post description. ' + data.message);
      }
    } catch (error) {
      console.log(`Error editing post with id ${post.PostId}`);
    }
  };

  const openEditPopup = () => {
    setOptionsVisible(false);
    setEditVisible(true);
  };

  const closeEditPopup = () => {
    setEditVisible(false);
  };

  const editPost = (e) => {
    setPostDraft(e.target.value);
  };

  const handleSaveEdit = () => {
    editPostDescription();
    console.log('Updated post description:', editPostDraft);
    closeEditPopup();
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setOptionsVisible(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [searchRef]);

  const renderMediaContent = () => {
    const fileExtension = contentUrl.split('.').pop();
    if (['mp4', 'webm', 'ogg', 'mov'].includes(fileExtension)) {
      return <video controls src={contentUrl} className="post-media"></video>;
    } else {
      return <img src={contentUrl} alt="Post media" className="post-media"/>;
    }
  };

  return (
    <div className="post-container">
      <div className="p-[10px]">
        <div className="post-header">
          <div className="post-user-info">
            {/* <img src={profilePic} alt="Profile Picture" className="w-[32px] h-[32px] rounded-full object-cover" /> */}
            <span className="post-username">{username}</span>
            <span className="post-timestamp">{new Date(Timestamp).toLocaleString()}</span> 
          </div>
          {username == localStorage.getItem('username') && <div className="relative">
            <MdOutlineMoreVert className="text-xl cursor-pointer" onClick={() => setOptionsVisible(!optionsVisible)} />
            {optionsVisible && (
              <div className="options-menu" ref={searchRef}>
                <button className="option-button" onClick={openEditPopup}>Edit</button>
                <button className="option-button" onClick={() => deletePost()}>Delete</button>
              </div>
            )}
          </div>}
        </div>
      </div>
      <div className="post-content">
        <p>{description}</p>
        {contentUrl && renderMediaContent()}
      </div>
      {/* Assuming no interactive like and comment features are currently supported */}
      {/* <div className="flex items-center justify-between">
        <div className="flex items-center gap-[5px]">
          <img src={likeIcon} alt="Like Icon" className="w-[24px] h-[24px]" />
          <span className="text-sm">{likes} likes</span>
        </div>
        <div>
          <span className="cursor-pointer border-b-[1px] border-slate-300 text-sm">{comments} comments</span>
        </div>
      </div> */}
      {editVisible && (
        <div className="edit-popup">
          <div className="edit-popup-content">
            <h2>Edit Post</h2>
            <textarea value={editPostDraft} onChange={editPost} />
            <div classname="button">
              <button className="cancel-button" onClick={closeEditPopup}>Cancel</button>
              <button className="save-button" onClick={handleSaveEdit}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Post;