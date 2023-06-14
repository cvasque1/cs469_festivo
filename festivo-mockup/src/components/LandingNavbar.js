import React from "react";

function LandingNavbar({ authURL }) {
  return (
      <div className="Navigation">
        <a className="Navigation__Link" href="/">
          Festivo
        </a>
        <a
          className="Navigation__Link Highlight SignIn"
          href={authURL}
        >
          Sign In
        </a>
      </div>
  );
}

export default LandingNavbar;
