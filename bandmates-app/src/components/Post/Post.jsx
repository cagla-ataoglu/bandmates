import React, { useState } from 'react';
import { MdOutlineMoreVert } from 'react-icons/md';
import likeIcon from '../../assets/like.png';

const Post = ({ post }) => {
  // Extract the updated fields from the post object
  const { username, Timestamp, description, url } = post;
  const [optionsVisible, setOptionsVisible] = useState(false);

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

  return (
    <div className="w-full rounded-md shadow-lg mt-[30px] mb-[30px] p-[20px]">
      <div className="p-[10px]">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {/* <img src={profilePic} alt="Profile Picture" className="w-[32px] h-[32px] rounded-full object-cover" /> */}
            <span className="font-bold ml-[10px] mr-[10px]">{username}</span>
            <span className="text-sm">{new Date(Timestamp).toLocaleString()}</span> 
          </div>
          <div className="relative">
            <MdOutlineMoreVert className="text-xl cursor-pointer" onClick={() => setOptionsVisible(!optionsVisible)} />
            {optionsVisible && (
              <div className="absolute right-0 top-[10px] bg-white border rounded-md shadow-lg mt-2">
                <button className="block w-full text-left px-4 py-2 hover:bg-gray-100" onClick={() => console.log("Edit clicked")}>Edit</button>
                <button className="block w-full text-left px-4 py-2 hover:bg-gray-100" onClick={() => deletePost()}>Delete</button>
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="mt-[20px] mb-[20px]">
        <p>{description}</p>
        {url && <img src={url} alt="Post media" className="mt-[20px] w-full object-contain" style={{ maxHeight: "500px" }} />}
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
    </div>
  );
};

export default Post;