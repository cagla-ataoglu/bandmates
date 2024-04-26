import React from 'react'
import Logo from '../Logo/Logo'
import { IoChatboxEllipsesSharp, IoPersonSharp, IoSearch } from "react-icons/io5";
import { FaHome } from "react-icons/fa";
import { IoChatbubbleEllipsesSharp } from "react-icons/io5";
import { IoNotifications } from "react-icons/io5";
import { IoSettingsSharp } from "react-icons/io5";
import profilePic from "../../assets/musician_pfp.jpg"

const Navbar = () => {
  return (
    <div className="h-[50px] w-full bg-blue-800 flex items-center sticky top-0">
        <div className="left" style={{flex: 3}}>
            <div className="logodiv">
                <Logo/>
            </div>

        </div>
        <div className="center" style={{flex: 5}}>
            <div className="searchBar w-[550px] h-[30px] bg-white rounded-xl flex items-center">
                <IoSearch className=" text-lg ml-[10px]"/>
                <input type="text" className="search w-full focus:outline-none bg-none mr-[10px]" />
            </div>
        </div>
        <div className="right flex items-center jutisfy-around text-white" style={{flex:2}}>
            {/* <div className="tabLinks text-lg cursor-pointer flex gap-[10px]">
                <span className="tabLink1 font-bold">Home</span>
                <span className="tabLink2">Messages</span>
                <span className="tabLink3">Notifications</span>
                <span className="tablink4">Profile</span>
                <span className="tabLink4 font-bold">Settings</span>
            </div> */}
            <div className="tabIcons flex">
                <div className="tabIcon1 cursor-pointer relative mr-[10px]">
                    <FaHome size={25}/>
                </div>
                <div className="tabIcon2 cursor-pointer relative mr-[10px]">
                    <IoPersonSharp size={25}/>
                    <span className="w-[15px] h-[15px] bg-red-600 rounded-full text-white absolute top-[-1px] right-[-10px] flex items-center justify-center text-xs transform -translate-x-1/2 -translate-y-1/2">1</span>
                </div>
                <div className="tabIcon3 cursor-pointer relative mr-[10px]">
                    <IoChatboxEllipsesSharp size={25}/>
                    <span className="w-[15px] h-[15px] bg-red-600 rounded-full text-white absolute top-[-1px] right-[-10px] flex items-center justify-center text-xs transform -translate-x-1/2 -translate-y-1/2">2</span>
                </div>
                <div className="tabIcon4 cursor-pointer relative mr-[10px]">
                    <IoNotifications size={25}/>
                    <span className="w-[15px] h-[15px] bg-red-600 rounded-full text-white absolute top-[-1px] right-[-10px] flex items-center justify-center text-xs transform -translate-x-1/2 -translate-y-1/2">5</span>
                </div>
                <div className="tabIcon5 cursor-pointer relative mr-[10px]">
                    <IoSettingsSharp size={25}/>
                </div>
            </div>
            <div className="profilePicDiv">
                <img src={profilePic} alt="" className="w-[30px] h-[30px] object-cover rounded-full ml-[10px]"/>
            </div>
        </div>
    </div>
  )
}

export default Navbar