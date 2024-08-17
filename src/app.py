from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to CurateHub!"

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    interest = data.get('interest')
    # Dummy data for now
    recommendations = [
        {"title": f"Recommended video for {interest} 1"},
        {"title": f"Recommended video for {interest} 2"}
    ]
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
