import React, { useState } from 'react';
import axios from 'axios';

function CreateChat({ onChatCreated }) {
    const [usernames, setUsernames] = useState('');
    const [chatName, setChatName] = useState('');
    const [creating, setCreating] = useState(false);

    const handleCreateClick = async () => {
        setCreating(true);
        try {
            const response = await fetch(`${import.meta.env.VITE_MESSAGE_API}/create_chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    usernames: usernames.split(',').map(username => username.trim()),
                    chat_name: chatName,
                    is_group: usernames.split(',').length > 2
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
                console.error('Failed to create chat:', error);
                setCreating(false);
            }
        } catch (error) {
            console.error('Failed to create chat:', error);
            setCreating(false);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={chatName}
                onChange={e => setChatName(e.target.value)}
                placeholder="Enter chat name"
                disabled={creating}
            />
            <input
                type="text"
                value={usernames}
                onChange={e => setUsernames(e.target.value)}
                placeholder="Enter usernames, separated by commas"
                disabled={creating}
            />
            <button onClick={handleCreateClick} disabled={creating}>
                {creating ? 'Creating...' : 'Create Group Chat'}
            </button>
        </div>
    );
}

export default CreateChat;
