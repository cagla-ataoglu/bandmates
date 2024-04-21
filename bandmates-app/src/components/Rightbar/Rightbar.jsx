import React from 'react'
import concertIcon from '../../assets/concert.png'

const Rightbar = () => {
  return (
    <div style={{flex: 3.5}}>
        <div className="pt-[20px] pr-[20px]">
            <div className="flex items-center">
                <img src={concertIcon} alt="Concert Icon" className="w-[35px] h-[35px] mr-[5px] ml-[15px]" />
                <span className="text-md"><b>Elvis Parsley</b> and <b>2 others</b> have a gig today.</span>
            </div>
        </div>
    </div>
  )
}

export default Rightbar