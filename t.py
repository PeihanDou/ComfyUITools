import requests, json, uuid

with open("ComfyUI/user/default/workflows/sdxl_work_api.json", "r", encoding="utf-8") as f:
    workflow = json.load(f)

payload = {"prompt": workflow, "client_id": str(uuid.uuid4())}
resp = requests.post("http://127.0.0.1:8188/prompt", json=payload)
print(resp.status_code)
print(resp.text)