import React from 'react';
import { FaBookmark, FaCalendarAlt } from 'react-icons/fa';
import { MdGroups } from 'react-icons/md';
import { FaListUl } from "react-icons/fa6";
import './GigsBar.css';

const GigsBar = () => {
    return (
        <div className="gigsbar-container">
            <div className="gigsbar-card">
                <div className="gigsbar-wrapper">
                    <ul className="gigsbarList">
                        <li>
                            <FaBookmark />
                            <span>My Gigs</span>
                        </li>
                        <li>
                            <FaListUl />
                            <span>Preferences</span>
                        </li>
                        <li>
                            <MdGroups />
                            <span>Groups</span>
                        </li>
                        <li>
                            <FaCalendarAlt />
                            <span>Events</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
);};

export default GigsBar;
