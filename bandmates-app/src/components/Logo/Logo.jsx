import React from 'react'
import PropTypes from 'prop-types';
import logo from "../../assets/logo.png"

const Logo = ({ size }) => {
  // Aspect ratio of the original logo image
  const originalWidth =  225;
  const originalHeight =  50;
  const aspectRatio = originalWidth / originalHeight;

  // Calculate the height based on the size and aspect ratio
  const height = size;
  const width = height * aspectRatio;

  return (
    <img src={logo} alt="bandmates logo" style={{ width: width, height: height }} />
  );
};

// Add propTypes validation
Logo.propTypes = {
  size: PropTypes.number.isRequired // Ensure that 'size' is a required number prop
};

export default Logo
