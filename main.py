# Purpose: Automate production in the hideout to produce mass profit to fund raids
# Utilize: API with https://tarkov.dev/ and create our own database.

# imports
import logging
import update_sheets


# Setup basic logging configuration ()
logging.basicConfig(level=logging.INFO, filename="Automaton_main.log", filemode="w",
                    format="%(asctime)s 0 %(levelname)s - %(message)s")
# Logging levels DEBUG, INFO, WARNING, ERROR, CRITICAL are available for now. Will modify later

# Create a progress bar to track long-running sections
def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + ' ' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

# Main function to run our more purposeful code
if __name__ == "__main__":
    
    # Run our function to update the spreadsheet
    update_sheets.update_items()
    
    # Additional actions will be performed from here referring to this sheet of data.
    logging.info("Program successfully completed operation")
