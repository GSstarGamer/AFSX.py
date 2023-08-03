from functions.ssFindnClick import find as find
from functions.ssFindnClick import find_and_click_button


def wait(button):
    while True:
        windowsOpen = find(button)
        if windowsOpen:
            break
        else:
            pass
    return


def clickTillgone(button):
    if not find(button):
        return False
    for i in range(1000):
        if find(button):
            find_and_click_button(button)
        else:
            return True
    return False
