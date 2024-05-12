import React, { useState, useEffect } from 'react';
import './CreateChat.css';

function CreateChat({ onChatCreated }) {
    const [usernames, setUsernames] = useState('');
    const [chatName, setChatName] = useState('');
    const [creating, setCreating] = useState(false);

    useEffect(() => {
        const currentUser = localStorage.getItem('username');
        setUsernames(currentUser);
    }, []);

    const handleCreateClick = async () => {
        setCreating(true);
        try {
            const response = await fetch(`${import.meta.env.VITE_MESSAGE_API}/create_chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    usernames: [usernames, ...usernames.split(',')].map(username => username.trim()).filter(Boolean),
                    chat_name: chatName,
                    is_group: usernames.split(',').length > 1
                })
            });
            if (response.ok) {
                const data = await response.json();
                onChatCreated(data.chat_id);
                setUsernames('');
                setChatName('');
                setCreating(false);
                return data;
            } else {
                throw new Error('Failed to create chat');
            }
        } catch (error) {
            console.error('Failed to create chat:', error);
            setCreating(false);
        }
    };

    return (
        <div className="create-chat-container">
            <div className="create-chat-header">Create a new chat</div>
            <input
                className="chat-input"
                type="text"
                value={chatName}
                onChange={e => setChatName(e.target.value)}
                placeholder="Enter chat name"
                disabled={creating}
            />
            <div className="usernames-label">Add users (separated by commas):</div>
            <input
                className="usernames-input"
                type="text"
                value={usernames}
                onChange={e => setUsernames(e.target.value)}
                placeholder="Add more users, separated by commas"
                disabled={creating}
            />
            <button className="create-button" onClick={handleCreateClick} disabled={creating}>
                {creating ? 'Creating...' : 'Create Group Chat'}
            </button>
        </div>
    );
}

export default CreateChat;
