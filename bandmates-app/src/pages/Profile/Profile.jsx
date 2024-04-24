import React from 'react'
import Navbar from '../../components/Navbar/Navbar'
import Sidebar from '../../components/Sidebar/Sidebar'
import Rightbar from '../../components/Rightbar/Rightbar'
import ProfileCard from '../../components/ProfileCard/ProfileCard'

const Profile = () => {
  return (
    <>
      <Navbar />
      <div className="flex">
        <ProfileCard />
      </div>
    </>
  )
}

export default Profile