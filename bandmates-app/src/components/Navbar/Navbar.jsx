import React from 'react';
import './Navbar.css';
import Logo from '../Logo/Logo';
import { IoChatboxEllipsesSharp, IoPersonSharp, IoSearch, IoSettingsSharp, IoNotifications } from "react-icons/io5";
import { FaHome, FaGuitar } from "react-icons/fa";
import profilePic from "../../assets/musician_pfp.jpg";

const Navbar = () => {
  return (
    <div className="navbar">
      <div className="left">
        <Logo />
        <div className="searchBar">
          <IoSearch className="searchIcon" />
          <input type="text" className="searchInput" />
        </div>
      </div>
      <div className="right">
        <div className="tabIcons">
          <div className="tabIcon">
            <FaHome size={25} />
            <div className="tabText">Home</div>
          </div>
          <div className="tabIcon">
            <IoPersonSharp size={25} />
            <span className="badge">1</span>
            <div className="tabText">Contacts</div>
          </div>
          <div className="tabIcon">
            <FaGuitar size={25} />
            <span className="badge">1</span>
            <div className="tabText">Gigs</div>
          </div>
          <div className="tabIcon">
            <IoChatboxEllipsesSharp size={25} />
            <span className="badge">2</span>
            <div className="tabText">Messages</div>
          </div>
          <div className="tabIcon">
            <IoNotifications size={25} />
            <span className="badge">5</span>
            <div className="tabText">Notifications</div>
          </div>
          <div className="tabIcon">
            <IoSettingsSharp size={25} />
            <div className="tabText">Settings</div>
          </div>
        </div>
        <div className="profilePicDiv">
          <img src={profilePic} alt="" className="profilePic" />
        </div>
      </div>
    </div>
  );
};

export default Navbar;
