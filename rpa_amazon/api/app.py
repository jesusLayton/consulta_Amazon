from flask import Flask, jsonify, request
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/api/products', methods=['GET'])
def get_products():
    # Logic to retrieve products from the automation script or database
    return jsonify({"message": "List of products"}), 200

@app.route('/api/product', methods=['POST'])
def add_product():
    data = request.json
    # Logic to add a product using the automation script or database
    return jsonify({"message": "Product added", "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True)