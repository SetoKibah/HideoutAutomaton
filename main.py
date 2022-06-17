# Purpose: Automate production in the hideout to produce mass profit to fund raids
# Utilize: API with https://tarkov.dev/ and create our own database.

# imports
import requests
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.DEBUG, filename="Automaton.log", filemode="w",
                    format="%(asctime)s 0 %(levelname)s - %(message)s")
# logging levels DEBUG, INFO, WARNING, ERROR, CRITICAL are available for now. Will modify later

# Setting our test items list, will select important items later for testing
items_list = ['pile of meds', 'shampoo', 'slickers', 'wires']

# Function to send query out
def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))



def query_send_receive(item_input):
    # Query payload
    new_query = f"""
    {{
        itemsByName(name: "{item_input}") {{
            name
            shortName
            avg24hPrice
            lastLowPrice
            low24hPrice
            high24hPrice
            basePrice
            sellFor{{
                price
                source
            }}
        }}
    }}

    """
    # Send query and get our relevant data
    result = run_query(new_query)
    logging.info(f"Result of run_query is {result}")
    trimmed_result = result['data']
    trimmed_result = trimmed_result['itemsByName']
    trimmed_result = trimmed_result[0]
    
    return trimmed_result

"""
print('All available prices:')
for item in price_list:
    print(f"{item['source']}:{item['price']}")
""" 

if __name__ == "__main__":
    
    # Testing list items comprehension with more pertinent information to take
    items_dictionary = {}
    for item_top in items_list:
        
        logging.info(f"Testing for item query of {item_top}")
        trimmed_result = query_send_receive(item_top)

        # Separate information to be used
        price_list = trimmed_result['sellFor']
        average_price = trimmed_result['avg24hPrice']
        last_low = trimmed_result['lastLowPrice']
        low_past_day = trimmed_result['low24hPrice']
        high_past_day = trimmed_result['high24hPrice']
        
        # Determine highest price
        highest_price = 0
        # Iterate through available price data to find the highest available
        for item in price_list:
            if item['price'] > highest_price:
                highest_source = item['source']
                highest_price = item['price']
                items_dictionary[item_top] = f"{item['price']} from {item['source']}"

    # Display pertinent information 
    print("**************************")       
    for item in items_dictionary:
        print(f"{item}: {items_dictionary[item]}")
    print("**************************")
    logging.info("Program successfully completed operation")