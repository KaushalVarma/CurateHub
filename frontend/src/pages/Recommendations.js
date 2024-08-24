import React, { useState, useEffect } from 'react';
import { fetchRecommendations } from '../services/recommendationService'; // Ensure correct import

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState(null);

  useEffect(() => {
    const getRecommendations = async () => {
      const data = await fetchRecommendations();
      setRecommendations(data);
    };
    getRecommendations();
  }, []);

  return (
    <div>
      <h2>Recommendations Page</h2>
      {recommendations ? (
        <div>
          {recommendations.map((rec, index) => (
            <div key={index}>
              <p>{rec.title}</p> {/* Adjust based on your data structure */}
            </div>
          ))}
        </div>
      ) : (
        <p>Loading recommendations...</p>
      )}
    </div>
  );
};

export default Recommendations;
