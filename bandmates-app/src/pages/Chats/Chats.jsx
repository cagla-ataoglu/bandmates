import React, { useState, useEffect, useRef } from 'react';
import ChatMessages from '../../components/ChatMessages/ChatMessages';
import SendChatMessage from '../../components/SendChatMessage/SendChatMessage';
import ReconnectingWebSocket from 'reconnecting-websocket';
import CreateChat from '../../components/CreateChat/CreateChat';
import './Chats.css';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';

function Chats() {
    const navigate = useNavigate();

    useEffect(() => {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        navigate('/login');
      }
    }, [navigate]);
    const [chats, setChats] = useState([]);
    const [currentChatId, setCurrentChatId] = useState(null);
    const [messages, setMessages] = useState([]);
    const ws = useRef(null);

    useEffect(() => {
        ws.current = new ReconnectingWebSocket(`${import.meta.env.VITE_MESSAGE_WS}/ws`);
        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.chat_id === currentChatId) {
                setMessages(prev => [...prev, data]);
            } else {
                setChats(prev => prev.map(chat => {
                    if (chat.chat_id === data.chat_id) {
                        return { ...chat, new: 'true' };
                    }
                    return chat;
                }));
            }
        };

        const fetchUserChats = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_MESSAGE_API}/get_user_chats`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: localStorage.getItem('username')
                    })
                });
                if (response.ok) {
                    const data = await response.json();
                    console.log(data.chats);
                    setChats(data.chats);
                    data.chats.forEach(chat => {
                        ws.current.send(JSON.stringify({ action: "join", chat_id: chat.chat_id }));
                    });
                } else {
                    console.error('Error fetching chats:', error)
                }
            } catch (error) {
                console.error('Error fetching chats:', error)
            }
        };
        fetchUserChats();

        return () => ws.current.close();
    }, [currentChatId]);

    const joinRoom = (chatId) => {
        setCurrentChatId(chatId);
        setMessages([]);

        const fetchMessages = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_MESSAGE_API}/get_messages`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        chat_id: chatId
                    })
                });
                if (response.ok) {
                    const data = await response.json();
                    setMessages(data.messages);
                    setChats(chats => chats.map(chat => {
                        if (chat.chat_id === chatId) return { ...chat, new: 'false' };
                        return chat;
                    }));
                } else {
                    console.error('Fetching messages failed:', error)
                }
            } catch (error) {
                console.error('Fetching messages failed:', error)
            }
        };
        fetchMessages();
    };

    return (
        <>
            <Navbar />
            <div className="chats-container">
                <CreateChat onChatCreated={(chat_id) => {
                    joinRoom(chat_id);
                    ws.current.send(JSON.stringify({ action: "join", chat_id: chat_id }));
                }} />
                <div className="chats-list">
                    <h2>Chats</h2>
                    <ul>
                        {chats.sort((a, b) => b.new - a.new).map(chat => (
                            <li key={chat.chat_id} onClick={() => joinRoom(chat.chat_id)} className={chat.new ? 'chat-new' : ''}>
                                {chat.chat_name} {chat.new == 'true' && '🔔'}
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="chat-window">
                    <h2>Current Chat: {currentChatId ? chats.find(chat => chat.chat_id === currentChatId)?.chat_name : 'Select a chat'}</h2>
                    <ChatMessages messages={messages} />
                    <SendChatMessage onSendMessage={message => {
                        const sendMessage = JSON.stringify({
                            action: 'message',
                            chat_id: currentChatId,
                            username: localStorage.getItem('username'),
                            message: message
                        });
                        ws.current.send(sendMessage);
                    }} />
                </div>
            </div>
        </>
    );
}

export default Chats;
