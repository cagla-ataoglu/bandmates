import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar'
import OtherUserCard from '../../components/OtherUserCard/OtherUserCard'

function OtherUser() {
    const { username } = useParams();
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
            <OtherUserCard username={username} />
        </div>
        </>
    )
}

export default OtherUser;
