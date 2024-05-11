import React, { useState } from 'react';
import './Register.css';
import Logo from '../../components/Logo/Logo';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [profileType, setProfileType] = useState('')

  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState('');

  const navigate = useNavigate();

  const handleSignUp = async () => {
    if (password !== confirmPassword) {

      setPopupMessage('Passwords do not match! Please try again.');
      setShowPopup(true);

      return;
    }

    try {
      const signup_response = await fetch(`${import.meta.env.VITE_AUTH_API}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password
        })
      });

      if (signup_response.ok) {
        var profile_creation_response = null
        if (profileType == 'musician') {
          profile_creation_response = await fetch(`${import.meta.env.VITE_PROFILE_API}/create_musician_profile`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: username
            })
          })
        } else if (profileType == 'band') {
          profile_creation_response = await fetch(`${import.meta.env.VITE_PROFILE_API}/create_band_profile`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: username
            })
          })
        }
        if (profile_creation_response && profile_creation_response.ok) {
          const signin_response = await fetch(`${import.meta.env.VITE_AUTH_API}/signin`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: username,
              password: password
            })
          });

          const signin_data = await signin_response.json();

          if (signin_response.ok) {
            localStorage.setItem('access_token', signin_data.tokens.access_token);
            localStorage.setItem('refresh_token', signin_data.tokens.refresh_token);
            localStorage.setItem('username', username);
            navigate('/');
          } else {

            setPopupMessage('Signin failed.');
            setShowPopup(true);
            navigate('/login');
          }
        } else {
          setPopupMessage('Profile creation failed.');
          setShowPopup(true);
        }
      } else {
        setPopupMessage('Signup failed.');
        setShowPopup(true);
      }
    } catch (error) {
      setPopupMessage(`Error: ${error.message}`);
      setShowPopup(true);
    }
  };

  const closePopup = () => {
    setShowPopup(false);
    setPopupMessage('');
  };

  return (
    <div className="register-container">
      <div className="content">
        <div className="left-content">
          <Logo />
          <span className="register-text">Where music finds its match. Groove now with BandMates!</span>
        </div>
        <div className="right-content">
          <div className="form-container">
            <div>
              <label>Profile Type:</label>
              <label>
                <input
                  type="radio"
                  value="musician"
                  checked={profileType === 'musician'}
                  onChange={() => setProfileType('musician')}
                />
                Musician
              </label>
              <label>
                <input
                  type="radio"
                  value="band"
                  checked={profileType === 'band'}
                  onChange={() => setProfileType('band')}
                />
                Band
              </label>
            </div>
            <input
              type="name"
              placeholder="username"
              className="input-field"
              value={username}
              onChange={e => setUsername(e.target.value)}
            />
            <input
              type="email"
              placeholder="email"
              className="input-field"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="password"
              className="input-field"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
            <input
              type="password"
              placeholder="confirm password"
              className="input-field"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
            />
            <button className="button" onClick={handleSignUp}>Sign Up</button>
            <button className="button secondary" onClick={() => { navigate('/login') }}>Already have an account? Login</button>
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
}

export default Register;
