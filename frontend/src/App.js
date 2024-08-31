import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home'; // Import the new Home component
import CategoryList from './components/CategoryList';
import Profile from './components/Profile';
import TagList from './components/TagList';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/categories" element={<CategoryList />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/tags" element={<TagList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
