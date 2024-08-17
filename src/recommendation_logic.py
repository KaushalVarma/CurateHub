def recommend_content(user_interests):
    """
    Recommend content based on user interests.
    
    Parameters:
    user_interests (list of str): List of user-selected interests or topics.
    
    Returns:
    list of dict: List of recommended content with titles.
    """
    recommendations = []
    for interest in user_interests:
        recommendations.append({
            "title": f"Recommended video for {interest} 1"
        })
        recommendations.append({
            "title": f"Recommended video for {interest} 2"
        })
    return recommendations