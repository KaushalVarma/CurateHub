document.getElementById('interest-form').addEventListener('submit', function(event){
    event.preventDefault();
    let interest = document.getElementById('interest-input').value;
    if(interest){
        // Send interest to the backend and fetch recommendations
        fetch('api/recommendations', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify({ interest: interest })
        })
        .then(response => response.json())
        .then(data => {
            let recommendationsDiv = document.getElementById('recommendations');
            recommendationsDiv.innerHTML = '<h3>Recommendations:</h3>';
            data.recommendations.forEach(item => {
                let p = document.createElement('p');
                p.textContent = item.title;
                recommendationsDiv.appendChild(p);
            })
        })
    }
})