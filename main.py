# Purpose: Automate production in the hideout to produce mass profit to fund raids
# Utilize: API with https://tarkov.dev/ and create our own database.

# imports
from time import time
import requests
import logging
import sheets_handling
import time
import progressbar

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, filename="Automaton.log", filemode="w",
                    format="%(asctime)s 0 %(levelname)s - %(message)s")
# Logging levels DEBUG, INFO, WARNING, ERROR, CRITICAL are available for now. Will modify later

# Setting our test items list, will select important items later for testing
items_list = ['pile of meds', 'shampoo', 'slickers', 'wires', 'sj6', '9x19mm rip', 'eagle', 'can of max energy', 
            'scav backpack', 'canister with purified water', 'bottle of water', 'cms surgical kit', 'Can of Hot Rod energy drink',
             'ox bleach', 'secure flash drive', 'aramid fiber fabric', 'vodka', 'wilston cigarettes', 'bottle of water', 'emergency water ration',
             'aquamari water bottle', 'aseptic bandage', 'toilet paper', 'm.u.l.e.', 'propital', 'salewa', 'ifak', 'capacitors', 'printed circuit board',
             '5.45x39mm pp', '9x18mm PM Rg028', 'weapon parts']

# A list of components for our tracked items. Will use this to further calculate our true profit after cost of material.
components_list = ['ai-2 medkit', 'aseptic bandage', 'augmentin antibiotic pills', 'soap', 'bottle of water', 'alyonka', 'pack of oat flakes',
                'army crackers', 'power cord', 'bottle of saline solution', 'bottle of hydrogen peroxide', 'hawk', 'wires', 'nippers', 'm67 hand grenade',
                'rdg-2b smoke grenade', 'can of tarcola', 'can of majaica', 'fleece', 'flyye mbss', 'water filter', 'medical tools', 'car first aid kit', 
                'pack of sugar', '42 signature blend english tea', 'ox bleach', 'alkaline cleaner', 'pack of sodium bicarbonate', 'broken gphone smartphone', 
                'broken gphone x smartphone', 'ssd drive', 'paca soft armor', 'moonshine', 'apollo soyuz cigarettes', 'canister with purified water',
                'kektape duct tape', 'gas mask air filter', 'fleece fabric', 'printer paper', 'zagustin hemostatic drug injector', 'morphine injector',
                'can of max energy drink', 'pile of meds', 'ibuprofen painkillers', 'golden star balm', 'analgin painkillers', 'calok-b hemostatic applicator',
                'esmarch tourniquet', 'army bandage', 'power supply unit', 'dvd drive', 'gas analyzer', '5.45x39mm PS gs', 'bolts', 'kite', 'molot vpo-209 .366 tkm carbine']


# Function to send query out
def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


# Format to send out queries to get our data
def query_send_receive(item_input):
    # Query payload
    new_query = f"""
    {{
        itemsByName(name: "{item_input}") {{
            name
            fleaMarketFee
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


# Function will update the spreadsheet with our tracked items
def update_items():
    # Testing list items comprehension with more pertinent information to take
    items_dictionary = {}
    fee_list = []
    
    for item_top in items_list:
        logging.info(f"Testing for item query of {item_top}")
        trimmed_result = query_send_receive(item_top)

        # Separate information to be used
        price_list = trimmed_result['sellFor']
        flea_market_fee = trimmed_result['fleaMarketFee']
        # add the fee to our list
        fee_list.append(flea_market_fee)
        # Determine highest price
        highest_price = 0
        # Iterate through available price data to find the highest available
        for item in price_list:
            if item['price'] > highest_price:
                highest_source = item['source']
                highest_price = item['price']
                items_dictionary[item_top] = item['price']
        
        logging.info(f"{item_top} completed successfully")
    
    # Take information and post it to our google sheet
    # Is not made available to general public. If wanted, create your own keys and give same file name.
    # Index tracking for updating our rows 
    fee_index = 0
    start_index = 1
    print('Updating worksheet')
    for item in items_dictionary:
        start_index += 1
        start_point_a = ('A', start_index)
        #start_point_a = sheets_handling.get_next_empty_cell('A')
        sheets_handling.update_row(item,items_dictionary[item], start_point_a, fee_list[fee_index])
        fee_index += 1
        # Google sheets doesn't like us updating too frequently, so we impose our own time limits to help
        time.sleep(15)


# Main function to run our more purposeful code
if __name__ == "__main__":
    
    # Run our function to update the spreadsheet
    update_items()
    
    # Additional actions will be performed from here referring to this sheet of data.
    logging.info("Program successfully completed operation")
