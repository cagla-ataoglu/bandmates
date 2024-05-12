import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './GigForm.css';

const GigForm = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    gigName: '',
    date: '',
    venue: '',
    genre: '',
    lookingFor: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log('formdata:', formData);
      const response = await fetch(`${import.meta.env.VITE_GIG_API}/post_gig`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          gig_name: formData.gigName,
          band_username: localStorage.getItem('username'),
          date: formData.date,
          venue: formData.venue,
          genre: formData.genre,
          looking_for: formData.lookingFor
        })
      })

      const data = await response.json();
      if (response.ok) {       
        console.log('Gig posted:', data)
        navigate('/gigs');
      } else {
        console.error('Failed to post gig:', data.message)
      }
    } catch (error) {
      console.error('Error posting gig:', error);
    }

    console.log(formData);
    // Reset form data after submission
    setFormData({
      gigName: '',
      date: '',
      venue: '',
      genre: '',
      lookingFor: '',
    });
  };

  return (
    <div className="form-container">
      <h2>Post Gig</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          <label htmlFor="gigName">Gig Name:</label>
          <input
            type="text"
            id="gigName"
            name="gigName"
            value={formData.gigName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-field">
          <label htmlFor="date">Date:</label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-field">
          <label htmlFor="venue">Venue:</label>
          <input
            type="text"
            id="venue"
            name="venue"
            value={formData.venue}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-field">
          <label htmlFor="genre">Genre:</label>
          <input
            type="text"
            id="genre"
            name="genre"
            value={formData.genre}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-field">
          <label htmlFor="lookingFor">Looking For:</label>
          <input
            type="text"
            id="lookingFor"
            name="lookingFor"
            value={formData.lookingFor}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" onClick={handleSubmit}>Post Gig</button>
      </form>
    </div>
  );
};

export default GigForm;
