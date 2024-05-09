import React, { useState, useEffect } from 'react';
import './Login.css';
import Logo from '../../components/Logo/Logo';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [showPopup, setShowPopup] = useState(false);
    const [popupMessage, setPopupMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await fetch('http://localhost:8080/signin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('access_token', data.tokens.access_token);
                localStorage.setItem('refresh_token', data.tokens.refresh_token);
              
                setShowPopup(true);
                setPopupMessage('Login successful');
                navigate('/');
            } else {
                setShowPopup(true);
                setPopupMessage('Login failed. ' + data.message);
            }
        } catch (error) {
            setShowPopup(true);
            setPopupMessage(`Login failed: ${error.message}`);
        }
    };

    const closePopup = () => {
        setShowPopup(false);
        setPopupMessage('');
    };

    return (
        <div className="login-container">
            <div className="content">
                <div className="left-content">
                    <Logo />
                    <span className="login-text">Where music finds its match. Groove now with BandMates!</span>
                </div>
                <div className="right-content">
                    <div className="form-container">
                        <input
                            type="text"
                            placeholder="Username"
                            className="input-field"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            className="input-field"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <button className="button" onClick={handleLogin}>Log In</button>
                        <button className="button secondary" onClick={() => navigate('/register')}>New here? Create a new account</button>
                        <span className="forgot-password">Forgot password?</span>
                    </div>
                </div>
            </div>
            {showPopup && (
                <div className="popup">
                    <div className="popup-content">
                        <span className="close" onClick={closePopup}>&times;</span>
                        <p>{popupMessage}</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LoginPage;
