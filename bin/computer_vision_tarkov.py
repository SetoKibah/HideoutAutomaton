# Experimenting with Computer Vision in Tarkov
# Meant for the scanning of certain values on certain areas of the screen

# Areas/values we want to look at and get
#   - Total Stash Value? (Needs Crop Region)
#   - Stash Rubles Count (Needs Crop Region)
#   - Stash Euros Count (Needs Crop Region)
#   - Stash USD Count (Needs Crop Region)
#   - Top flea value for selection? (Needs Crop Region)
#   - Flea fee price for input price (Needs Crop Region)

# Desired actions
#   - Determine profit from sale of items
#   - Track our monetary value over time
#   - Log actions performed in game
#   - Put hourly values into a spreadsheet, with timestamps of when collected
#   - Identify ROI of specified items we are crafting
#   - Effectively start crafts on a rotation
#   - Restock supplies for crafts, but stay under certain range
#   - Run constantly, including logging into the game and logging out
#   - Potentially monitor fuel remaining, possibility to replace fuel


### Computer Vision Testing, will convert to running program when working as intended
# Import dependencies
import pyautogui
import cv2
import numpy as np
import pytesseract
from time import sleep

# Set path for pytesseract (will need to change for different computers potentially if not set to PATH)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Top right money values: screen_array[40:80, 1650:, :]
# Total Stash Value on Overall: screen_array[740:790, 1050:1300, :]

def get_money_values():
    # Take screenshot
    screen = pyautogui.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region (Note height, width, not sure on 3rd)
    # (Works in a range(like 400:600, or 600:, or :600))
    cropped_region = screen_array[50:80, 1695:, :]
    # Corrected Colors
    corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)
    information = pytesseract.image_to_string(corrected_colors)
    return(information)

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

sleep(2)
# Navigate to locations and get the info
pyautogui.moveTo(pyautogui.locateCenterOnScreen(r"C:\Users\arche\Desktop\HideoutAutomaton\Character_Button.PNG", confidence = .8))
pyautogui.click()
sleep(1)
individual_values = get_money_values()
pyautogui.moveTo(pyautogui.locateCenterOnScreen(r"C:\Users\arche\Desktop\HideoutAutomaton\Overall.PNG", confidence = .8))
pyautogui.click()
sleep(1)
overall_value = get_stash_overall()
sleep(1)
pyautogui.press('esc')
value_list = individual_values.split(" ")
overall_value = overall_value.replace('\n', '')
print(f"\nOur overall ruble value is: ₽{overall_value}\nCurrent Rubles: ₽{value_list[0]}\nCurrent Euros: {value_list[1]}\nCurrent USD: {value_list[2]}" )
