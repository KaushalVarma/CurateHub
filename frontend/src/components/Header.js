import React from 'react';
import { Link } from 'react-router-dom';

export const Header = () => {
    return (
        <header>
            <nav>
                <h1>CurateHub</h1>
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/profile">Profile</Link></li>
                    <li><Link to="/recommendations">Recommendations</Link></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;