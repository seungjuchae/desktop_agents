# coordinator/collect_desktop_metadata.py

import os
import platform
import json
import time
import psutil
import shutil
import pyautogui
from screeninfo import get_monitors
from datetime import datetime

def check_browser_installed(browser_names):
    found = []
    for name in browser_names:
        if shutil.which(name):
            found.append(name)
    return found

def get_screen_resolution():
    try:
        monitor = get_monitors()[0]
        return {"width": monitor.width, "height": monitor.height}
    except:
        return {"width": 0, "height": 0}

def get_running_apps():
    apps = set()
    for proc in psutil.process_iter(attrs=["name"]):
        try:
            apps.add(proc.info["name"])
        except:
            continue
    return sorted(list(apps))

def collect_metadata():
    metadata = {
        "os": platform.system(),
        "platform_version": platform.version(),
        "screen_resolution": get_screen_resolution(),
        "running_apps": get_running_apps(),
        "available_browsers": check_browser_installed([
            "google-chrome", "chrome", "firefox", "microsoft-edge", "safari", "brave-browser"
        ]),
        "collected_at": datetime.utcnow().isoformat() + "Z"
    }

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("✅ metadata.json saved")

    screenshot_path = "desktop_home.png"
    pyautogui.screenshot(screenshot_path)
    print(f"🖼️ Screenshot saved to {screenshot_path}")

    return metadata, screenshot_path

if __name__ == "__main__":
    collect_metadata()
