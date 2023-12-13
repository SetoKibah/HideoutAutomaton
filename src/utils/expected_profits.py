import requests
from time import sleep, strftime
import sheets_handling_profits
import sys


def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


# Create a progress bar so we know what we're doing
def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + ' ' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")



items_list = ['pile of meds', 'shampoo', 'slickers', 'wires', 'sj6', '9x19mm rip', 'eagle', 'can of max energy', 
            'scav backpack', 'canister with purified water', 'bottle of water', 'cms surgical kit', 'Can of Hot Rod energy drink',
             'ox bleach', 'secure flash drive', 'aramid fiber fabric', 'vodka', 'wilston cigarettes', 'bottle of water', 'emergency water ration',
             'aquamari water bottle', 'aseptic bandage', 'toilet paper', 'm.u.l.e.', 'propital', 'salewa', 'ifak', 'capacitors', 'printed circuit board',
             '5.45x39mm pp', 'weapon parts', 'car battery', 'nixxor lens', '.366 tkm ap-m', '9x18mm pm pbm gzh', 'can of thermite', '12/70 flechette', 
             'magnet', 'kite', 'rechargeable battery', 'lucky scav junk box',
             'ana tactical m1 armored rig', 'magazine case', 'ak-74 5.45x39 6l31 60-round magazine', 'cordura', 'army bandage', 'ripstop fabric',
             'grizzly medical kit', 'vaseline balm', 'surv12 field surgical kit', 'calok-b hemostatic applicator', 'ai-2 medkit', 'medical bloodset', 
             'can of condensed milk', 'Bottle of Tarkovskaya vodka', 'corrugated hose', 'clin window cleaner',
             'gas mask air filter', 'kirasa', 'kektape', 'fleece fabric', 'aluminum splint', 'blackrock chest rig', 'paracord', 'lshz light helmet',
             'soap', '6b5-16', '6b5-15', 'water filter', 'grenade case', 'magnum buckshot', 'power cord', 'broken lcd', 'broken gphone', 
             'round pliers', 'iskra', 'pack of sugar', 'can of beef stew (small)', 'kvass', 'coffee beans', 'sj1', 'portable defibrillator',
             'xtg-12', 'expeditionary fuel tank']

# hawk, fleece, 'pilgrim tourist backpack', 'vog-25',  Issues encountered


def component_acquisition(end_item_name):
  new_query = f"""
  {{
      items(name: "{end_item_name}") {{
          name
          avg24hPrice
          sellFor{{
            vendor{{
              name
            }}
            priceRUB
          }}          
          craftsFor {{
            rewardItems{{
              item{{
                name
              }}
              quantity
            }}
            requiredItems {{
              item {{
                name
                avg24hPrice
              }}
              quantity
            }}
          }}
      }}
  }}
  """
 
  result = run_query(new_query)
  #print(result['data']['items'])
  result = result['data']['items'][0]

  # Get highest vendor price
  vendor_name = "None"
  vendor_price = 0
  vendors = result['sellFor']
  for vendor in vendors:
    if int(vendor['priceRUB']) > vendor_price:
      vendor_name = vendor['vendor']['name']
      vendor_price = int(vendor['priceRUB'])
    #print(f"Vendor: {vendor['vendor']['name']}\nSells: {vendor['priceRUB']}")
  
  #print(f"{vendor_name}: {vendor_price} is the highest sale price")
  
  
  item_price = int(result['avg24hPrice'])
  
  # Exit program if exception occurs, then close the program
  try:
    output_price = item_price * int(result['craftsFor'][0]['rewardItems'][0]['quantity'])
  except Exception as e:
    print(f'Exception occurred with {result}\nError code {e}')
    sys.exit()
    
  items = result['craftsFor'][0]['requiredItems']
  #output_price = result['avg24hPirce']
  cost = 0
  for item in items:
      price = item['item']['avg24hPrice']
      name = item['item']['name']
      quantity = item['quantity']
    
      #print(f"{name}: {price} ---- {quantity}")
      cost += int(price) * int(quantity)

  flea_query = f"""
  {{
      items(name: "{end_item_name}") {{
          fleaMarketFee(price:{item_price})
          }}
  }}
  """
  flea_fee = run_query(flea_query)
  flea_fee = flea_fee['data']['items'][0]
  flea_fee = flea_fee['fleaMarketFee']
  #print(f"Old Fee: {result['fleaMarketFee']}\nNew Fee: {flea_fee}")

  return(output_price, cost, flea_fee, item_price, int(result['craftsFor'][0]['rewardItems'][0]['quantity']), vendor_name, vendor_price)


def main():
  start_index = 2


  ### Currently only accounts for 24 hour price of all items, does not account for trader
  ### lowest cost of anything. This results in inaccurate readings and must be accounted for.
  ### Priority should go to Trader Price if available
  sheets_handling_profits.update_single_cell('J2', 'UPDATING...')
  progress_bar(0, len(items_list))
  for index, item in enumerate(items_list):
    output_price, cost, fee, item_price, output_quantity, vendor_name, vendor_price = component_acquisition(item)
    #print(f'{item}: {expected_profit}')
    sheets_handling_profits.update_single_cell(f'A{start_index}', item)
    sheets_handling_profits.update_single_cell(f'B{start_index}', cost)
    sheets_handling_profits.update_single_cell(f'C{start_index}', fee)
    sheets_handling_profits.update_single_cell(f'D{start_index}', item_price)
    sheets_handling_profits.update_single_cell(f'E{start_index}', output_price)
    sheets_handling_profits.update_single_cell(f'F{start_index}', output_quantity)
    sheets_handling_profits.update_single_cell(f'H{start_index}', vendor_name)
    sheets_handling_profits.update_single_cell(f'I{start_index}', vendor_price)
    start_index += 1
    sleep(7)
    progress_bar(index + 1, len(items_list))

  print('\n### Projected Profits Updated')

  # Visual of time last updated for the sheet
  sheets_handling_profits.update_single_cell('J2', 'UPDATED')
  current_time = strftime("%m-%d %H:%M")
  sheets_handling_profits.update_single_cell('J3', current_time)

  ### On Projected Profits sheet
  # Simple Profit proves the sheet does not require item price to get
  # the accurate profit expectation.
  # However, the program may want the item price in a more convenient location
  # while grabbing additional info to compare to.
  # Must decide whether to remove "Item_Price" column or leave for future calculations.

# Run main for testing
if __name__ == "__main__":
  main()