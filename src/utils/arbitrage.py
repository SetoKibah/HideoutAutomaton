# This tool will find items within instant-profit range for reselling to traders
# Requires trader price and average 24 hour price
import collections
import collections.abc
collections.MutableMapping = collections.abc.MutableMapping
import sys
import requests
from collections.abc import MutableMapping
from time import sleep, strftime
import tools_sheets


def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def progress_bar(progress, total, row):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + ' ' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%, row {row}", end="\r")
  
def data_clean():
    start_index = 2
    query = f"""
  {{
      items{{
          name
          avg24hPrice
          low24hPrice
          sellFor{{
              vendor{{
                  name
              }}
              priceRUB
          }}
      }}
  }}
  """
    data_raw = run_query(query)
    data_list = data_raw['data']['items']

    print(f'Length of data: {len(data_list)}')

    progress_bar(0, len(data_list), 0)
    for index,item in enumerate(data_list):
        name, average_price, low_price = item['name'], item['avg24hPrice'], item['low24hPrice']
        
        highest_vendor, highest_price = None, 0
        for vendor in item['sellFor']:
            #print(vendor['vendor']['name'])
            #print(vendor['priceRUB'])
            if int(vendor['priceRUB']) > highest_price:
                if vendor['vendor']['name'] == "Flea Market":
                    flea_price = int(vendor['priceRUB'])
                else:
                    highest_vendor = vendor['vendor']['name']
                    highest_price = int(vendor['priceRUB'])
        #abs_difference = abs(average_price - highest_price)
        #print(f"Name: {name}\nAverage Flea: {average_price}\n{highest_vendor}: {highest_price}\nAbs Dif: {abs_difference}")
        #print(name)
        if low_price != None:
            if highest_price > low_price:
             #   print(f'Name: {name}')
             #   print(f'Low 24hr vs highest price: {low_price} vs {highest_price}')
                tools_sheets.update_single_cell(f'A{start_index}', name)
                tools_sheets.update_single_cell(f'B{start_index}', average_price)
                tools_sheets.update_single_cell(f'C{start_index}', low_price)
                tools_sheets.update_single_cell(f'D{start_index}', highest_price)
                tools_sheets.update_single_cell(f'E{start_index}', highest_vendor)
                start_index += 1
                sleep(5)
        progress_bar(index + 1, len(data_list), start_index - 1)
if __name__ == "__main__":
    data_clean()
    print('Complete')