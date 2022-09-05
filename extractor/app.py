from flask import Flask, request
import json
import requests
from helpers import us_real_esate_mapping
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

us_real_estate_api_key = os.environ['US_REAL_ESTATE_API_KEY']
ingest_host = os.environ['INGEST_HOST']

# Get all properties for sale in a city
# Params example:
# city: 'Jacksonville'
# state_code: 'Fl'
# limit: 10
# offset: 20
@app.route('/fetch-properties-by-city', methods=['POST'])
def fetch_properties():
    body = json.loads(request.data)
    city = body['city']
    state_code = body['state_code']
    offset = body['offset'] if body["offset"] else 0
    limit = body['limit'] if body['limit'] else 42

    url = "https://us-real-estate.p.rapidapi.com/v2/for-sale"
    querystring = {
        "offset": f"{offset}",
        "limit": f"{limit}",
        "state_code": f"{state_code.upper()}",
        "city": f"{city.capitalize()}",
        "sort": "newest"
    }
    headers = {
        "X-RapidAPI-Key": us_real_estate_api_key,
        "X-RapidAPI-Host": "us-real-estate.p.rapidapi.com"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    addresses = []

    for api_property in response.json()["data"]["home_search"]["results"]:
        property_record = us_real_esate_mapping(api_property)
        res = requests.post(
            f'{ingest_host}/properties/ingest/single', json=property_record)
        res.raise_for_status()
        print(res.json())
        print(res.text)
        print('\n')
        addresses.append(str(res.content))

    return f'{response.json()["data"]["home_search"]["count"]} properties for {city} {state_code} saved'



if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)
