// RangeSelector.js
import React from 'react';
import './RangeSelector.css'

const RangeSelector = ({ range, setRange }) => {
    return (
        <div className="AppPageContentDisplay__Form">
            <div className="RangeSelector">
                <input type="radio" value="long_term" name="range" id="long_term" checked={range === 'long_term'}
                onChange={(e) => setRange(e.target.value)} />
                <label htmlFor="long_term" className="RangeOption">All Time</label>
                <input type="radio" value="medium_term" name="range" id="medium_term" checked={range === 'medium_term'} onChange={(e) => setRange(e.target.value)} />
                <label htmlFor="medium_term" className="RangeOption">Last 6 Months</label>
                <input type="radio" value="short_term" name="range" id="short_term" checked={range === 'short_term'} onChange={(e) => setRange(e.target.value)} />
                <label htmlFor="short_term" className="RangeOption">Last Month</label>
                <input type="radio" value="genres" name="range" id="genres" checked={range === 'genres'} onChange={(e) => setRange(e.target.value)} />
                <label htmlFor="genres" className="RangeOption">Genres</label>
            </div>
            <p id="TopArtistMessage">Top Artist</p>
        </div>
    );
};

export default RangeSelector;
