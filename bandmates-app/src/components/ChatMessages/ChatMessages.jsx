import React from 'react';

const ChatMessages = ({ messages }) => {
    return (
        <div className="messages-display">
            <ul>
                {messages.map((msg, index) => (
                    <li key={index} className={msg.sender_id === "your_user_id" ? "my-message" : "other-message"}>
                        <strong>{msg.sender_id}:</strong> {msg.message}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ChatMessages;
