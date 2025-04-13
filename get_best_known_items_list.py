import requests
import json

# Raw GitHub URL
RAW_URL = "https://raw.githubusercontent.com/daboisadasd/CycleInventoryHelper/main/known_objects.list"
OUTPUT_FILE = "known_objects.list"

def download_known_objects():
    try:
        print(f"[DEBUG] Downloading known objects list from: {RAW_URL}")
        response = requests.get(RAW_URL)
        response.raise_for_status()

        data = response.text.strip()
        parsed = json.loads(data)

        with open(OUTPUT_FILE, "w") as f:
            json.dump(parsed, f, indent=4)
            print(f"[+] Saved {len(parsed)} known objects to {OUTPUT_FILE}")
    except Exception as e:
        print(f"[!] Failed to download or save known objects: {e}")

if __name__ == "__main__":
    download_known_objects()
