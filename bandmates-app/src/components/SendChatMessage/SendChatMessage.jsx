import React, { useState } from 'react';

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
                type="text"
                value={message}
                onChange={e => setMessage(e.target.value)}
                placeholder="Type a message..."
                autoFocus
            />
            <button type="submit">Send</button>
        </form>
    );
};

export default SendChatMessage;
