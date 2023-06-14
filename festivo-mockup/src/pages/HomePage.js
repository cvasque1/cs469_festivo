import React, { useEffect, useState } from "react";
import './HomePage.css';
import SearchBar from "../components/SearchBar";
import FestivalCard from "../components/FestivalCard";
import YearDropdown from "../components/YearDropdown";
import AuthenticatedNavbar from "../components/AuthenticatedNavbar";
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

const itemsPerPage = 8;

function HomePage() {
    const [festivals, setFestivals] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedYear, setSelectedYear] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [username, setUsername] = useState("");
    const [years, setYears] = useState([]);

    useEffect(() => {
        fetch('/api/user')
            .then(response => response.json())
            .then(data => setUsername(data.name));

        fetch('/api/festivals')
            .then(response => response.json())
            .then(data => setFestivals(data));
    }, [])

    useEffect(() => {
        const uniqueYears = [...new Set(festivals.map(festival => festival.year))].sort((a, b) => a - b);
        setYears(uniqueYears);
    }, [festivals]);

    const handleSearch = (query) => {
        setSearchQuery(query)
    }

    const handleYearChange = (year) => {
        setSelectedYear(year);
    };

    const filteredFestivals = festivals.filter((festival) => {
        return (
            festival.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
            (selectedYear === "" || festival.year === selectedYear)
        );
    });

    filteredFestivals.sort((a, b) => a.name.localeCompare(b.name)); // sort by name
    filteredFestivals.sort((a, b) => a.year - b.year); // sort by year

    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    
    const displayedFestivals = filteredFestivals.slice(startIndex, endIndex);

    return (
        <div className="HomePage">        
            <AuthenticatedNavbar />
            <h1>FESTIVO</h1>
            <br/>
            <h2>Welcome, {username}.</h2>
            <p>Choose which festival you would like to get artist recommendations for.</p>
            <div className="ContentContainer">
                <div className="SearchFilters">
                    <SearchBar onSearch={handleSearch} />
                    <YearDropdown onYearSelection={handleYearChange} years={years} />
                </div>
                <div className="FestivalCardContainer">
                {displayedFestivals.map(festival => (
                    <FestivalCard key={`${festival.name}-${festival.year}`} festival={festival} />
                ))}
                </div>
                <button 
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                >
                    Prev
                </button>
                <button 
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={endIndex >= filteredFestivals.length}
                >
                    Next
                </button>
            </div>
        </div>
    )
}

export default HomePage;