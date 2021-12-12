from flask import Flask, request, url_for, redirect, render_template, jsonify
from flask_cors import CORS
# ml imports
from ml import Model, Model_content_v2

model = Model()
model_content_v2 = Model_content_v2()


# Initalise the Flask app
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "<h1>up and running</h1>"


@app.route('/recommend/<id>')
def content_basedv1(id):
    result = model.new_data(id)
    return jsonify(result)


@app.route('/recommendv2/<id>')
def content_basedv2(id):
    result = model_content_v2.new_movie(id)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
