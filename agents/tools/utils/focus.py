# tools/utils/focus.py

import subprocess
import time

def wait_and_focus(app_name: str, timeout: int = 10, interval: float = 0.5) -> bool:
    """
    Waits for a window with `app_name` in its title or class to appear, then focuses it.
    Returns True if focused successfully, False otherwise.
    """
    print(f"🕒 Waiting to focus app: {app_name} (timeout: {timeout}s)")

    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            output = subprocess.check_output(["wmctrl", "-lx"]).decode()

            for line in output.splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    win_id = parts[0]
                    win_class = parts[2].lower()
                    win_title = " ".join(parts[4:]).lower()

                    if app_name.lower() in win_class or app_name.lower() in win_title:
                        subprocess.run(["wmctrl", "-i", "-a", win_id])
                        print(f"✅ Focused window for app: {app_name} ({win_id})")
                        return True

            time.sleep(interval)

        except Exception as e:
            print(f"⚠️ Focus error: {e}")
            time.sleep(interval)

    print(f"❌ Failed to focus app '{app_name}' within timeout.")
    return False
