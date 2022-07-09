import requests

# Function to send query out
def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def itemVScomponentQuery(item_input):
    # Query payload
    new_query = f"""
    {{
        items(name: "{item_input}") {{
            name
            sellFor{{
                price
                source
            }}
            craftsFor{{
                requiredItems{{
                    item{{
                        name
                        sellFor{{
                            price
                            source
                        }}
                    }}
                quantity
                }}
            }}
        }}
    }}

    """
    #cuts info down to dictionary that we use
    result = run_query(new_query)
    trimmed_result = result['data']
    trimmed_result = trimmed_result['items']
    trimmed_result = trimmed_result[0]

    return trimmed_result

def compare_itemprice_componentstotalprice(item_input):
    #gives us
    trimmed_result = itemVScomponentQuery(item_input)
    item_seller_list = trimmed_result["sellFor"]
    
    highest_price = 0
    for seller in item_seller_list:
        if seller["price"] > highest_price:
            highest_source = seller["source"]
            highest_price = seller["price"]
    item_highest_source = highest_source
    item_highest_price = highest_price
    
    component_list = trimmed_result["craftsFor"]
    component_list = component_list[0]
    component_list = component_list["requiredItems"]

    component_total_list= []
    component_total_price = 0
    for component in component_list:
        component_quantity = component["quantity"]
        component_item = component["item"]
        component_name = component_item["name"]
        component_total_list.append(f'{component_quantity}x {component_name}')

        component_seller_list = component_item["sellFor"]
        for seller in component_seller_list:
            if seller["price"] > highest_price:
                highest_source = seller["source"]
                highest_price = seller["price"]
        component_highest_source = highest_source
        component_highest_price = highest_price

        component_total_price += component_quantity * component_highest_price
    
    print(f'{item_input}-{item_highest_price},{component_total_list}-{component_total_price}')
    if item_highest_price > component_total_price:
        print("sell the item, you get more money")
    elif item_highest_price == component_total_price:
        print("they are the same")
    else:
        print("sell it in components, you get more money")

compare_itemprice_componentstotalprice('slickers')