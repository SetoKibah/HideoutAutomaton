# Purpose: Automate production in the hideout to produce mass profit to fund raids
# Utilize: API with https://tarkov.dev/ and create our own database.

### NEW CHANGES TO TARKOV
# Hideout Stations are currently able to search items, useful tool for automation
# Flea market is undergoing changes, will need monitoring.
# Need to standardize acquiring crafting materials and starting crafts
# Prepare for supervised testing, leading to unsupervised testing with logs


########################################## New Component Idea
# Handler for looted raid items to flea market
# Can pull image data from API (see GraphQL playground)
# Finish raids, leave items in top rows -> Bot runs until no items found
# On end logout

# Bot process
#   - Identify item
#   - Select filter
#   - Gets average price
#   - Places at average price
#   - IF item cannot sell to Flea, Sell to highest Vendor
#   - If no items are detected, assume done and exit game
##########################################


# imports
import logging
import bin.update_sheets as update_sheets


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
