import os
import pyautogui
import time
import subprocess
from pynput.keyboard import Key, Controller
from agents.tools.utils.typing import perform_keyboard_action

from agents.tools.base import BaseTool

keyboard = Controller()

class KeyboardTool(BaseTool):
    supported_actions = {
        "type", "copy", "paste", "rename", "alt_tab", "language_change",
        "search", "open_app", "open_folder", "search_and_launch",
        "type_in_writer", "get_alt_tab_order",
        "search_file", "search_folder", "rename_file", "rename_folder"
    }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        if name == "type":
            perform_keyboard_action("type", action.get("text", ""))

        elif name == "copy":
            pyautogui.hotkey("ctrl", "c")

        elif name == "paste":
            pyautogui.hotkey("ctrl", "v")

        elif name in ["rename", "rename_file", "rename_folder"]:
            pyautogui.press("f2")

        elif name == "alt_tab":
            num = action.get("count", 1)
            delay = action.get("delay", 0.5)
            self._alt_tab(num, delay)

        elif name == "language_change":
            pyautogui.keyDown("alt")
            pyautogui.press("shift")
            pyautogui.keyUp("alt")

        elif name in ["search", "search_file", "search_folder"]:
            pyautogui.hotkey("ctrl", "f")

        elif name == "open_app":
            app_name = action.get("app_name", "")
            pyautogui.press("winleft")
            time.sleep(2)
            pyautogui.write(app_name)
            pyautogui.press("enter")

        elif name == "open_folder":
            folder = action.get("folder_path", "")
            pyautogui.press("winleft")
            time.sleep(2)
            pyautogui.write(folder)
            pyautogui.press("enter")

        elif name == "search_and_launch":
            self._search_and_launch(
                action.get("app_name", ""),
                action.get("delay", 0.7),
                action.get("enter", True)
            )

        elif name == "type_in_writer":
            perform_keyboard_action("type", action.get("text", ""))

        elif name == "get_alt_tab_order":
            result = self._get_alt_tab_order(debug=action.get("debug", False))
            print("🧠 Alt-Tab Order:", result)

        else:
            print(f"⚠️ KeyboardTool: Unknown action {name}")

    # --- Private helpers ---

    def _search_and_launch(self, name: str, delay: float = 0.7, enter: bool = True):
        subprocess.run(["xdotool", "key", "Super_L"])
        time.sleep(delay)
        subprocess.run(["xdotool", "type", name])
        time.sleep(2)
        if enter:
            subprocess.run(["xdotool", "key", "Return"])

    def _alt_tab(self, num=1, delay=0.5):
        time.sleep(2)
        keyboard.press(Key.alt)
        time.sleep(delay)
        for _ in range(num):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(delay)
        keyboard.release(Key.alt)

    def _get_alt_tab_order(self, debug=False):
        try:
            stacking = subprocess.check_output(["xprop", "-root", "_NET_CLIENT_LIST_STACKING"]).decode()
            window_ids = stacking.strip().split("#")[-1].strip().split(", ")
            if debug:
                print("[DEBUG] Window IDs (stacking):", window_ids)

            wmctrl_output = subprocess.check_output(["wmctrl", "-lx"]).decode()
            if debug:
                print("[DEBUG] wmctrl output:\n", wmctrl_output)

            window_map = {}
            for line in wmctrl_output.splitlines():
                parts = line.split(None, 4)
                if len(parts) >= 5:
                    win_id = parts[0].lower()
                    win_class = parts[2]
                    win_title = parts[4]
                    app_name = win_class.split('.')[-1]
                    window_map[win_id] = (app_name, win_title)

            ordered_apps = []
            for wid in window_ids[::-1]:
                wid_clean = wid.strip().lower().replace("0x", "")
                wid_normalized = f"{int(wid_clean, 16):08x}"
                key = f"0x{wid_normalized}"
                if key in window_map:
                    ordered_apps.append(window_map[key])
                elif debug:
                    print(f"[WARN] No match for {key}")

            return ordered_apps

        except Exception as e:
            print(f"[ERROR] {e}")
            return []













































