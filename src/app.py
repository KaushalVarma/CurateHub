from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to CurateHub!"

# GET method for recommendations
@app.route('/api/recommendations', methods=['GET'])
def get_recommendations_get():
    interests = request.args.getlist('interests')
    recommendations = [
        {"title": f"Recommended video for {interest} 1"} for interest in interests
    ]
    return jsonify({'recommendations': recommendations})

# POST method for recommendations
@app.route('/api/recommendations', methods=['POST'])
def get_recommendations_post():
    data = request.json
    interest = data.get('interest')
    recommendations = [
        {"title": f"Recommended video for {interest} 1"},
        {"title": f"Recommended video for {interest} 2"}
    ]
    return jsonify({"recommendations": recommendations})

# Test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'GET method works!'})

if __name__ == '__main__':
    app.run(debug=True)
