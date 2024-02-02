from PIL import Image
import requests

def run_query(query):
    # Send a POST request to the API with the given query
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        # Return the response as JSON if the request is successful
        return response.json()
    else:
        # Raise an exception if the request fails
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

items_list = ['pile of meds']

for item_name in items_list:
    # Construct the query to retrieve the grid image link for the item
    query = f'''
    {{
        items(name:"{item_name}") {{
            gridImageLink
        }}
    }}
    '''
    # Execute the query and retrieve the data
    data = run_query(query)
    print(data)
    # Extract the grid image link from the data
    link = data['data']['items'][0]['gridImageLink']

    # Download the image data from the link
    img_data = requests.get(link).content
    # Save the image with the item name as the filename
    with open(f'images\{item_name}.png', 'wb') as handler:
        handler.write(img_data)
