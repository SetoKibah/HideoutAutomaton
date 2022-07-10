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
            craftsFor{{
                requiredItems{{
                    item{{
                        name
                        sellFor{{
                            price
                            vendor{{
                                name
                            }}
                        }}
                    }}
                    quantity
                }}
                rewardItems{{
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
    trimmed_result = result['data']['items'][0]


    return trimmed_result

def highest_seller(list_of_vendors):
    #must be the list of sellFor
    highest_price = 0
    for seller in list_of_vendors:
        if seller["price"] > highest_price and seller["source"] != "fleaMarket":
            highest_source = seller["source"]
            highest_price = seller["price"]
    item_highest_source = highest_source
    item_highest_price = highest_price
    
    return (item_highest_price,item_highest_source)

def highest_vendor(list_of_vendors):
    #must be the list of sellFor
    highest_price = 0
    for seller in list_of_vendors:
        if seller["price"] > highest_price and seller["vendor"]["name"] != "Flea Market":
            highest_source = seller["vendor"]["name"]
            highest_price = seller["price"]
    item_highest_source = highest_source
    item_highest_price = highest_price

    return (item_highest_price,item_highest_source)

def compare_itemprice_componentstotalprice(item_input):
    #trimmed_information
    trimmed_result = itemVScomponentQuery(item_input)["craftsFor"][0]
    trimmed_reward = trimmed_result["rewardItems"][0]
    trimmed_reward_seller_list = trimmed_reward["item"]["sellFor"]

    #item information
    reward_name = trimmed_reward["item"]["name"]
    reward_quantity = trimmed_reward["quantity"]
    reward_price = highest_seller(trimmed_reward_seller_list)[0]
    reward_vendor = highest_seller(trimmed_reward_seller_list)[1]
    reward_total_price = reward_quantity * reward_price
    
        #Note to self: maybe add a component_total_list= []
    
    #component information
    trimmed_components = trimmed_result["requiredItems"]
    component_total_list= []
    component_total_price = 0
    for component in trimmed_components:
        component_quantity = component["quantity"]
        component_name = component["item"]["name"]
        component_total_list.append(f'{component_quantity}x {component_name}')
        component_seller_list = component["item"]["sellFor"]
        component_price = highest_vendor(component_seller_list)[0]
        component_vendor = highest_vendor(component_seller_list)[1]
        
        component_total_price += component_quantity * component_price

    #presenting and decision
    print(f'{item_input}-{reward_total_price},{component_total_list}-{component_total_price}')
    if reward_total_price > component_total_price:
        print("sell the item, you get more money")
    elif reward_total_price == component_total_price:
        print("they are the same")
    else:
        print("sell it in components, you get more money")

if __name__ == "__main__":
    compare_itemprice_componentstotalprice('slickers')