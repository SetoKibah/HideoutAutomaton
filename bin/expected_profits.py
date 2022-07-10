import requests
from time import sleep
import sheets_handling_profits

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
             '5.45x39mm pp', '9x18mm PM Rg028', 'weapon parts', 'car battery', 'nixxor lens', '.366 tkm ap-m', 'kalashnikov ak-74m 5.45x39 assault rifle',
             '9x18mm pm pbm gzh', 'can of thermite', '12/70 flechette', 'magnet', 'kite', 'rechargeable battery', 'lucky scav junk box',
             'ana tactical m1 armored rig', 'magazine case', 'ak-74 5.45x39 6l31 60-round magazine', 'cordura', 'army bandage', 'ripstop fabric',
             'grizzly medical kit', 'vaseline balm', 'surv12 field surgical kit', 'calok-b hemostatic applicator', 'ai-2 medkit', 'medical bloodset', 
             'can of condensed milk', 'Bottle of Tarkovskaya vodka']

# hawk, fleece (multiple crafts)


def component_acquisition(end_item_name):
  new_query = f"""
  {{
      itemsByName(name: "{end_item_name}") {{
          name
          avg24hPrice
          fleaMarketFee
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
  result = result['data']['itemsByName'][0]

  output_price = int(result['avg24hPrice']) * int(result['craftsFor'][0]['rewardItems'][0]['quantity'])
  

  items = result['craftsFor'][0]['requiredItems']
  #output_price = result['avg24hPirce']
  cost = 0
  for item in items:
      price = item['item']['avg24hPrice']
      name = item['item']['name']
      quantity = item['quantity']
      #print(f"{name}: {price} ---- {quantity}")
      cost += int(price) * int(quantity)


#  print(f'\n\nEstimated Cost: {cost}')
#  print(f'Output Price: {output_price}')
#  print(f'Projected Profit: {(output_price) - cost}\n')
  return(output_price - cost - (int(result['fleaMarketFee']) * int(result['craftsFor'][0]['rewardItems'][0]['quantity'])))

start_index = 2


### Currently only accounts for 24 hour price of all items, does not account for trader
### lowest cost of anything. This results in inaccurate readings and must be accounted for.
### Priority should go to Trader Price if available

progress_bar(0, len(items_list))
for index, item in enumerate(items_list):
  expected_profit = component_acquisition(item)
  #print(f'{item}: {expected_profit}')
  sheets_handling_profits.update_single_cell(f'A{start_index}', item)
  sheets_handling_profits.update_single_cell(f'B{start_index}', expected_profit)
  start_index += 1
  sleep(1)
  progress_bar(index + 1, len(items_list))

print('\n### Projected Profits Updated')