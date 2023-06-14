import React, { useEffect, useState } from 'react';
import './LandingPage.css'
import LandingNavbar from '../components/LandingNavbar';


function LandingPage() {
    const [authUrl, setAuthUrl] = useState('');

    useEffect(() => {
        fetch('/get_auth_url')
            .then(response => response.json())
            .then(data => setAuthUrl(data.auth_url));
    }, []);

    return (
        <body>
            <header>
                <nav>
                    <LandingNavbar authUrl={authUrl} />
                </nav>
            </header>

            <section class="Homepage">
                <h1 class="HomepageHeader__Title">Enhance your Festival Experience</h1>
                <div class="HomepageContent">
                    <p class="HomepageContent__Description">Festivo is a free Spotify-powered app that recommends you artists from <span class="CapContainer"><span id="cap">any*</span><span id="secret">that's cap</span></span> lineup based on your most listened-to artists.</p>
                    <a class="HomepageContent__SignIn" href={authUrl}>Sign in with spotify</a>
                </div>
            </section>
        </body>
    )
}


export default LandingPage;