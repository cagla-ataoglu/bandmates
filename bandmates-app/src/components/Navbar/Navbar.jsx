import React, { useState, useEffect, useRef } from 'react';
import './Navbar.css';
import Logo from '../Logo/Logo';
import { IoChatboxEllipsesSharp, IoPersonSharp, IoSearch, IoSettingsSharp, IoNotifications } from "react-icons/io5";
import { FaHome, FaGuitar } from "react-icons/fa";
import profilePic from "../../assets/musician_pfp.jpg";
import { useNavigate } from 'react-router-dom';
import debounce from 'lodash.debounce';

const Navbar = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const searchRef = useRef(null);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const fetchSearchResults = async (prefix) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/search_profiles_by_prefix`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prefix })
      });
      const data = await response.json();
      if (data.status === 'success') {
        setResults(data.profiles);
        setIsDropdownVisible(true);
      } else {
        setResults([]);
        setIsDropdownVisible(false);
      }
    } catch (error) {
      console.error('Error fetching search results:', error);
      setResults([]);
      setIsDropdownVisible(false);
    }
  };

  const debouncedSearch = debounce((input) => {
    if (input.length > 1) {
      fetchSearchResults(input);
    } else {
      setResults([]);
      setIsDropdownVisible(false);
    }
  }, 300);

  useEffect(() => {
    debouncedSearch(searchTerm);
    return debouncedSearch.cancel;
  }, [searchTerm]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setIsDropdownVisible(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [searchRef]);

  return (
    <div className="navbar">
      <div className="left">
        <Logo size={30}/>
        <div className="searchBar" ref={searchRef}>
          <IoSearch className="searchIcon" />
          <input
            type="text"
            className="searchInput"
            placeholder="Search users..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {isDropdownVisible && (
            <div className="searchResults">
              {results.map((profile, idx) => (
                <div key={idx} className="searchResultItem" onClick={() => {
                  navigate(`/users/${profile.username}`);
                  setIsDropdownVisible(false);
                }}>
                  {profile.display_name || profile.username}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <div className="right">
        <div className="tabIcons">
          <div className="tabIcon" onClick={() => navigate('/')}>
            <FaHome size={25} />
            <div className="tabText" >Home</div>
          </div>
          <div className="tabIcon" onClick={() => navigate('/gigs')}>
            <FaGuitar size={25} />
            <div className="tabText">Gigs</div>
          </div>
          <div className="tabIcon" onClick={() => navigate('/chats')}>
            <IoChatboxEllipsesSharp size={25} />
            <div className="tabText">Chats</div>
          </div>
        </div>
        <div className="profilePicDiv" onClick={() => navigate('/profile')}>
          <img src={profilePic} alt="" className="profilePic" />
        </div>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Navbar;
