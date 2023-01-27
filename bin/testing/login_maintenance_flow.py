# Logs in and takes care of a single item, to be expanded.

# Imports
import pyautogui as auto
from time import sleep

# Note: Starts with pre-purchased materials, simply collects and restarts crafts

# Collects and restarts the workbench craft
def refresh_workbench():
    while True:
        if auto.locateOnScreen('bin\Workbench.PNG', confidence=.9):
            auto.click(auto.moveTo(auto.locateCenterOnScreen('bin\Workbench.PNG', confidence=.9)))
            break
        else:
            for i in range(0, 15):
                auto.scroll(-1)
        sleep(1)
    auto.click(auto.moveTo(1588,824, duration=.5))
    sleep(2)
    auto.click(auto.moveTo(1588,863, duration=.5))
    auto.click(auto.moveTo(960,782, duration=1))
    
def refresh_lavatory():
    auto.click(auto.moveTo(auto.locateCenterOnScreen('bin\Lavatory.PNG', confidence=.9)))
    sleep(2)
    auto.click(auto.moveTo(1582,664, duration=.5))
    sleep(2)
    auto.click()
    sleep(1)
    auto.click(auto.moveTo(961,784, duration=.5))
    auto.moveTo(932, 1002, duration=.5)
    

def refresh_medical():
    auto.click(auto.moveTo(1619,609, duration=.5))
    sleep(2)
    auto.click()
    sleep(1)
    auto.click(auto.moveTo(961,784, duration=.5))
    auto.moveTo(932, 1002, duration=.5)

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
    sleep(1)
    auto.press('esc')
    sleep(1)
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
    """
    while True:
        
        if auto.locateOnScreen('bin\Workbench.PNG', confidence=.9):
            auto.moveTo(auto.locateCenterOnScreen('bin\Workbench.PNG', confidence=.9))
            break
        else:
            print('See nothing...')
            auto.scroll(-1)
        sleep(1)
    """

    login()
    auto.click(auto.moveTo(1372, 26, duration=.05))
    sleep(2)
    refresh_medical()
    sleep(2)
    refresh_lavatory()
    sleep(2)
    refresh_workbench()
    sleep(2)
    #logout()
    #sleep(interval)