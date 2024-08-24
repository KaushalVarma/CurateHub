// src/services/recommendationService.js

export const fetchRecommendations = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/recommendations'); // Adjust the URL based on your API endpoint
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return [];
    }
};
