# Experimenting with Computer Vision in Tarkov
# Meant for the scanning of certain values on certain areas of the screen

# Areas/values we want to look at and get
#   - Total Stash Value? (COMPLETE)
#   - Stash Rubles Count (COMPLETE)
#   - Stash Euros Count (COMPLETE)
#   - Stash USD Count (COMPLETE)
#   - Top flea value for selection? (Needs Crop Region)
#   - Flea fee price for input price (Needs Crop Region)

# Desired actions (After basic flea market understanding is achieved)
#   - Determine profit from sale of items ------------------------------------[]
#   - Track our monetary value over time -------------------------------------[]
#   - Log actions performed in game ------------------------------------------[]
#   - Put hourly values into a spreadsheet, with timestamps of when collected []
#   - Identify ROI of specified items we are crafting ------------------------[]
#   - Effectively start crafts on a rotation ---------------------------------[]
#   - Restock supplies for crafts, but stay under certain range --------------[]
#   - Run constantly, including logging into the game and logging out --------[]
#   - Potentially monitor fuel remaining, possibility to replace fuel --------[]


### Computer Vision Testing, will convert to running program when working as intended
# Import dependencies
import pyautogui as pya
import cv2
import numpy as np
import pytesseract
import gspread
from time import sleep
import sheets_handling_profits
import time
import datetime as dt

# Global Confidence Variable
CONFIDENCE = 0.8

# Specific sheet for our data
# authenticating access
sa = gspread.service_account(filename='pysheetskeys.json')
# Connect to our spreadsheets
sh = sa.open("Tarkov Butler")
# Connect to our specific sheet
wks = sh.worksheet("Computer Vision")

# Function will search a specified column to get the bottom of the list.
def get_next_empty_cell(column):
    for i in range(1,999):
        cell = wks.acell(f'{column}{i}').value
        if cell == None:
            start_point = (column, i)
            break
    return start_point


# Set path for pytesseract (will need to change for different computers potentially if not set to PATH)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

##### Temporary Important Info Locations
# Top right money values: screen_array[40:80, 1650:, :]
# Total Stash Value on Overall: screen_array[740:790, 1050:1300, :]

# Function gets a specific area of the screen, reads it, and returns the info
def get_specified_info(x1, x2, y1, y2):
    # Take screenshot
    screen = pya.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region (Note height, width, not sure on 3rd)
    # (Works in a range(like 400:600, or 600:, or :600))
    cropped_region = screen_array[x1:x2, y1:y2, :]
    # Corrected Colors
    #corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)
    information = pytesseract.image_to_string(cropped_region)
    return(information)

# Start from Main. Used to update current values
def update_values():
    sleep(2)
    # Navigate to locations and get the info
    # First move to the main stash by selecting the Character button
    pya.moveTo(pya.locateCenterOnScreen("Character_Button.PNG", confidence = CONFIDENCE))
    pya.click()
    sleep(2)
    # Read the values and save the list
    individual_values = get_specified_info(50, 80, 1640, None)

    # Repeat the process for overall stash value
    pya.moveTo(pya.locateCenterOnScreen("Overall.PNG", confidence = CONFIDENCE))
    pya.click()
    sleep(2)
    overall_value = get_specified_info(740, 800, 1050, 1300)
    sleep(1)

    # Return to the main menu when complete
    pya.press('esc')
    value_list = individual_values.split(" ")
    overall_value = overall_value.replace('\n', '')

    # Display information and compare to actual values for review
    print(f"\nOur overall ruble value is: ₽{overall_value}\nCurrent Rubles: ₽{value_list[0]}\nCurrent Euros: {value_list[1]}\nCurrent USD: {value_list[2]}" )

    # Append data to our google sheets
    # Format: Date, Time, Overall, Ruble Liq, Euro Liq, Dollar Liq

    # Getting date and time format setup
    today = dt.datetime.now()
    today_string = today.strftime("%m-%d-%Y %H:%M")
    today_list = today_string.split(' ')
    now = today_list[1]
    today = today_list[0]

    # Upload to google sheet
    start = get_next_empty_cell('A')

    wks.update(f'A{start[1]}', today)
    wks.update(f'B{start[1]}', now)
    wks.update(f'C{start[1]}', float(value_list[0][1:]))
    wks.update(f'D{start[1]}', float(value_list[1][1:]))
    wks.update(f'E{start[1]}', float(value_list[2][1:]))
    try:
        wks.update(f'F{start[1]}', float(overall_value))
    except:
        print('Awful read, print failure to sheet and move on')
        wks.update(f'F{start[1]}', 'Bad read')


### Block used for constantly showing current frames, keeping as a test tool for narrowing down areas

# Loop over frames
while True:
    # Take screenshot
    screen = pya.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region (Note height, width, not sure on 3rd)
    # (Works in a range(like 400:600, or 600:, or :600))
    cropped_region = screen_array[150:190, 1340:1500, :]
    # Corrected Colors
    corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)
    # Handle rendering
    cv2.imshow('ScreenCap', corrected_colors)
    
    # Will get text from specified image area
    #print(pytesseract.image_to_string(corrected_colors))
    #sleep(30)
    
    # Cv2.waitkey
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
 

# Close down the frame
cv2.destroyAllWindows()
"""
update_values()

###### Navigate to Flea and determine if item is within purchase parameters
item_in_question = 'ai-2'
print('Seeking...')
sleep(2)
pya.click(pya.moveTo(pya.locateCenterOnScreen('Flea_Market_Button.PNG', confidence = CONFIDENCE), duration = .5))
sleep(1)
pya.click(pya.moveTo(123, 120, duration = .5))
pya.typewrite(item_in_question, interval=.1)
sleep(2)
pya.click(pya.moveTo(123, 160, duration = .5))
sleep(3)

#################### Section looks at the top price in the list (assumed to be the lowest)
test_price = get_specified_info(150, 190, 1340, 1500)
#####################
#test_price = int(test_price.replace('p', ''))

print(f'The value the program sees is: {test_price}')
# If the value is in Euros, should convert to equivalent ruble value
if '€' in test_price:
    test_price.replace('€', '')
    test_price = int(test_price) * 114
    print(f'The equivalent in rubles is {test_price}')
elif 'p' in test_price:
    test_price.replace('p', '')
    print(f'Cleaned value: {test_price}')

pya.press('esc')
"""