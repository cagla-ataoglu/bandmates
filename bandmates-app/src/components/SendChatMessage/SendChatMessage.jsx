import React, { useState } from 'react';
import './SendChatMessage.css';

const SendChatMessage = ({ onSendMessage }) => {
    const [message, setMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        if (message.trim()) {
            onSendMessage(message.trim());
            setMessage('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="send-message-form">
            <input
                className="message-input"
                type="text"
                value={message}
                onChange={e => setMessage(e.target.value)}
                placeholder="Type a message..."
                autoFocus
            />
            <button className="send-button" type="submit">Send</button>
        </form>
    );
};

export default SendChatMessage;
