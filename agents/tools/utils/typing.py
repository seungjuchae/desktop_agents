# tools/utils/typing.py

import time
import re
from datetime import datetime
import pyautogui
import pyperclip

def contains_korean(text):
    return any('\uac00' <= char <= '\ud7a3' for char in text)

def split_by_language(text):
    return re.findall(r'[\uac00-\ud7a3]+|[^\uac00-\ud7a3]+', text)

def switch_language():
    print("🔄 Toggling language via Alt key...")
    pyautogui.keyDown('alt')
    time.sleep(0.1)
    pyautogui.keyUp('alt')
    time.sleep(0.5)

def paste_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)

def perform_keyboard_action(event, key):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⌨️ Performing {event} with key '{key}'")

    if event == "type":
        segments = split_by_language(key)
        current_lang = "english"

        for segment in segments:
            if contains_korean(segment):
                if current_lang != "korean":
                    switch_language()
                    current_lang = "korean"
                print(f"⌨️ Pasting Korean: {segment}")
                paste_text(segment)
            else:
                if current_lang != "english":
                    switch_language()
                    current_lang = "english"
                print(f"⌨️ Typing English: {segment}")
                pyautogui.write(segment, interval=0.05)

    elif event in [
        "copy", "paste", "cut", "undo", "redo", "save",
        "select_all", "delete_line", "new_tab", "close_tab"
    ]:
        pyautogui.hotkey(*key.lower().split("+"))

    elif event == "alt+tab":
        times = int(key.split("x")[-1]) if "x" in key else 1
        for _ in range(times):
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.2)

    elif event in ["back_navigation", "forward_navigation"]:
        direction = "left" if "left" in key else "right"
        pyautogui.hotkey("alt", direction)

    elif key.lower() in ["enter", "backspace", "tab", "esc", "space"]:
        pyautogui.press(key.lower())

    else:
        print(f"⚠️ Unknown keyboard event: {event} with key '{key}'")
