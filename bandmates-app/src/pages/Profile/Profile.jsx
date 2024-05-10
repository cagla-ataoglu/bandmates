import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar'
import ProfileCard from '../../components/ProfileCard/ProfileCard'

const Profile = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      navigate('/login');
    }
  }, [navigate]);

  return (
    <>
      <Navbar />
      <div className="flex">
        <ProfileCard username={localStorage.getItem('username')} />
      </div>
    </>
  )
}

export default Profile