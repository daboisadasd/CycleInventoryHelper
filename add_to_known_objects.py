import json
import argparse

def extract_base_item_ids(data):
    try:
        items = json.loads(data)
        base_ids = [item.get("baseItemId") for item in items if "baseItemId" in item]
        return base_ids
    except Exception as e:
        print(f"[!] Failed to parse JSON: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Extract baseItemId values from inventory JSON.")
    parser.add_argument("-f", "--file", help="Path to inventory JSON file", required=True)
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            data = f.read()
            base_ids = extract_base_item_ids(data)
            with open("known_objects.list", "w") as out_file:
                json.dump(base_ids, out_file, indent=4)
            print(f"[+] Extracted {len(base_ids)} baseItemId(s) to known_objects.json")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    print("[+] Starting extraction...")
    print("[+] This script will extract baseItemId values from the provided inventory JSON file.")
    print("[+] The extracted values will be saved to known_objects.json.")
    print("[+] Make sure to provide the correct path to the inventory JSON file.")
    print("[+] Example usage: python add_to_known_objects.py -f inventory.json")
    print("[+] You can straight copy and paste your inventory found in mongodb into a .json file.")
    main()
