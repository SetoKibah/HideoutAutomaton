# HideoutAutomaton

This project is designed to take inputs from multiple sources, including the use of Computer Vision and API, to make intelligent decisions and emulate user action similar to what a human would do. The environment this exercise takes place in is Escape from Tarkov, specifically in the Hideout and Flea Market environments.

**Caution**: This is NOT intended as a cheat or advantage to any player, and should not be used to alter gameplay for any other player. This design in no way reads game memory or alters game files to its advantage. Abuse of such automated systems can result in bans to your account, you have been warned.

## Packages
  - pyautogui
  - requests
  - cv2
  - numpy
  - pytesseract
  - time
  - datetime
  - gspread
  - logging
  - xlsx

**Note**: pytesseract is a wrapper for the Tesseract OCR, and is not a standalone package. Installation of the Tesseract OCR is required. Example instructions on installation and first-time setup can be found here: https://stackabuse.com/pytesseract-simple-python-optical-character-recognition/

## Installation Instructions
Not implemented yet

## Intended use
Features may be added as the project becomes more complex, but the current design as of writing this Readme is stated as thus (June 15, 2022)
- The end-goal is to have this operate on items you choose in the hideout (one per station to start)  and dynamically check prices using in-game information and 3rd-party analytics, as well as log the performance of your sales and overall stash value over time. 
- GUI implementation is not planned as this will largely operate without supervision. 
- Option to add a specified run-time/interval is being considered, but not promised at this time.
- Login and logout to comply with Battlestate not wanting users logged in and idle.

## Issues and bugs
Any issues and bugs should be submitted for review. Pull requests are welcome and are reviewed ASAP.
Should you encounter a bug you cannot identify, get in touch with myself (Discord is the best place to direct message me, join at https://discord.com/invite/Z6TpQvm)
