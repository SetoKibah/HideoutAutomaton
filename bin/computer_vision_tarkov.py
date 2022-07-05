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
import pyautogui
import cv2
import numpy as np
import pytesseract
import gspread
from time import sleep
import time
import datetime as dt

# Specific sheet for our data
# authenticating access
sa = gspread.service_account(filename=r'C:\Users\arche\Desktop\HideoutAutomaton\pysheetskeys.json')
# Connect to our spreadsheets
sh = sa.open("General Budgeting")
# Connect to our specific sheet
wks = sh.worksheet("Tarkov Calculations")

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

# Top right money values: screen_array[40:80, 1650:, :]
# Total Stash Value on Overall: screen_array[740:790, 1050:1300, :]

# Function meant to get the current liquid money values in the stash, assumes a 1920x1080 resolution.
def get_money_values():
    # Take screenshot
    screen = pyautogui.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region (Note height, width, not sure on 3rd)
    # (Works in a range(like 400:600, or 600:, or :600))
    cropped_region = screen_array[50:80, 1640:, :]
    # Corrected Colors
    corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)
    information = pytesseract.image_to_string(corrected_colors)
    return(information)

# Gets the information for overall stash value according to the game, assumes a 1920x1080 resolution
def get_stash_overall():
    # Take screenshot
    screen = pyautogui.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region (Note height, width, not sure on 3rd)
    # (Works in a range(like 400:600, or 600:, or :600))
    cropped_region = screen_array[740:790, 1050:1300, :]
    # Corrected Colors
    corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)
    information = pytesseract.image_to_string(corrected_colors)
    return(information)


### Block used for constantly showing current frames, keeping as a test tool for narrowing down areas
"""
# Loop over frames
while True:
    # Take screenshot
    screen = pyautogui.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region (Note height, width, not sure on 3rd)
    # (Works in a range(like 400:600, or 600:, or :600))
    cropped_region = screen_array[740:790, 1050:1300, :]
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

### Logic testing and method planning
sleep(2)
# Navigate to locations and get the info
# First move to the main stash by selecting the Character button
pyautogui.moveTo(pyautogui.locateCenterOnScreen(r"C:\Users\arche\Desktop\HideoutAutomaton\Character_Button.PNG", confidence = .8))
pyautogui.click()
sleep(1)
# Read the values and save the list
individual_values = get_money_values()

# Repeat the process for overall stash value
pyautogui.moveTo(pyautogui.locateCenterOnScreen(r"C:\Users\arche\Desktop\HideoutAutomaton\Overall.PNG", confidence = .8))
pyautogui.click()
sleep(1)
overall_value = get_stash_overall()
sleep(1)

# Return to the main menu when complete
pyautogui.press('esc')
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
wks.update(f'F{start[1]}', float(overall_value))

