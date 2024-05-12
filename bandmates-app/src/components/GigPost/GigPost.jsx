import React, { useState, useEffect, useRef } from 'react';

const GigPost = ({ post }) => {
    const { GigName, GigDate, BandUsername, Genre, Venue, LookingFor, Timestamp } = post;

    useEffect(() => {
        console.log(post)
    }, []);

    return (
        <div className='post-container'>
            <div className='p-[10px]'>
                <div className="post-header">
                    <div className='post-user-info'>
                        <span className='post-username'>{BandUsername}</span>
                        <span className='post-timestamp'>{new Date(Timestamp).toLocaleString()}</span>
                    </div>
                </div>
                <div className="post-content">
                    <p><strong>{GigName}</strong></p>
                    <p>Date: {GigDate}</p>
                    <p>Genre: {Genre}</p>
                    <p>Venue: {Venue}</p>
                    <p>Looking for: {LookingFor}</p>
                </div>
            </div>
        </div>
    );
};

export default GigPost;