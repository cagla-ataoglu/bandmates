import React from 'react';
import { FaPhotoVideo, FaBookmark, FaCalendarAlt } from 'react-icons/fa';
import { MdGroups } from 'react-icons/md';
import profilePic from '../../assets/janedoe_pfp.jpg';
import './Leftbar.css';

const Sidebar = () => {
    return (
        <div className="sidebar-container">
            <div className="sidebar-card">
                <div className="sidebar-wrapper">
                    <ul className="sidebarList">
                        <li>
                            <FaPhotoVideo />
                            <span>Videos</span>
                        </li>
                        <li>
                            <MdGroups />
                            <span>Groups</span>
                        </li>
                        <li>
                            <FaBookmark />
                            <span>Bookmarks</span>
                        </li>
                        <li>
                            <FaCalendarAlt />
                            <span>Events</span>
                        </li>
                    </ul>
                    <button className="button">
                        See more
                    </button>
                    <hr />
                    <div className="profile-list">
                        <ul className="sidebarList">
                            {[...Array(10)].map((_, index) => (
                            <li key={index}>
                                <img src={profilePic} alt="profileImage" />
                                <span>James Escobar</span>
                            </li>
                        ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
);};

export default Sidebar;
