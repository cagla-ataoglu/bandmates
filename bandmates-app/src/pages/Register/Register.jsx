import React from 'react';
import './Register.css'; // Import the CSS file for Register styling
import Logo from '../../components/Logo/Logo';

const Register = () => {
  return (
    <div className="register-container">
      <div className="content">
        <div className="left-content">
          <Logo />
          <span className="register-text">Where music finds its match. Groove now with BandMates!</span>
        </div>
        <div className="right-content">
          <div className="form-container">
            <input type="name" placeholder="username" className="input-field" />
            <input type="email" placeholder="email" className="input-field" />
            <input type="password" placeholder="password" className="input-field" />
            <input type="password" placeholder="confirm password" className="input-field" />
            <button className="button">Sign Up</button>
            <button className="button secondary">Already have an account? Login</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
