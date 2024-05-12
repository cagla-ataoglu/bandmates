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
    const [genres, setGenres] = useState([]);

    const [newInstrument, setNewInstrument] = useState('');
    const [instruments, setInstruments] = useState([]);

    const [newMember, setNewMember] = useState('');
    const [members, setMembers] = useState([]);

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
                if (data.genres) {
                    setGenres(data.genres);
                }
                if (data.instruments) {
                    setInstruments(data.instruments);
                }
                if (data.members) {
                    setMembers(data.members)
                }
            } else {
                console.error(`Failed to fetch profile data for ${username}`);
            }
        } catch (error) {
            console.error('Error fetching profile data:', error);
        }
    };

    const editDisplayName = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/update_display_name`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    display_name: editedName
                })
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Display name updated.');
                window.location.reload();
            } else {
                console.log('Failed to update display name:', data.message);
            }
        } catch (error) {
            console.log('Error updating display name:', error);
        }
    }

    const editLocation = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/update_location`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    location: editedLocation
                })
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Location updated.');
                window.location.reload();
            } else {
                console.log('Failed to update location:', data.message);
            }
        } catch (error) {
            console.log('Error updating location:', error);
        }
    }

    const addGenre = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/add_genre`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    genre: newGenre
                })
            });
            const data = await response.json()
            if (response.ok) {
                console.log(`Genre added.`);
                setGenres([...genres, newGenre]);
                setNewGenre('');
            } else {
                console.log('Failed to add genre:', data.message);
            }
        } catch (error) {
            console.log('Error adding genre:', error);
        }
    }

    const removeGenre = async (genre) => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/remove_genre`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    genre: genre
                })
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Genre removed.')
                setGenres(genres.filter(g => g !== genre));
            } else {
                console.log('Failed to remove genre:', data.message);
            }
        } catch (error) {
            console.log('Error removing genre:', error)
        }
    }

    const addInstrument = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/add_instrument`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    instrument: newInstrument
                })
            });
            const data = await response.json()
            if (response.ok) {
                console.log(`Instrument added.`);
                setInstruments([...instruments, newInstrument]);
                setNewInstrument('');
            } else {
                console.log('Failed to add instrument:', data.message);
            }
        } catch (error) {
            console.log('Error adding instrument:', error);
        }
    }

    const removeInstrument = async (instrument) => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/remove_instrument`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    instrument: instrument
                })
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Instrument removed.')
                setInstruments(instruments.filter(ins => ins !== instrument));
            } else {
                console.log('Failed to remove instrument:', data.message);
            }
        } catch (error) {
            console.log('Error removing instrument:', error)
        }
    }

    const addMember = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/add_member`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    member: newMember
                })
            });
            const data = await response.json()
            if (response.ok) {
                console.log(`Member added.`);
                setMembers([...members, newMember]);
                setNewMember('');
            } else {
                console.log('Failed to add member:', data.message);
            }
        } catch (error) {
            console.log('Error adding member:', error);
        }
    }

    const removeMember = async (member) => {
        try {
            const response = await fetch(`${import.meta.env.VITE_PROFILE_API}/remove_member`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    member: member
                })
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Member removed.')
                setMembers(members.filter(mem => mem !== member));
            } else {
                console.log('Failed to remove member:', data.message);
            }
        } catch (error) {
            console.log('Error removing member:', error)
        }
    }

    useEffect(() => {
        fetchProfileData();
    }, [username]);

    const editProfile = () => {
        setEditProfilePopUp(!editProfilePopUp);
        fetchProfileData();
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

    const handleAddGenre = () => {
        if (newGenre.trim()) {
            addGenre(); 
            setNewGenre(''); 
        }
    };

    const handleRemoveGenre = (genre) => {
        removeGenre(genre);
    };

    const handleAddInstrument = () => {
        if (newInstrument.trim()) {
            addInstrument(); 
            setNewInstrument(''); 
        }
    };

    const handleRemoveInstrument = (genre) => {
        removeInstrument(genre);
    };

    const handleAddMember = () => {
        if (newMember.trim()) {
            addMember(); 
            setNewMember(''); 
        }
    };

    const handleRemoveMember = (member) => {
        removeMember(member);
    };

    return (
        <div className="custom-container">
            <div className='pc'>
                <div className="gradiant"></div>
                <div className="profile-down">
                    {profileData && (
                        <>
                            <img src={profileData.profile_picture} alt="" />
                            <div className="profile-information">{username}</div>
                            <div className="profile-title">Name: {profileData.display_name}</div>
                            <div className="profile-information">Profile type: {profileData.profile_type}</div>
                            <div className="profile-information">Location: {profileData.location}</div>
                            {profileData.genres && (
                                <div className="profile-information">Genres: {profileData.genres.join(', ')}</div>
                            )}
                            {profileData.profile_type === "band" && profileData.members && (
                                <div className="profile-information">Members: {profileData.members.join(', ')}</div>
                            )}
                            {profileData.profile_type === "musician" && profileData.instruments && (
                                <div className="profile-information">Instruments: {profileData.instruments.join(', ')}</div>
                            )}
                            {/* <div className="profile-description">{profileData.profile_description}</div> */}
                            {/* <div className="profile-button"><a href={`mailto:${profileData.email}`}>Contact Me</a></div> */}
                        </>
                    )}
                    <div className="edit-button">
                        <button onClick={editProfile}><MdEditNote className="icon" />
                            <span className="text">Edit Profile</span>
                        </button>
                    </div>
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
                                    {genres && genres.map((genre, index) => (
                                        <div key={index} className="genre-item">
                                        <span>{genre}</span>
                                        <button onClick={() => handleRemoveGenre(genre)} className="remove-button"><IoMdClose /></button>
                                    </div>
                                    ))}
                                    
                                </div>
                            </div>
                        </div>
                        {profileData.profile_type == 'musician' && <div className="input-container">
                            <label htmlFor="instrument">Instrument:</label>
                            <div className="genre-container">
                                <div className="genre-input-container">
                                    <input
                                        type="text"
                                        id="instrument"
                                        value={newInstrument}
                                        onChange={(e) => setNewInstrument(e.target.value)}
                                        className="text-input"
                                        placeholder="Enter an instrument..."
                                    />
                                    <button onClick={handleAddInstrument} className="add-button">Add</button>
                                </div>
                                <div className="genre-item-container">
                                    {instruments && instruments.map((instrument, index) => (
                                        <div key={index} className="genre-item">
                                        <span>{instrument}</span>
                                        <button onClick={() => handleRemoveInstrument(instrument)} className="remove-button"><IoMdClose /></button>
                                    </div>
                                    ))}
                                    
                                </div>
                            </div>
                        </div>}
                        {profileData.profile_type == 'band' && <div className="input-container">
                            <label htmlFor="member">Member:</label>
                            <div className="genre-container">
                                <div className="genre-input-container">
                                    <input
                                        type="text"
                                        id="instrument"
                                        value={newMember}
                                        onChange={(e) => setNewMember(e.target.value)}
                                        className="text-input"
                                        placeholder="Enter a member name..."
                                    />
                                    <button onClick={handleAddMember} className="add-button">Add</button>
                                </div>
                                <div className="genre-item-container">
                                    {members && members.map((member, index) => (
                                        <div key={index} className="genre-item">
                                        <span>{member}</span>
                                        <button onClick={() => handleRemoveMember(member)} className="remove-button"><IoMdClose /></button>
                                    </div>
                                    ))}
                                    
                                </div>
                            </div>
                        </div>}
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
