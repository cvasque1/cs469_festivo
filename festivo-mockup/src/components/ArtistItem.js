// ArtistItem.js
import React from 'react';
import './ArtistItem.css';

const ArtistItem = ({ image, name, url }) => {
    return (
        <a className="ArtistItem" href={url}>
            <div className="ArtistItemBlock">
                <div className="ArtistImage" style={{ backgroundImage: `url(${image})` }}></div>
                <div className="ArtistNameContainer">
                    <p className="ArtistName">{name}</p>
                </div>
            </div>
        </a>
    );
};

export default ArtistItem;
