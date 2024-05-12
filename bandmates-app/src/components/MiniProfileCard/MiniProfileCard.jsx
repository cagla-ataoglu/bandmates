import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types'; // Import PropTypes
import './MiniProfileCard.css';

const MiniProfileCard = ({ username }) => {
    const [profileData, setProfileData] = useState(null);

    const fetchProfileData = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/get_profile`, {
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

    return (
        <div className="mpc-container">
            <div className='mpc-pc'>
                <div className="gradiant" style={{ height: '50px' }}></div>
                <div className="profile-down">
                    {profileData && (
                        <>
                            <img src={profileData.profile_picture} alt="" style={{ height: '75px', width: '75px' }} />
                            <div className="profile-title" style={{ fontSize: '14px' }}>{profileData.display_name}</div>
                            <div className="profile-information" style={{ fontSize: '12px' }}>{profileData.profile_type}</div>
                            <div className="profile-information" style={{ fontSize: '12px' }}>{profileData.location}</div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

// Prop type validation
MiniProfileCard.propTypes = {
    username: PropTypes.string.isRequired,
};
  
export default MiniProfileCard;
