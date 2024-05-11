import React, { useState } from 'react';
import './GigForm.css';

const GigForm = () => {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you can handle posting the gig using the formData
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
                    <button type="submit">Post Gig</button>
                </form>
        </div>
  );
};

export default GigForm;
