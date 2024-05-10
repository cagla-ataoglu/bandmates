import React, { useState, useEffect } from 'react';
import profilePic from '../../assets/janedoe_pfp.jpg';
import './ProfileCard.css';
import { MdEditNote } from "react-icons/md";
import { IoIosCloseCircleOutline, IoMdClose } from "react-icons/io";

const ProfileCard = ({ username }) => {
    const [profileData, setProfileData] = useState(null);
    const profile_img = profilePic;
    const [editedName, setEditedName] = useState('');
    const [editedLocation, setEditedLocation] = useState('');
    const [editProfilePopUp, setEditProfilePopUp] = useState(false);
    const [newGenre, setNewGenre] = useState('');

    const dummyGenre = ['Rock']; 
    const [genres, setGenres] = useState(dummyGenre);

    const fetchProfileData = async () => {
        try {
            const response = await fetch(`http://localhost:8081/get_profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username
                })
            });
            if (response.ok) {
                const data = await response.json();
                setProfileData(data);
            } else {
                console.error(`Failed to fetch profile data for ${username}`);
            }
        } catch (error) {
            console.error('Error fetching profile data:', error);
        }
    };

    useEffect(() => {
        fetchProfileData();
    }, [username]);

    const editProfile = () => {
        setEditProfilePopUp(!editProfilePopUp);
        if (profileData) {
            setEditedName(profileData.display_name);
            setEditedLocation(profileData.location);
        }
    };

    const handleChangeName = (e) => {
        setEditedName(e.target.value);
    };

    const handleChangeLocation = (e) => {
        setEditedLocation(e.target.value);
    };

    const handleSave = () => {
        // D:
        setEditProfilePopUp(false);
    };

    const handleAddGenre = () => {
        if (newGenre.trim()) { 
            setGenres([...genres, newGenre]); 
            setNewGenre(''); 
          }
    };

    const removeGenre = () => {

    };

    return (
        <div className="custom-container">
            <div className='pc'>
                <div className="gradiant"></div>
                <div className="edit-button">
                    <button onClick={editProfile}><MdEditNote className="icon" />
                        <span className="text">Edit Profile</span>
                    </button>
                </div>
                <div className="profile-down">
                    {profileData && (
                        <>
                            <img src={profileData.profile_picture} alt="" />
                            <div className="profile-information">{username}</div>
                            <div className="profile-title">Name: {profileData.display_name}</div>
                            <div className="profile-information">Profile type: {profileData.profile_type}</div>
                            <div className="profile-information">Location: {profileData.location}</div>
                            <div className="profile-information">Genres: {profileData.genres}</div>
                            {profileData.profile_type === "band" && profileData.members && (
                                <div className="profile-information">Members: {profileData.members.join(', ')}</div>
                            )}
                            {profileData.profile_type === "musician" && profileData.instrument && (
                                <div className="profile-information">Instruments: {profileData.instruments.join(', ')}</div>
                            )}
                            {profileData.genres && (
                                <div className="profile-information">{profileData.genres.join(', ')}</div>
                            )}
                            {/* <div className="profile-description">{profileData.profile_description}</div> */}
                            {/* <div className="profile-button"><a href={`mailto:${profileData.email}`}>Contact Me</a></div> */}
                        </>
                    )}
                </div>
            </div>
            {editProfilePopUp && (
                <div className="edit-popup">
                    <div className="edit-popup-inner">
                        <div className="edit-popup-header">
                            <h2>Edit Profile</h2>
                            <button onClick={editProfile} className="close-button">
                                <IoIosCloseCircleOutline />
                            </button>
                        </div>
                        <hr className="divider" />
                        <div className="input-container">
                            <label htmlFor="name">Name:</label>
                            <input
                                type="text"
                                id="name"
                                value={editedName}
                                onChange={handleChangeName}
                                className="text-input"
                            />
                        </div>
                        <div className="input-container">
                            <label htmlFor="location">Location:</label>
                            <input
                                type="text"
                                id="location"
                                value={editedLocation}
                                onChange={handleChangeLocation}
                                className="text-input"
                            />
                        </div>
                        <div className="input-container">
                            <label htmlFor="genre">Genre:</label>
                            <div className="genre-container">
                                <div className="genre-input-container">
                                    <input
                                        type="text"
                                        id="genre"
                                        value={newGenre}
                                        onChange={(e) => setNewGenre(e.target.value)}
                                        className="text-input"
                                        placeholder="Enter a genre..."
                                    />
                                    <button onClick={handleAddGenre} className="add-button">Add</button>
                                </div>
                                <div className="genre-item-container">
                                    <div key={0} className="genre-item">
                                        <span>{dummyGenre}</span>
                                        <button onClick={removeGenre} className="remove-button"><IoMdClose /></button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="button-container">
                            <button onClick={handleSave} className="save-button">Save</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ProfileCard;
