import cv2
import pyautogui
import pydirectinput
import numpy as np
import time


def find_and_click_button(button_path):
    # Load the button image (template)
    button_template = cv2.imread(button_path, cv2.IMREAD_GRAYSCALE)

    # Get the screen dimensions
    screen_width, screen_height = pyautogui.size()

    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(
        screenshot_gray, button_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Check if the template match is above a certain threshold
    if max_val > 0.8:
        # Get the button's coordinates
        button_width, button_height = button_template.shape[::-1]
        button_x, button_y = max_loc[0] + \
            button_width // 2, max_loc[1] + button_height // 2

        # Simulate a mouse click on the button's coordinates
        pyautogui.moveTo(button_x, button_y, duration=2)
        pydirectinput.click(button_x, button_y)
        return True
    else:
        return False


def find(button_path):
    # Load the button image (template)
    button_template = cv2.imread(button_path, cv2.IMREAD_GRAYSCALE)

    # Get the screen dimensions
    screen_width, screen_height = pyautogui.size()

    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(
        screenshot_gray, button_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Check if the template match is above a certain threshold
    if max_val > 0.8:
        # Get the button's coordinates
        button_width, button_height = button_template.shape[::-1]
        button_x, button_y = max_loc[0] + \
            button_width // 2, max_loc[1] + button_height // 2

        # Simulate a mouse click on the button's coordinates
        pyautogui.click
        return (button_x, button_y)
    else:
        return False


def tweenClick(x, y, duration=0.5):
    pydirectinput.moveTo(0, 0)
    stepsPsec = 120
    current_x, current_y = pydirectinput.position()

    steps = int(duration * stepsPsec)

    x_increment = (x - current_x) / steps
    y_increment = (y - current_y) / steps

    # Perform the tween movement
    for step in range(steps + 1):
        next_x = current_x + x_increment * step
        next_y = current_y + y_increment * step
        pydirectinput.moveTo(int(round(next_x)), int(round(next_y)))
        time.sleep(1 / stepsPsec)

    pydirectinput.moveTo(x, y)

    pydirectinput.click()
