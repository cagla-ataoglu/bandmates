import React from 'react';
import './Login.css'; // Import the CSS file for LoginPage styling
import Logo from '../../components/Logo/Logo';

const LoginPage = () => {
    return (
        <div className="login-container">
            <div className="content">
                <div className="left-content">
                    <Logo />
                    <span className="login-text">Where music finds its match. Groove now with BandMates!</span>
                </div>
                <div className="right-content">
                    <div className="form-container">
                        <input type="username" placeholder="Username" className="input-field" />
                        <input type="password" placeholder="Password" className="input-field" />
                        <button className="button">Log In</button>
                        <button className="button secondary">New here? Create a new account</button>
                        <span className="forgot-password">Forgot password?</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
