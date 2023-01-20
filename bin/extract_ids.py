import requests
from time import sleep
import xlsxwriter
import itertools

def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def id_acquisition():
    new_query = f"""
    {{
        hideoutStations{{
        name
        crafts{{
            id
            level
            station{{
                name
            }}
            requiredItems{{
                item{{
                    name
                    id
                    avg24hPrice
                }}
                count
            }}
            rewardItems{{
                count
                item{{
                    id
                    name
                    avg24hPrice
                }}
            
            }}
        }}
        }}
    }}
    """
    # List creation
    id_list = []
    id_list.append(['ID', 'Name', 'Station', 'Station Level'])
    result = run_query(new_query)
    
    full_list = result['data']['hideoutStations']
    components_list = []
    
    for item in full_list:
        if item['crafts'] != []:
            for craft_item in item['crafts']:
                id_list.append([craft_item['rewardItems'][0]['item']['id'],craft_item['rewardItems'][0]['item']['name'], craft_item['station']['name'], craft_item['level']])
                if craft_item['requiredItems'] != []:
                    components_list.append([craft_item['requiredItems'][0]['item']['id'],craft_item['requiredItems'][0]['item']['name']])
                    
    return id_list, components_list


if __name__ == "__main__":
    ids, components = id_acquisition()
    components_sorted = list(set(map(tuple,components)))
    print(len(components))
    print(len(components_sorted))
    components_sorted.insert(0, ['ID','Name'])
    
    with xlsxwriter.Workbook('ID and Names.xlsx') as workbook:
        worksheet_one = workbook.add_worksheet('Craft Rewards')
        worksheet_two = workbook.add_worksheet('Craft Components')
        
        for row_num, data in enumerate(ids):
            worksheet_one.write_row(row_num, 0, data)
        for row_num, data in enumerate(components_sorted):
            worksheet_two.write_row(row_num, 0, data)
            
    