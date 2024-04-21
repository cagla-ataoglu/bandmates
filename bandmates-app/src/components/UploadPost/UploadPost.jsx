import React, { useState } from 'react';
import profilePic from '../../assets/musician_pfp.jpg';
import { MdLabel, MdPermMedia, MdEmojiEmotions, MdLocationPin } from "react-icons/md";
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
        <div className="w-full h-[170px] rounded-lg shadow-lg">
            <div className="wrapper p-[10px] ">
                <div className="top flex items-center">
                    <img src={profilePic} alt="profilepic" className="w-[30px] h-[30px] rounded-full mr-[10px] object-cover" />
                    <input type="text" placeholder="What is on your mind?" value={content} onChange={(e) => setContent(e.target.value)} className="w-[80%] focus:outline-none" />
                </div>
                <hr className="m-[20px]" />
                <div className="bottom flex items-center justify-between">
                    <div className="flex ml-[20px]">
                        <div className="flex items-center mr-[15px] cursor-pointer">
                            <MdPermMedia className="mr-[3px] text-orange-500" />
                            <span>Photo or Video</span>
                        </div>
                        <div className="flex items-center mr-[15px] cursor-pointer">
                            <MdLabel className="mr-[3px] text-green-500" />
                            <span>Tags</span>
                        </div>
                        <div className="flex items-center mr-[15px] cursor-pointer">
                            <MdEmojiEmotions className="mr-[3px] text-yellow-500" />
                            <span>Emojis</span>
                        </div>
                        <div className="flex items-center mr-[15px] cursor-pointer">
                            <MdLocationPin className="mr-[3px] text-red-500" />
                            <span>Location</span>
                        </div>
                    </div>
                    <button onClick={handleSubmit} className="bg-blue-700 text-white p-[7px] rounded-lg font-bold">Upload</button>
                </div>
            </div>
        </div>
    );
};

export default UploadPost;
