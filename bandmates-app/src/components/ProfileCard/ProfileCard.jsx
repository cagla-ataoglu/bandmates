import React, { useState, useEffect } from 'react';
import profilePic from '../../assets/janedoe_pfp.jpg';
import './ProfileCard.css';

const ProfileCard = ({ username }) => {
    const [profileData, setProfileData] = useState(null);
    const profile_img = profilePic;

    const fetchProfileData = async () => {
        try {
            const formData = new FormData();
            formData.append('username', username)
            const response = await fetch(`http://localhost:8081/get_profile/${username}`, {
                method: 'GET',
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

    return (
        <div className="custom-container">
            <div className='pc'>
                <div className="gradiant"></div>
                <div className="profile-down">
                    {profileData && (
                        <>
                            <img src={profileData.profile_picture} alt="" />
                            <div className="profile-title">{profileData.display_name}</div>
                            <div className="profile-information">{profileData.profile_type}</div>
                            <div className="profile-information">{profileData.location}</div>
                            <div className="profile-information">{profileData.genres}</div>
                            {profileData.profile_type === "band" && profileData.members && (
                                <div className="profile-information">Members: {profileData.members.join(', ')}</div>
                            )}
                            {profileData.profile_type === "musician" && profileData.instrument && (
                                <div className="profile-information">{profileData.instruments.join(', ')}</div>
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
        </div>
    );
};

export default ProfileCard;
