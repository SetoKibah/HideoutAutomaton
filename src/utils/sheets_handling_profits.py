# Handles uploading data to google sheets for our database.

# imports
import gspread
import datetime as dt
import logging

# Setup basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    filename="Automaton.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s: %(message)s"  # Updated log message format
)

# authenticating access
sa = gspread.service_account(filename=r'C:\Users\Bradley\Desktop\HideoutAutomaton\HideoutAutomaton\bin\pysheetskeys.json')
# Connect to our spreadsheets
sh = sa.open("Tarkov Butler")
# Connect to our specific sheet
wks = sh.worksheet("Projected Profits")
logging.info('Google sheets authentication successful')

# Function to check an item value in the list (meant for the computer_vision bit currently)
def check_item(item_name):
    values = wks.get_all_values()
    average_price = 0
    for value in values:
        if item_name in value:
            logging.info(f'Item {item_name} current average value is: {value[2]}')  # Log the item value
            average_price = value[2]
    return average_price

# Function will search a specified column to get the bottom of the list.
def get_next_empty_cell(column):
    for i in range(1, 999):
        cell = wks.acell(f'{column}{i}').value
        if cell == None:
            start_point = (column, i)
            break
    logging.info(f"Start looking for next empty cell: {start_point}")  # Log the start point
    return start_point

# Used for updating one cell at a time, applicable for updating a list over time.
def update_single_cell(cell, input_value):
    wks.update(cell, input_value)
