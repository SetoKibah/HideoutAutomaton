import requests
from time import sleep
import csv

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
        }}
        }}
    }}
    """
    id_list = []
    id_list.append(['ID', 'Station', 'Station Level'])
    result = run_query(new_query)
    full_list = result['data']['hideoutStations']
    for item in full_list:
        if item['crafts'] != []:
            print(item['name'])
            for craft_item in item['crafts']:
                id_list.append([craft_item['id'], craft_item['station']['name'], craft_item['level']])
    return id_list
if __name__ == "__main__":
    ids = id_acquisition()
    
    print(len(ids))
    f = open('id_list.csv', 'w')
    writer = csv.writer(f)
    for id in ids:
        print(id)
        writer.writerow(id)
    f.close()