# import subprocess
# import time
# import time

# from pynput.keyboard import Key, Controller


# def search_and_launch(name: str, delay: float = 0.7, enter: bool = True):
#     """
#     Opens GNOME Activities search and types the given app name.

#     Args:
#         name (str): The text to search for (e.g., 'libreoffice calc').
#         delay (float): Delay after pressing Super key (default 0.7 seconds).
#         enter (bool): Whether to press Enter after typing (default True).
#     """
#     # Press Super key to open Activities
#     subprocess.run(["xdotool", "key", "Super_L"])
#     time.sleep(delay)

#     # Type the search query
#     subprocess.run(["xdotool", "type", name])
#     time.sleep(0.2)

#     # Press Enter to launch the selected app (optional)
#     if enter:
#         subprocess.run(["xdotool", "key", "Return"])

# # Example usage:
# # search_and_launch("libreoffice calc")


# keyboard = Controller()


# def alt_tab(num=1, delay=0.5):
#     """
#     Simulate holding Alt and pressing Tab `num` times to switch windows.
    
#     Args:
#         num (int): Number of times to press Tab while holding Alt.
#         delay (float): Delay between key events in seconds.
#     """
#     time.sleep(2)  # Give yourself time to focus the right window

#     keyboard.press(Key.alt)
#     time.sleep(delay)

#     for _ in range(num):
#         keyboard.press(Key.tab)
#         keyboard.release(Key.tab)
#         time.sleep(delay)

#     keyboard.release(Key.alt)

# # Example usage:
# # alt_tab(3)  # Press Alt+Tab 3 times


# def get_alt_tab_order(debug=False):
#     """
#     Returns a list of (app_name, window_title) in GNOME Alt+Tab order.

#     Args:
#         debug (bool): Print debug info if True.
#     Returns:
#         List of tuples: [(app_name, window_title), ...]
#     """
#     try:
#         stacking = subprocess.check_output(["xprop", "-root", "_NET_CLIENT_LIST_STACKING"]).decode()
#         window_ids = stacking.strip().split("#")[-1].strip().split(", ")
#         if debug:
#             print("[DEBUG] Window IDs (stacking):", window_ids)

#         wmctrl_output = subprocess.check_output(["wmctrl", "-lx"]).decode()
#         if debug:
#             print("[DEBUG] wmctrl output:\n", wmctrl_output)

#         window_map = {}
#         for line in wmctrl_output.splitlines():
#             parts = line.split(None, 4)
#             if len(parts) >= 5:
#                 win_id = parts[0].lower()
#                 win_class = parts[2]
#                 win_title = parts[4]
#                 app_name = win_class.split('.')[-1]
#                 window_map[win_id] = (app_name, win_title)

#         ordered_apps = []
#         for wid in window_ids[::-1]:  # Reverse = top window first
#             wid_clean = wid.strip().lower().replace("0x", "")
#             wid_normalized = f"{int(wid_clean, 16):08x}"
#             key = f"0x{wid_normalized}"
#             if key in window_map:
#                 ordered_apps.append(window_map[key])
#             elif debug:
#                 print(f"[WARN] No match for {key}")

#         return ordered_apps

#     except Exception as e:
#         print(f"[ERROR] {e}")
#         return []
    



# # keyboard = Controller()

# def type_in_writer(text: str, delay: float = 0.05):
#     """
#     Types the given text into the currently active window (e.g., LibreOffice Writer).

#     Args:
#         text (str): Text to be typed.
#         delay (float): Delay between keystrokes.
#     """
#     print("type in writer working rn")
#     time.sleep(2)  # Give time to focus the right window
#     for char in text:
#         keyboard.type(char)
#         time.sleep(delay)

#     keyboard.press(Key.enter)
#     keyboard.release(Key.enter)