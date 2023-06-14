import React from "react";
import './FestivalCard.css'
import { useNavigate } from "react-router-dom";


function FestivalCard({ festival, key }) {
    const navigate = useNavigate();
    const festivalName = festival.name.replace(/ /g, "-");
    const festivalYear = festival.year;
    
    const navigateToFestival = () => {
      navigate(`/app/festival/${festivalName}/${festivalYear}`);
    }

    return (
      <div onClick={navigateToFestival} key={key} className="FestivalCard">
        <div
          className="FestivalImage"
          style={{ backgroundImage: `url(${festival.imageURL})` }}
        ></div>
        <div className="FestivalCardContent">
          <p className="FestivalName">{festival.name}</p>
          <p className="FestivalYear">{festival.year}</p>
        </div>
      </div>
    );
  }


export default FestivalCard;