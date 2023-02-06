import pyautogui as auto
from time import sleep
import cv2 as cv
import numpy as np
import random
import pytesseract as tess
import requests



def run_query(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def get_images():
    pass

item = 'pile of meds'
query = f"""
{{
    items(name: "{item}"){{
        name
        avg24hrPrice
    }}  
}}


"""
data = run_query(query)
print('Capturing')

while(True):
    
    screenshot = auto.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    cropped_region = screenshot[100:220, 1300:1450 :]
    cv.imshow('Computer Vision', cropped_region)
    if auto.locateOnScreen('test_image.png', confidence=.7):
        print('Found')
        break
    else:
        print('Not Found')
    # Look for item
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')