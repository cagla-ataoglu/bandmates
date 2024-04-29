import React from 'react';
import { MdOutlineMoreVert } from 'react-icons/md';

const Post = ({ post }) => {
  // Extract the updated fields from the post object
  const { username, Timestamp, description, url } = post;

  return (
    <div className="w-full rounded-md shadow-lg mt-[30px] mb-[30px] p-[20px]">
      <div className="p-[10px]">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {/* <img src={profilePic} alt="Profile Picture" className="w-[32px] h-[32px] rounded-full object-cover" /> */}
            <span className="font-bold ml-[10px] mr-[10px]">{username}</span>
            <span className="text-sm">{new Date(Timestamp).toLocaleString()}</span> 
          </div>
          <div>
            <MdOutlineMoreVert className="text-xl cursor-pointer" />
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
