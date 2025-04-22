import time
from tools import keyboard
from keyboard_tool import type_in_writer
from mouse_tool import left_click
from actions.performer import perform_mouse_action, perform_keyboard_action

def launch_excel():
    print("🟢 Launching LibreOffice Calc...")
    keyboard.search_and_launch("libreoffice calc")


def launch_word():
    from actions.performer import perform_mouse_action, perform_keyboard_action
    print("🟢 Launching LibreOffice word...")

    from tools import keyboard
    keyboard.search_and_launch("libreoffice writer")

    print("⏳ Waiting for app to launch...")
    time.sleep(4)

    print("🎯 Moving and clicking...")
    perform_mouse_action(470, 317, action_type="left_click", delay=0.5)

    print("⌨️ Typing...")
    perform_keyboard_action("type", "안녕하세요! This is a test message to check 한글 입력 기능. LibreOffice Writer에서 자동으로 작성된 문장입니다. Let's type more. Python으로 만든 에이전트는 really smart and responsive. 오늘 날씨가 좋네요. Let's open Excel and write some data..")   

