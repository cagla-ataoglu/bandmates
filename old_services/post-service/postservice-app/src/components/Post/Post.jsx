import React from 'react';
import { MdOutlineMoreVert } from 'react-icons/md';

const Post = ({ post }) => {
  const { profilePic, username, timestamp, content, media, likes, comments } = post;

  return (
    <div className="w-full rounded-md shadow-lg mt-[30px] mb-[30px] p-[20px]">
      <div className="p-[10px]">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <img src={profilePic} alt="Profile Picture" className="w-[32px] h-[32px] rounded-full object-cover" />
            <span className="font-bold ml-[10px] mr-[10px]">{username}</span>
            <span className="text-sm">{timestamp}</span>
          </div>
          <div>
            <MdOutlineMoreVert className="text-xl cursor-pointer" />
          </div>
        </div>
      </div>
      <div className="mt-[20px] mb-[20px]">
        <span>{content}</span>
        {media && <img src={media} alt="Media Post" className="mt-[20px] w-full object-contain" style={{ maxHeight: "500" }} />}
      </div>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-[5px]">
          <img src={likeIcon} alt="Like Icon" className="w-[24px] h-[24px]" />
          <span className="text-sm">{likes} likes</span>
        </div>
        <div className="div">
          <span className="cursor-pointer border-b-[1px] bored-slate-300 text-sm">{comments} comments</span>
        </div>
      </div>
    </div>
  );
};

export default Post;
