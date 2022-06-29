import json

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


def mapping(property):
    address_lines = list(map((lambda x: x.strip()), property['location']['address']['line']))

    # Location Data
    address_line_1 = address_lines[0]
    address_line_2 = None
    if (len(address_lines) > 1):
        address_line_2 = address_lines[1]
    city = property['location']['address']['city']
    state = property['location']['address']['state']
    state_code = property['location']['address']['state_code']
    zipcode = property['location']['address']['postal_code']
    neighborhood = property['location']['address']
    lat = property['location']['address']['coordinate']['lat']
    lon = property['location']['address']['coordinate']['lon']
    point = f'POINT({lat},{lon})'

    # General Info
    property_type = property['description']['type']
    septic_tank = None
    garage_spaces = property['description']['garage']

    last_update_date = property['last_update_date']
    list_date = property['list_date']
    us_real_estate_api_id = property['property_id']
    is_new_construction = property['flags']['is_new_construction']
    is_subdivision = property['flags']['is_subdivision']
    is_plan = property['flags']['is_plan']
    is_price_reduced = property['flags']['is_price_reduced']
    is_pending = property['flags']['is_pending']
    is_foreclosure = property['flags']['is_foreclosure']
    is_new_listing = property['flags']['is_new_listing']
    is_coming_soon = property['flags']['is_coming_soon']
    is_contingent = property['flags']['is_contingent']

    year_built = property['description']['year_built']
    baths_3qtr = property['description']['baths_3qtr']
    sold_date = property['description']['sold_date']
    sold_price = property['description']['sold_price']
    baths_full = property['description']['baths_full']
    baths_half = property['description']['baths_half']
    lot_sqft = property['description']['lot_sqft']
    sqft = property['description']['sqft']
    baths = property['description']['baths']
    baths_1qtr = property['description']['baths_1qtr']
    stories = property['description']['stories']
    beds = property['description']['beds']
    
    # Purchase Info
    list_price = property['list_price']
    rehab_costs = 0
    down_payment = list_price * 0.25
    loan_amount = list_price + rehab_costs
    closing_costs = loan_amount + 0.0268
    equity_required = down_payment + closing_costs
    mortgage_rate = 0.05
    mortgage_payment = get_mortgage_payment(loan_amount, mortgage_rate, 30)

    # Operating Expenses
    property_tax = property
    hoa = property
    property_management = property
    home_insurance = property
    monthly_repairs = property
    monthly_capex = property
    total_monthly_expenses = 0

    # Income
    rent = get_rent()
    rent_after_vacancy = rent * (1 - 0.083)
    effective_gross_income = rent_after_vacancy
    net_cash_flow = effective_gross_income - total_monthly_expenses

    # Metrics
    cap_rate = property
    cash_on_cash = property

def get_mortgage_payment(loan_amount, interest_rate, term):
    monthly_interest_rate = interest_rate / 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-term * 12))
    return monthly_payment

def get_rent():
    # TODO: Get rent from API
    return 0