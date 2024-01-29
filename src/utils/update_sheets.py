# imports
import requests
import logging
import time
from utils import sheets_handling

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, filename="Automaton_sheets.log", filemode="w",
                    format="%(asctime)s 0 %(levelname)s - %(message)s")
# Logging levels DEBUG, INFO, WARNING, ERROR, CRITICAL are available for now. Will modify later

# Setting our test items list, will select important items later for testing
items_list = ['pile of meds', 'shampoo', 'slickers', 'wires', 'sj6', '9x19mm rip', 'eagle', 'can of max energy', 
            'scav backpack', 'canister with purified water', 'bottle of water', 'cms surgical kit', 'Can of Hot Rod energy drink',
             'ox bleach', 'secure flash drive', 'aramid fiber fabric', 'vodka', 'wilston cigarettes', 'bottle of water', 'emergency water ration',
             'aquamari water bottle', 'aseptic bandage', 'toilet paper', 'm.u.l.e.', 'propital', 'salewa', 'ifak', 'capacitors', 'printed circuit board',
             '5.45x39mm pp', '9x18mm PM Rg028', 'weapon parts', 'car battery', 'nixxor lens', '.366 tkm ap-m', 'kalashnikov ak-74m 5.45x39 assault rifle',
             '9x18mm pm pbm gzh', 'vog-25', 'can of thermite', '12/70 flechette', 'magnet', 'kite', 'hawk', 'rechargeable battery', 'lucky scav junk box',
             'ana tactical m1 armored rig', 'magazine case', 'ak-74 5.45x39 6l31 60-round magazine', 'fleece', 'cordura', 'army bandage', 'ripstop fabric',
             'grizzly medical kit', 'vaseline balm', 'surv12 field surgical kit', 'calok-b hemostatic applicator', 'ai-2 medkit', 'medical bloodset', 
             'can of condensed milk', 'Bottle of Tarkovskaya vodka']

# A list of components for our tracked items. Will use this to further calculate our true profit after cost of material.
components_list = ['ai-2 medkit', 'aseptic bandage', 'augmentin antibiotic pills', 'soap', 'bottle of water', 'alyonka', 'pack of oat flakes',
                'army crackers', 'power cord', 'bottle of saline solution', 'bottle of hydrogen peroxide', 'hawk', 'wires', 'nippers', 'm67 hand grenade',
                'rdg-2b smoke grenade', 'can of tarcola', 'can of majaica', 'fleece', 'flyye mbss', 'water filter', 'medical tools', 'car first aid kit', 
                'pack of sugar', '42 signature blend english tea', 'ox bleach', 'alkaline cleaner', 'pack of sodium bicarbonate', 'broken gphone smartphone', 
                'broken gphone x smartphone', 'ssd drive', 'paca soft armor', 'moonshine', 'apollo soyuz cigarettes', 'canister with purified water',
                'kektape duct tape', 'gas mask air filter', 'fleece fabric', 'printer paper', 'zagustin hemostatic drug injector', 'morphine injector',
                'can of max energy drink', 'pile of meds', 'ibuprofen painkillers', 'golden star balm', 'analgin painkillers', 'calok-b hemostatic applicator',
                'esmarch tourniquet', 'army bandage', 'power supply unit', 'dvd drive', 'gas analyzer', '5.45x39mm PS gs', 'bolts', 'kite', 'molot vpo-209 .366 tkm carbine']

# Create a progress bar so we know what we're doing
def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + ' ' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

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
        items(name: "{item_input}") {{
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
    trimmed_result = trimmed_result['items']
    trimmed_result = trimmed_result[0]
    
    return trimmed_result


# Function will update the spreadsheet with our tracked items
def update_items():
    # Testing list items comprehension with more pertinent information to take
    items_dictionary = {}
    fee_list = []

    print('Update items...')
    progress_bar(0, len(items_list))
    for index, item_top in enumerate(items_list):
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
        progress_bar(index + 1, len(items_list))
        
        logging.info(f"{item_top} completed successfully")
    
    # Take information and post it to our google sheet
    # Is not made available to general public. If wanted, create your own keys and give same file name.
    # Index tracking for updating our rows 
    fee_index = 0
    start_index = 1
    print('\nUpdating worksheet')
    progress_bar(0, len(items_dictionary))
    for index, item in enumerate(items_dictionary):
        # Google sheets doesn't like us updating too frequently, so we impose our own time limits to help
        time.sleep(15)
        start_index += 1
        start_point_a = ('A', start_index)
        #start_point_a = sheets_handling.get_next_empty_cell('A')
        sheets_handling.update_row(item,items_dictionary[item], start_point_a, fee_list[fee_index])
        fee_index += 1
        progress_bar(index + 1, len(items_dictionary))
  