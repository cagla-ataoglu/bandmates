import React, { useState } from 'react';
import { MdOutlineMoreVert } from 'react-icons/md';
import likeIcon from '../../assets/like.png';
import "./Post.css"

const Post = ({ post }) => {
  // Extract the updated fields from the post object
  const { username, Timestamp, description, url } = post;
  const [optionsVisible, setOptionsVisible] = useState(false);
  const [editVisible, setEditVisible] = useState(false);
  const [editPostDraft, setPostDraft] = useState(description);

  const deletePost = async () => {
    try {
      const response = await fetch('http://localhost:8090/delete_post', {
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
    console.log('Updated post description:', editPostDraft);
    closeEditPopup();
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
          <div className="relative">
            <MdOutlineMoreVert className="text-xl cursor-pointer" onClick={() => setOptionsVisible(!optionsVisible)} />
            {optionsVisible && (
              <div className="options-menu">
                <button className="option-button" onClick={openEditPopup}>Edit</button>
                <button className="option-button" onClick={() => deletePost()}>Delete</button>
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="post-content">
        <p>{description}</p>
        {url && <img src={url} alt="Post media" />}
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