from PIL import Image
import requests

def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

items_list = ['pile of meds']

for item_name in items_list:
    query = f'''
    {{
        items(name:"{item_name}") {{
            gridImageLink
        }}
    }}
    '''
    data = run_query(query)
    print(data)
    link = data['data']['items'][0]['gridImageLink']

    img_data = requests.get(link).content
    with open(f'images\{item_name}.png', 'wb') as handler:
        handler.write(img_data)

#im = Image.open('pile_of_meds.webp')
#im.save('pile_of_meds.png', format="png", lossless=True)