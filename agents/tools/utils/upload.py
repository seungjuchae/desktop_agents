import requests

def upload_screenshot(agent_id, plan_id, step, stage, file_path, server_url, api_key):
    url = f"{server_url}/api/agents/{agent_id}/upload_screenshot?plan_id={plan_id}"
    headers = {"authorization": f"Bearer {api_key}"}
    files = {"screenshot": open(file_path, "rb")}
    data = {"step": step, "stage": stage}

    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        print(f"📤 Uploaded {stage}_step_{step}.png: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to upload screenshot: {e}")
