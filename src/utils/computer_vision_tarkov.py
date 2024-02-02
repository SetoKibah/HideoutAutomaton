from time import sleep
import datetime as dt
import pyautogui as pya
import cv2
import numpy as np
import pytesseract
import gspread
import sheets_handling_profits
import gspread
import pytesseract

# Global constant for confidence level in computer vision tasks
CONFIDENCE = 0.8

# Specific sheet for our data
# authenticating access
sa = gspread.service_account(filename=r'src\config\pysheetskeys.json')
# Connect to our spreadsheets
sh = sa.open("Tarkov Butler")
# Connect to our specific sheet
wks = sh.worksheet("Computer Vision")

# Set path for pytesseract (will need to change for different computers potentially if not set to PATH)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Function will search a specified column to get the bottom of the list.
def get_next_empty_cell(column):
    for i in range(1, 999):
        cell = wks.acell(f'{column}{i}').value
        if cell is None:
            start_point = (column, i)
            break
    return start_point

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

def update_values(rubles, euros, dollars, combined):
    # Get the next empty cell in the Rubles column
    rubles_cell = get_next_empty_cell('A')
    # Get the next empty cell in the Euros column
    euros_cell = get_next_empty_cell('B')
    # Get the next empty cell in the Dollars column
    dollars_cell = get_next_empty_cell('C')
    # Get the next empty cell in the Time column
    time_cell = get_next_empty_cell('E')
    # Get the next empty cell in the Date column
    date_cell = get_next_empty_cell('F')

    # Update the Rubles value in the corresponding cell
    wks.update(f'{rubles_cell[0]}{rubles_cell[1]}', rubles)
    # Update the Euros value in the corresponding cell
    wks.update(f'{euros_cell[0]}{euros_cell[1]}', euros)
    # Update the Dollars value in the corresponding cell
    wks.update(f'{dollars_cell[0]}{dollars_cell[1]}', dollars)
    # Update the combined ruble value in the corresponding cell
    wks.update(f'D{rubles_cell[1]}', combined)
    # Update the current time in the corresponding cell
    wks.update(f'{time_cell[0]}{time_cell[1]}', dt.datetime.now().strftime("%H:%M:%S"))
    # Update the current date in the corresponding cell
    wks.update(f'{date_cell[0]}{date_cell[1]}', dt.datetime.now().strftime("%Y-%m-%d"))
  
def total_liquid_rubles():
    # Take screenshot
    screen = pya.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region
    cropped_region = screen_array[42:74, 1620:1920, :]
    # Corrected Colors
    corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)
    
    # Get text from specified image area
    raw_string = pytesseract.image_to_string(corrected_colors)

    # Separate the string into 3 parts
    string_1, string_2, string_3 = raw_string.split(' ')
    
    # Remove the first character from each string
    string_1 = string_1[1:]
    string_2 = string_2[1:]
    string_3 = string_3[1:]
    
    # Convert each string to int
    int_1 = int(string_1)
    int_2 = int(string_2)
    int_3 = int(string_3)
    
    # Print the values of the 3 strings
    print(f'Rubles: ₽{int_1:,}\nEuros: €{int_2:,}\nDollars: ${int_3:,}')
    
    # Calculate the combined value in rubles
    combined = int_1 + (int_2 * 158) + (int_3 * 143)
    
    # Print the combined value formatted in rubles with commas
    print(f'Combined in Rubles: ₽{combined:,}')
    
    return int_1, int_2, int_3, combined

if __name__ == "__main__":
    rubles, euros, dollars, combined = total_liquid_rubles()
    update_values(rubles, euros, dollars, combined)

    
"""
### Block used for constantly showing current frames, keeping as a test tool for narrowing down areas

# Loop over frames
while True:
    # Take screenshot
    screen = pya.screenshot()
    # Convert to numpy array
    screen_array = np.array(screen)
    # Crop region (Note height, width, not sure on 3rd)
    # (Works in a range(like 400:600, or 600:, or :600))
    cropped_region = screen_array[42:74, 1620:1920, :]
    # Corrected Colors
    corrected_colors = cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR)
    # Handle rendering
    cv2.imshow('ScreenCap', corrected_colors)
    
    # Will get text from specified image area
    #print(pytesseract.image_to_string(corrected_colors))

    # Cv2.waitkey
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
 

# Close down the frame
cv2.destroyAllWindows()
"""
