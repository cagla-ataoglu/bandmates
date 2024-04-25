import React from 'react';
import './ProfileCard.css'

const ProfileCard = () => {
    return(
        <div className="custom-container">
            <div className='pc'>
                <div className="gradiant"></div>
                <div className="profile-down">
                    <img src="" alt="" />
                    <div className="profile-title">Name</div> {/* username or display name */}
                    <div className="profile-information">Profile Type</div> {/* band or musician */}
                    <div className="profile-information">Location</div>
                    <div className="profile-description">Profile Description</div> {/* a description of their profile given by the user */}
                    <div className="profile-button"><a href="mailto: user@email">Contact Me</a></div> {/* put here the link to msg function or email */}

                </div>
            </div>
        </div>
    )
}

export default ProfileCard