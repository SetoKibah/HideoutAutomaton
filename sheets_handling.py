# Handles uploading data to google sheets for our database.

# imports
import gspread
import datetime as dt

# authenticating access
sa = gspread.service_account(filename='pysheetskeys.json')
# Connect to our spreadsheets
sh = sa.open("General Budgeting")
# Connect to our specific sheet
wks = sh.worksheet("TestSheet")

# Function will search a specified column to get the bottom of the list.
def get_next_empty_cell(column):
    for i in range(1,999):
        cell = wks.acell(f'{column}{i}').value
        if cell == None:
            start_point = (column, i)
            break
        
    return start_point
        
# Used for updating one cell at a time, applicable for updating a list over time.
def update_single_cell(values, input_value):
    column, index = values
    value = input_value
    wks.update(f"{column}{index}", float(value))

# Update going out through the rows (ported from test sheets, will alter to be more specific later)
def update_row(name, value, start_row):
    column, index = start_row
    current_date = dt.date.today()
    current_time = dt.datetime.now()
    current_time = current_time.strftime("%H:%M")
    wks.update(f"A{index}", name)
    wks.update(f"B{index}", float(value))
    wks.update(f"C{index}", current_time)
    wks.update(f"D{index}", str(current_date))
  