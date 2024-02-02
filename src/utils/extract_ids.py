import requests
import xlsxwriter

def run_query(query):
    """
    Sends a GraphQL query to the Tarkov API and returns the response.
    """
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def id_acquisition():
    """
    Retrieves IDs and other information related to hideout stations and crafts.
    """
    query = """
    {
        hideoutStations {
            name
            crafts {
                id
                level
                station {
                    name
                }
                requiredItems {
                    item {
                        name
                        id
                        avg24hPrice
                    }
                    count
                }
                rewardItems {
                    count
                    item {
                        id
                        name
                        avg24hPrice
                    }
                }
            }
        }
    }
    """
    # List creation
    id_list = [['ID', 'Name', 'Station', 'Station Level']]
    result = run_query(query)
    
    full_list = result['data']['hideoutStations']
    components_list = []
    
    for item in full_list:
        if item['crafts']:
            for craft_item in item['crafts']:
                reward_item = craft_item['rewardItems'][0]['item']
                station = craft_item['station']
                id_list.append([reward_item['id'], reward_item['name'], station['name'], craft_item['level']])
                
                if craft_item['requiredItems']:
                    required_item = craft_item['requiredItems'][0]['item']
                    components_list.append([required_item['id'], required_item['name']])
                    
    return id_list, components_list


if __name__ == "__main__":
    ids, components = id_acquisition()
    components_sorted = list(set(map(tuple, components)))
    
    print(len(components))
    print(len(components_sorted))
    
    components_sorted.insert(0, ['ID', 'Name'])
    
    with xlsxwriter.Workbook('ID and Names.xlsx') as workbook:
        worksheet_one = workbook.add_worksheet('Craft Rewards')
        worksheet_two = workbook.add_worksheet('Craft Components')
        
        for row_num, data in enumerate(ids):
            worksheet_one.write_row(row_num, 0, data)
        for row_num, data in enumerate(components_sorted):
            worksheet_two.write_row(row_num, 0, data)
