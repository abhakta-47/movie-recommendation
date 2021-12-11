from flask import Flask, request, url_for, redirect, render_template, jsonify
from flask_cors import CORS
# ml imports
from ml import Model

model = Model()

# Initalise the Flask app
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "<h1>up and running</h1>"


@app.route('/recommend/<id>')
def recommende(id):
    result = model.new_data(id)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
