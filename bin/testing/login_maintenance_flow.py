# Logs in and takes care of a single item, to be expanded.

# Imports
import pyautogui as auto
from time import sleep

# Note: Starts with pre-purchased materials, simply collects and restarts crafts

# Collects and restarts the workbench craft
def refresh_workbench():
    auto.click(auto.moveTo(774,114, duration=.5))
    sleep(2)
    auto.click(auto.moveTo(1586,823, duration=.5))
    sleep(2)
    auto.click(auto.moveTo(1589,861, duration=.5))
    sleep(2)
    auto.click(auto.moveTo(959,785, duration=.5))
    sleep(2)
    auto.press('esc')

def refresh_lavatory():
    pass

def refresh_medical():
    pass

# Logs into the game and awaits at menu
def login():
    auto.press('win')
    auto.typewrite('battlestate', interval=.05)
    auto.press('enter')
    sleep(8)
    auto.click(auto.moveTo(864, 519, duration=.1))
    auto.typewrite('', interval=.05)
    auto.press('enter')
    auto.sleep(8)
    auto.click(auto.moveTo(1333,812, duration=.5))
    auto.sleep(90)
    auto.click(auto.moveTo(225,1069, duration=.5))
    auto.sleep(75)
    
    
    
# Exits game completely
def logout():
    auto.press('esc')
    sleep(1)
    auto.press('esc')
    auto.click(auto.moveTo(956,951, duration=.5))
    sleep(.5)
    auto.press('y')


if __name__ == "__main__":
    
    # 32min 15 seconds duration pcb craft
    # 46 minute wait to wait for all crafts (ideal)
    # Can scroll along the bottom
    # Important variables
    interval = 1935
    runs = 10
    sleep(5)
    
    while True:
        
        if auto.locateOnScreen('bin\Workbench.PNG', confidence=.9):
            auto.moveTo(auto.locateCenterOnScreen('bin\Workbench.PNG', confidence=.9))
            break
        else:
            print('See nothing...')
            auto.scroll(-1)
        sleep(1)
    
    
    #login()
    #refresh_workbench()
    
    
    #for i in range(0, runs):
    #    login()
    #    refresh_workbench()
    #    sleep(2)
    #    logout()
    #    print(f"Run {i+1} complete. Sleeping {interval/60} minutes...")
    #    sleep(interval)
    