# Purpose: Automate production in the hideout to produce mass profit to fund raids
# Utilize: API with https://tarkov.dev/ and create our own database.

# imports
import requests

# Function to send query out
def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

# Query payload
new_query = """
{
    itemsByName(name: "shampoo") {
        name
        shortName
        avg24hPrice
        lastLowPrice
        low24hPrice
        high24hPrice
        basePrice
        sellFor{
            price
            source
        }
    }
}
"""
# Send query and get our relevant data
result = run_query(new_query)
trimmed_result = result['data']
trimmed_result = trimmed_result['itemsByName']
trimmed_result = trimmed_result[0]

# Separate information to be used
price_list = trimmed_result['sellFor']
average_price = trimmed_result['avg24hPrice']
last_low = trimmed_result['lastLowPrice']
low_past_day = trimmed_result['low24hPrice']
high_past_day = trimmed_result['high24hPrice']

"""
print('All available prices:')
for item in price_list:
    print(f"{item['source']}:{item['price']}")
""" 
# Determine highest price
highest_price = 0

for item in price_list:
    if item['price'] > highest_price:
        highest_source = item['source']
        highest_price = item['price']
        
print(f"Highest Price- {highest_price}₽ from {highest_source}₽\n"
      f"Average Price- {average_price}₽\nLast Low- {last_low}₽\n"
      f"Last 24Hr Low- {low_past_day}₽\nLast 24hr High- {high_past_day}₽")

print(f"24hr High is {int(high_past_day) - int(highest_price)}₽ greater than current high")
print(f"Recommend ~{int((int(high_past_day) - int(highest_price))/2 + int(highest_price))}₽ for sale price")