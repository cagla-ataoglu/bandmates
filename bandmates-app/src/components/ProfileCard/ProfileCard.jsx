import React, { useState, useEffect } from 'react';
import profilePic from '../../assets/janedoe_pfp.jpg';
import './ProfileCard.css';
import { MdEditNote } from "react-icons/md";
import { IoIosCloseCircleOutline } from "react-icons/io";

const ProfileCard = ({ username }) => {
    const [profileData, setProfileData] = useState(null);
    const profile_img = profilePic;
    const [editedName, setEditedName] = useState('');
    const [editedLocation, setEditedLocation] = useState('');
    const [editProfilePopUp, setEditProfilePopUp] = useState(false);

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

    const editDisplayName = async () => {
        try {
            const response = await fetch('http://localhost:8081/update_display_name', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    display_name: editedName
                })
            });
            const data = await response.json()
            if (response.ok) {
                console.log('Display name updated.');
                window.location.reload();
            } else {
                console.log('Failed to update display name:', data.message);
            }
        } catch (error) {
            console.log('Error updating display name:', error)
        }
    }

    const editLocation = async () => {
        try {
            const response = await fetch('http://localhost:8081/update_location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    location: editedLocation
                })
            });
            const data = await response.json()
            if (response.ok) {
                console.log('Location updated.');
                window.location.reload();
            } else {
                console.log('Failed to update location:', data.message);
            }
        } catch (error) {
            console.log('Error updating location:', error)
        }
    }

    const addGenre = async () => {
        try {
            const response = await fetch('http://localhost:8081/add_genre', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username
                })
            });
            const data = await response.json()
            if (response.ok) {
                console.log(`Genre added.`);
                window.location.reload();
            } else {
                console.log('Failed to add genre:', data.message);
            }
        } catch (error) {
            console.log('Error adding genre:', error)
        }
    }

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
        editDisplayName();
        editLocation();       
        setEditProfilePopUp(false);
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
