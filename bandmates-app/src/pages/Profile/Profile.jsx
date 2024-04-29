import React from 'react'
import Navbar from '../../components/Navbar/Navbar'
import ProfileCard from '../../components/ProfileCard/ProfileCard'

const Profile = () => {
  return (
    <>
      <Navbar />
      <div className="flex">
        <ProfileCard username={"thebeatles"} />
      </div>
    </>
  )
}

export default Profile