import React from 'react'
import { FaPhotoVideo, FaBookmark, FaCalendarAlt } from "react-icons/fa";
import { MdGroups } from "react-icons/md";
import ProfileCard from '../../components/ProfileCard/ProfileCard'
import profilePic from "../../assets/janedoe_pfp.jpg"

const Sidebar = () => {
  return (
    <div style={{flex: 2, height:"calc(100vh - 50px)"}} className="custom-scrollbar overflow-y-auto">
        <div className="p-[20px]">
            <ul className="sidebarList m-0 p-0">
                <li>
                <FaPhotoVideo/>
                <span>Videos</span>
                </li> 
                <li>
                <MdGroups/>
                <span>Groups</span>
                </li> 
                <li>
                <FaBookmark/>
                <span>Bookmarks</span>
                </li>
                <li>
                <FaCalendarAlt/>
                <span>Events</span>
                </li> 
            </ul>
            <div className="button">
                <button className="rounded-md bg-slate-300 w-[150px] p-[10px]">See More</button>
            </div>
            <hr className="mt-[20px]"/>
            <div className="mt-[20px]">
                <ul className="sidebarList">
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    <li>
                        <img src={profilePic} alt="profileImage" className="w-[32px] h-[32px] rounded-full object-cover"/>
                        <span>James Escobar</span>
                    </li>
                    
                </ul>
            </div>
        </div>
    </div>
  )
}

export default Sidebar