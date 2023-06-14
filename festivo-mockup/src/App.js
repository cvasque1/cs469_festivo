import React, { useState } from 'react'
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import './App.css';
import FestivalPage from './pages/FestivalPage';
import LandingPage from './pages/LandingPage';


function App() {
  return (
    <div className="App">
      <Router>
        <div className="container">
          <Routes>
            <Route exact path="/" element={<LandingPage />} />
            <Route exact path="/app/home" element={<HomePage />} />
            <Route path="/app/festival/:festivalName/:festivalYear" element={<FestivalPage />} />
          </Routes>
        </div>
      </Router>
    </div>
  )
}

export default App