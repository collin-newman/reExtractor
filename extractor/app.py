from flask import Flask, request
import json
import requests
from helpers import save_json_to_file
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/properties-by-location', methods=['POST'])
def fetch_properties():
    body = json.loads(request.data)
    city = body['city']
    state_code = body['state_code']

    # url = "https://us-real-estate.p.rapidapi.com/v2/for-sale"
    # querystring = {
    #     "offset": "0",
    #     "limit": "42",
    #     "state_code": f"{state_code.upper()}",
    #     "city": f"{city.capitalize()}",
    #     "sort": "newest"
    # }
    # headers = {
    #     "X-RapidAPI-Key": "c4182ea640msh91c3897924ad99ap13e4f9jsn42bf788eaff9",
    #     "X-RapidAPI-Host": "us-real-estate.p.rapidapi.com"
    # }
    # response = requests.request(
    #     "GET", url, headers=headers, params=querystring)

    # jsonFilePath = f'{os.getcwd()}/extractor/us-real-estate-api/jax_properties.json'

    # save_json_to_file(response.text, jsonFilePath)
    return f'Properties for {city} {state_code} saved'


if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)
