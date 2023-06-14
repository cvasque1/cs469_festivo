import React, { useState } from "react";
import './SearchBar.css'


function SearchBar({ onSearch }) {
    const [searchQuery, setSearchQuery] = useState("");

    const handleSearch = (e) => {
        setSearchQuery(e.target.value);
        onSearch(e.target.value);
    }

    return (
        <input
            type="text"
            placeholder="Search festivals..."
            value={searchQuery}
            onChange={handleSearch}
            className="SearchBar"
        />
    );
}


export default SearchBar;