import React from 'react';
import './ProfileCard.css'

const ProfileCard = () => {
    return(
        <div className="custom-container">
            <div className='pc'>
                <div className="gradiant"></div>
                <div className="profile-down">
                    <img src="" alt="" />
                    <div className="profile-title">Profile title here</div>
                    <div className="profile-description">Profile information here</div>
                    <div className="profile-button"><a href="mailto: user@email">Contact Me (link to email here)</a></div>
                </div>
            </div>
        </div>
    )
}

export default ProfileCard