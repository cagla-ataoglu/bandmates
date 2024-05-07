import React from 'react';
import concertIcon from '../../assets/concert.png';
import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBCardHeader, MDBCardFooter, MDBBtn } from 'mdb-react-ui-kit';
import './Rightbar.css';

const Rightbar = () => {
  return (
    <div className="container">
      <div className="card">
        <div className="wrapper">
          <img src={concertIcon} alt="Concert Icon" className="w-[30px] h-[30px] mr-[5px] ml-[10px]" />
          <p><b>Elvis Presley</b> and <b>2 others</b> have a gig today.</p>
        </div>
      </div>
    </div>
  );
};

export default Rightbar;
