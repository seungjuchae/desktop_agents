import time
from keyboard import search_and_launch, alt_tab
from pynput.keyboard import Key, Controller

keyboard = Controller()

# Step 1: Launch Chrome via GNOME search
search_and_launch("chrome")
time.sleep(2)  # Give Chrome time to launch

# Step 2: Ctrl+N to open a new window
keyboard.press(Key.ctrl)
keyboard.press('n')
keyboard.release('n')
keyboard.release(Key.ctrl)
time.sleep(1)

# Step 3: Type "hello"
keyboard.type("hello")
time.sleep(1)

# Step 4: Launch LibreOffice Calc
search_and_launch("libreoffice calc")
time.sleep(3)  # Let it load

# Step 5: Alt+Tab to second most recent window
alt_tab(2)





# from screeninfo import get_monitors
# import subprocess

# def get_system_input_info():
#     # Get screen width and height
#     monitor = get_monitors()[0]
#     width = monitor.width
#     height = monitor.height

#     # Get current layout (fallback using setxkbmap)
#     try:
#         layout_info = subprocess.check_output(['setxkbmap', '-query']).decode()
#         current_layout = "unknown"
#         for line in layout_info.splitlines():
#             if line.startswith("layout:"):
#                 current_layout = line.split(":")[1].strip()
#                 break
#     except Exception:
#         current_layout = "unknown"

#     # No easy way to get list of layouts without xkb-switch or dbus
#     available_layouts = [current_layout] if current_layout != "unknown" else []

#     return {
#         "screen_size": [width, height],
#         "current_layout": current_layout,
#         "available_layouts": available_layouts
#     }

# print(get_system_input_info())











# import time
# from tools import keyboard
# from tools.keyboard import type_in_writer
# from tools.mouse import left_click
# from actions.performer import perform_mouse_action, perform_keyboard_action

# def launch_excel():
#     print("🟢 Launching LibreOffice Calc...")
#     keyboard.search_and_launch("libreoffice calc")


# def launch_word():
#     from actions.performer import perform_mouse_action, perform_keyboard_action
#     print("🟢 Launching LibreOffice word...")

#     from tools import keyboard
#     keyboard.search_and_launch("libreoffice writer")

#     print("⏳ Waiting for app to launch...")
#     time.sleep(4)

#     print("🎯 Moving and clicking...")
#     perform_mouse_action(470, 317, action_type="left_click", delay=0.5)

#     print("⌨️ Typing...")
#     perform_keyboard_action("type", "안녕하세요! This is a test message to check 한글 입력 기능. LibreOffice Writer에서 자동으로 작성된 문장입니다. Let's type more. Python으로 만든 에이전트는 really smart and responsive. 오늘 날씨가 좋네요. Let's open Excel and write some data..")   

