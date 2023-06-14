import React, { useEffect, useState } from "react";
import ArtistItem from "../components/ArtistItem";
import RangeSelector from "../components/RangeSelector";
import AuthenticatedNavbar from "../components/AuthenticatedNavbar";
import './FestivalPage.css';
import { useParams } from "react-router-dom";

function FestivalPage() {
    const {festivalName, festivalYear} = useParams();
    const [range, setRange] = useState('long_term');
    const [longTermRecs, setLongTermRecs] = useState([]);
    const [medTermRecs, setMedTermRecs] = useState([]);
    const [shortTermRecs, setShortTermRecs] = useState([]);
    const [genreRecs, setGenreRecs] = useState([]);
    const [longTermLoading, setLongTermLoading] = useState(true);
    const [medTermLoading, setMedTermLoading] = useState(true);
    const [shortTermLoading, setShortTermLoading] = useState(true);
    const [genreLoading, setGenreLoading] = useState(true);

    let isLoading = false;
    let artists = [];
    switch (range) {
        case 'long_term':
            artists = longTermRecs;
            isLoading = longTermLoading;
            break;
        case 'medium_term':
            artists = medTermRecs;
            isLoading = medTermLoading;
            break;
        case 'short_term':
            artists = shortTermRecs;
            isLoading = shortTermLoading;
            break;
        case 'genres':
            artists = genreRecs;
            isLoading = genreLoading;
            break;
        default:
            artists = [];
    }

    useEffect(() => {
        // ...

        fetch(`/api/recommended-artists/${festivalName}/${festivalYear}/long_term`)
            .then(response => response.json())
            .then(data => {
                setLongTermRecs(data);
                setLongTermLoading(false);
            });

        fetch(`/api/recommended-artists/${festivalName}/${festivalYear}/medium_term`)
            .then(response => response.json())
            .then(data => {
                setMedTermRecs(data);
                setMedTermLoading(false);
            });

        fetch(`/api/recommended-artists/${festivalName}/${festivalYear}/short_term`)
            .then(response => response.json())
            .then(data => {
                setShortTermRecs(data);
                setShortTermLoading(false);
            });

        fetch(`/api/recommended-artists/${festivalName}/${festivalYear}/genres`)
            .then(response => response.json())
            .then(data => {
                setGenreRecs(data);
                setGenreLoading(false);
            });
    }, []);

    const createPlaylist = (term) => {
        fetch(`/api/create-playlist/${festivalName}/${festivalYear}/${term}`)
            .then(response => {
                if (response.ok) {
                    // Playlist created successfully
                    alert("Playlist created successfully!");
                } else {
                    // Playlist creation failed
                    alert("Failed to create playlist.");
                }
            })
            .catch(error => {
                console.error("Error creating playlist:", error);
                alert("An error occurred while creating the playlist.");
            });
    };

    return (
            <section className="AppPage">
                <div className="AppPageContent">
                    <AuthenticatedNavbar />
                    <div className="AppPageContentImage"></div>
                    <section className="AppPageContentDisplay">
                        <div className="AppPageContentDisplay__Title">
                            <p>Your</p>
                            <h1>{festivalName.replace(/-/g, " ")} <span id="Year">{festivalYear}</span></h1>
                            <p>Recommended Artists</p>
                        </div>
                        <RangeSelector range={range} setRange={setRange} />
                        <div className="AppPageContentDisplayArtists">
                        {isLoading ? (
                            <div className="LoadingSymbol">
                                <span className="LoadingText"></span>
                            </div>
                        ) : (
                            <ul className="AllArtists">
                                {artists.map(artist => 
                                    <ArtistItem 
                                        key={artist.url} 
                                        image={artist.image} 
                                        name={artist.name} 
                                        url={artist.url} 
                                    />
                                )}
                            </ul>
                        )}
                        </div>    
                    </section>
                    <section className="AppPageContentPlaylist">
                        <form 
                            className="PlaylistGenerator"
                            onSubmit={(e) => {
                                e.preventDefault();
                                createPlaylist(range);
                            }}
                        >
                            <input className="Indicator" type="text" name="playlistPointer" value={range} style={{visibility: "hidden"}} />
                            <button className="PlaylistGenerator__Button" type="submit">Create Playlist</button>
                        </form>
                    </section>
                </div>
            </section>
    );
}


export default FestivalPage;