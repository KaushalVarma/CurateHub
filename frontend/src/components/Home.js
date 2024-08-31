import React, { useEffect, useState } from 'react';
import { fetchCategories, fetchTags, fetchUserProfile } from '../services/api';
import './Home.css';

const Home = () => {
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  const [profile, setProfile] = useState({});

  useEffect(() => {
    const loadData = async () => {
      try {
        const categoriesData = await fetchCategories();
        setCategories(categoriesData);

        const tagsData = await fetchTags();
        setTags(tagsData);

        const profileData = await fetchUserProfile();
        setProfile(profileData);
      } catch (error) {
        console.error('Error loading data:', error);
      }
    };

    loadData();
  }, []);

  return (
    <div className="home">
      <header className="home-header">
        <h1>Welcome to CurateHub, {profile.name || 'Guest'}</h1>
        <p>Your platform for curated content and personalized recommendations.</p>
      </header>
      <main className="home-main">
        <section className="home-intro">
          <h2>Get Started</h2>
          <p>Explore categories, tags, and manage your profile to get the most out of CurateHub.</p>
        </section>
        <section className="home-features">
          <div className="feature">
            <h3>Categories</h3>
            <ul>
              {categories.map((category) => (
                <li key={category.id}>{category.name}</li>
              ))}
            </ul>
          </div>
          <div className="feature">
            <h3>Tags</h3>
            <ul>
              {tags.map((tag) => (
                <li key={tag.id}>{tag.name}</li>
              ))}
            </ul>
          </div>
          <div className="feature">
            <h3>Profile</h3>
            <p>Name: {profile.name}</p>
            <p>Email: {profile.email}</p>
          </div>
        </section>
      </main>
      <footer className="home-footer">
        <p>© 2024 CurateHub. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;
