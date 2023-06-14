import React from "react";
import './Navbar.css'


function AuthenticatedNavbar() {
    function handleSignOut() {
        fetch('/sign_out')
            .then(response => response.json())
            .then(data => {
                // Check if sign-out was successful
                if (data.message === 'Sign-out successful') {
                // Redirect to the landing page
                window.location.href = '/';
                } else {
                // Handle sign-out failure
                console.log('Sign-out failed');
                }
            })
            .catch(error => {
                // Handle fetch error
                console.error('Error signing out:', error);
            });
    }

    return (
        <nav className="authenticatedNavbar">
            <div className="Navigation">
                <a className="Navigation__Link Auth" href="/app/home">
                    Festivo
                </a>
                <button className="Navigation__Link Highlight SignOut Auth" onClick={handleSignOut}>
                Sign Out
                </button>
            </div>
        </nav>
    );
}

export default AuthenticatedNavbar;
