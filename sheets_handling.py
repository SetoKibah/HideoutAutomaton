# Handles uploading data to google sheets for our database.

# imports
import gspread
import datetime as dt
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.DEBUG, filename="Automaton.log", filemode="w",
                    format="%(asctime)s 0 %(levelname)s - %(message)s")

# authenticating access
sa = gspread.service_account(filename='pysheetskeys.json')
# Connect to our spreadsheets
sh = sa.open("General Budgeting")
# Connect to our specific sheet
wks = sh.worksheet("TestSheet")
logging.info('Google sheets authentication successful')

# Function will search a specified column to get the bottom of the list.
def get_next_empty_cell(column):
    for i in range(1,999):
        cell = wks.acell(f'{column}{i}').value
        if cell == None:
            start_point = (column, i)
            break
    logging.info(f"start poing for next empty cell {start_point}")
    return start_point
        
# Used for updating one cell at a time, applicable for updating a list over time.
def update_single_cell(values, input_value):
    column, index = values
    value = input_value
    wks.update(f"{column}{index}", float(value))
    logging.info('Single Cell update action complete')

# Update going out through the rows (ported from test sheets, will alter to be more specific later)
def update_row(name, value, start_row):
    logging.info('Update row action start')
    column, index = start_row
    current_date = dt.date.today()
    current_time = dt.datetime.now()
    current_time = current_time.strftime("%H:%M")
    wks.update(f"A{index}", name)
    wks.update(f"B{index}", float(value))
    wks.update(f"C{index}", current_time)
    wks.update(f"D{index}", str(current_date))
    logging.info('Update row action complete')