def get_redfin_csv_address(csv_json):
  property = {}
  index = 1
  for address_line in csv_json['ADDRESS'].split('#'):
    property[f'address_line_{index}'] = address_line
    index = index + 1
  property['city'] = csv_json['CITY']
  property['state'] = csv_json['STATE OR PROVINCE']
  return property