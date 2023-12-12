import pyautogui as pya
import cv2
import numpy as np
import pytesseract
from time import sleep


# Get image data
def pull_image_query():
    pass

# Request price data for item
def pull_price_data():
    pass


if __name__ == "__main__":

    # Loop over frames and search for items
    while True:
        # Take screenshot
        screen = pya.screenshot()
        # Convert to numpy array
        screen_array = np.array(screen)
        # Crop region (Note height, width, not sure on 3rd)
        # (Works in a range(like 400:600, or 600:, or :600))
        cropped_region = screen_array[70:900, 1250:, :]
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