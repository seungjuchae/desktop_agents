# tools/utils/screenshot.py
import pyautogui
import os

def take_screenshot(filename):
    path = os.path.join("screenshots", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pyautogui.screenshot(path)
    print(f"📸 Screenshot saved: {path}")
    return path
