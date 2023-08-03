import cv2
import numpy as np
import platform
import pyautogui

os_got = platform.system()
if os_got == "Darwin":
    screen_width, screen_height = pyautogui.size()
else:
    import pydirectinput
    screen_width, screen_height = pydirectinput.size()


def find_and_click_button(button_path):
    global screen_width, screen_height

    button_template = cv2.imread(button_path, cv2.IMREAD_GRAYSCALE)

    screenshot = pyautogui.screenshot()

    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(
        screenshot_gray, button_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.8:
        button_width, button_height = button_template.shape[::-1]
        button_x, button_y = max_loc[0] + \
            button_width // 2, max_loc[1] + button_height // 2

        pyautogui.moveTo(button_x, button_y, duration=2)
        if os_got == "Darwin":
            pyautogui.click(button_x, button_y)

        else:
            pydirectinput.click(button_x, button_y)
        return True
    else:
        return False


def find(button_path):
    global screen_width, screen_height
    button_template = cv2.imread(button_path, cv2.IMREAD_GRAYSCALE)

    screenshot = pyautogui.screenshot()

    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(
        screenshot_gray, button_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.8:
        button_width, button_height = button_template.shape[::-1]
        button_x, button_y = max_loc[0] + \
            button_width // 2, max_loc[1] + button_height // 2

        return (button_x, button_y)
    else:
        return False
