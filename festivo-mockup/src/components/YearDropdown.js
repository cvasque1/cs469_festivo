import React from "react";
import './YearDropdown.css'


function YearDropdown({ onYearSelection, years }) {
    const handleYearChange = (e) => {
        const selectedYear = e.target.value === "" ? "" : parseInt(e.target.value);
        onYearSelection(selectedYear);
    }

    return (
        <select className="DropDown" name="year" onChange={handleYearChange}>
            <option key="" value="">All Years</option>
        {years.map(year => (
            <option key={year} value={year}>{year}</option>
        ))}
        </select>
    );
}


export default YearDropdown;

