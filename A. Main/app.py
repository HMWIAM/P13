from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('/home/henry/Desktop/P13/A. Main/model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_cites():
    data = request.get_json()
    city_name = data['city']
    
    # Call your recommend function with the city_name
    city, prices = model.recommend(city_name)
    
    # Prepare the response data
    response_data = {
        'city_name': city_name,
        'recommended_cities': city,
        'recommended_prices': prices
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run()