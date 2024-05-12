import React, { useState, useEffect } from 'react';
import './ChatMessages.css';


const ChatMessages = ({ messages }) => {
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        const username = localStorage.getItem('username');
        setCurrentUser(username);
    }, []);

    return (
        <div className="messages-display">
            <ul>
                {messages.map((msg, index) => (
                    <li key={index} 
                        className={msg.username === currentUser ? "my-message" : "other-message"}>
                        <strong>{msg.username}:</strong> {msg.message}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ChatMessages;
