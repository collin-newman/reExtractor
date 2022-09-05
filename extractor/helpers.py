import json, requests
from dotenv import load_dotenv
import os

load_dotenv()
rent_api_key = os.environ['RENT_API_KEY']


def get_redfin_csv_address(csv_json):
    property = {}
    index = 1
    for address_line in csv_json['ADDRESS'].split('#'):
        property[f'address_line_{index}'] = address_line
        index = index + 1
    property['city'] = csv_json['CITY']
    property['state'] = csv_json['STATE OR PROVINCE']
    return property

def save_json_to_file(jsonArray, jsonFilePath):
    with open(jsonFilePath, 'w') as f:
        json.dump(jsonArray, f, ensure_ascii=False)


def us_real_esate_mapping(property):
    # TODO split address into 2 lines if its an apartment
    # address_lines = list(
    #     map((lambda x: x.strip()), property['location']['address']['line']))

    new_property = {}

    # Location Data
    new_property['address_line_1'] = property['location']['address']['line']
    # new_property['address_line_1'] = address_lines[0]
    new_property['address_line_2'] = ''
    # if (len(address_lines) > 1):
    #     new_property['address_line_2'] = address_lines[1]
    new_property['city'] = property['location']['address']['city']
    new_property['state'] = property['location']['address']['state']
    new_property['state_code'] = property['location']['address']['state_code']
    new_property['zipcode'] = property['location']['address']['postal_code']
    new_property['neighborhood'] = ''
    new_property['lat'] = property['location']['address']['coordinate']['lat']
    new_property['lon'] = property['location']['address']['coordinate']['lon']
    new_property['point'] = f'POINT({new_property["lat"]},{new_property["lon"]})'

    # General Info
    new_property['property_type'] = property['description']['type']
    new_property['septic_tank'] = False
    new_property['garage_spaces'] = property['description']['garage'] if property['description']['garage'] else 0

    new_property['last_update_date'] = property['last_update_date']
    new_property['list_date'] = property['list_date']
    new_property['us_real_estate_api_id'] = property['property_id']
    new_property['is_new_construction'] = property['flags']['is_new_construction']
    new_property['is_subdivision'] = property['flags']['is_subdivision']
    new_property['is_plan'] = property['flags']['is_plan']
    new_property['is_price_reduced'] = property['flags']['is_price_reduced']
    new_property['is_pending'] = property['flags']['is_pending']
    new_property['is_foreclosure'] = property['flags']['is_foreclosure']
    new_property['is_new_listing'] = property['flags']['is_new_listing']
    new_property['is_coming_soon'] = property['flags']['is_coming_soon']
    new_property['is_contingent'] = property['flags']['is_contingent']

    new_property['year_built'] = property['description']['year_built']
    new_property['baths_3qtr'] = property['description']['baths_3qtr']
    new_property['sold_date'] = property['description']['sold_date']
    new_property['sold_price'] = property['description']['sold_price']
    new_property['baths_full'] = property['description']['baths_full']
    new_property['baths_half'] = property['description']['baths_half']
    new_property['lot_sqft'] = property['description']['lot_sqft']
    new_property['sqft'] = property['description']['sqft']
    new_property['baths'] = property['description']['baths']
    new_property['baths_1qtr'] = property['description']['baths_1qtr']
    new_property['stories'] = property['description']['stories']
    new_property['beds'] = property['description']['beds']

    # Price Info
    new_property['list_price'] = property['list_price']
    new_property['purchase_price'] = property['list_price']
    new_property['market_value'] = property['list_price']
    new_property['rehab_costs'] = 0
    new_property['down_payment'] = new_property['list_price'] * 0.25
    new_property['loan_amount'] = new_property['list_price'] + \
        new_property['rehab_costs']
    new_property['closing_costs'] = new_property['loan_amount'] + 0.0268
    new_property['equity_required'] = new_property['down_payment'] + \
        new_property['closing_costs']
    new_property['mortgage_rate'] = 0.05
    new_property['mortgage'] = get_mortgage_payment(
        new_property['loan_amount'], new_property['mortgage_rate'], 30)
    new_property['total_cash_invested'] = new_property['equity_required']


    rent_from_api = get_rent(
        new_property['address_line_1'],
        new_property['address_line_2'],
        new_property['city'],
        new_property['state'],
        new_property['zipcode'],
    )

    # Operating Expenses
    new_property['property_tax'] = 0
    new_property['hoa'] = 0
    new_property['property_management'] = rent_from_api * 0.1
    new_property['home_insurance'] = 0
    new_property['monthly_repairs'] = 0
    new_property['monthly_capex'] = 0
    new_property['total_monthly_expenses'] = 0
    new_property['operating_expenses'] = 0

    # Income
    new_property['rent'] = rent_from_api
    new_property['rent_after_vacancy'] = new_property['rent'] * (1 - 0.083)
    new_property['effective_gross_income'] = new_property['rent_after_vacancy']
    new_property['net_operating_income'] = rent_from_api - \
        new_property['operating_expenses']
    new_property['net_cash_flow'] = new_property['effective_gross_income'] - \
        new_property['total_monthly_expenses']

    # Metrics
    new_property['cap_rate'] = new_property['net_operating_income'] / \
        new_property['market_value']
    new_property['cash_on_cash'] = (
        12 * new_property['net_cash_flow']) / new_property['equity_required']

    return new_property


def get_mortgage_payment(loan_amount, interest_rate, term):
    monthly_interest_rate = interest_rate / 12
    monthly_payment = (loan_amount * monthly_interest_rate) / \
        (1 - (1 + monthly_interest_rate) ** (-term * 12))
    return monthly_payment


def get_rent(address_line_1, address_line_2, city, state, zipcode):
    # TODO: Find better way to get rent
    # Add a sleep to account for API rate limiting
    return 0
    full_address = ''
    if address_line_2 == '':
        full_address = f'{address_line_1}, {address_line_2}, {city}, {state}, {zipcode}'
    else:
        full_address = f'{address_line_1}, {city}, {state}, {zipcode}'

    url = "https://realtymole-rental-estimate-v1.p.rapidapi.com/rentalPrice"

    querystring = {"address": full_address, "compCount": "0"}

    headers = {
        "X-RapidAPI-Key": rent_api_key,
        "X-RapidAPI-Host": "realtymole-rental-estimate-v1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    print(json.loads(response.text))

    # TODO add rentRangeLow and rentRangeHigh

    return json.loads(response.text)['rent']
