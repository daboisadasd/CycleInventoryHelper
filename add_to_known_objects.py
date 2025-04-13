import json
import argparse
import os

def extract_base_item_ids(data):
    try:
        items = json.loads(data)
        return [item.get("baseItemId") for item in items if "baseItemId" in item]
    except Exception as e:
        print(f"[!] Failed to parse JSON: {e}")
        return []

def load_known_objects(filename="known_objects.list"):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return set(json.load(f))
        except Exception as e:
            print(f"[!] Failed to load existing known objects: {e}")
    return set()

def main():
    parser = argparse.ArgumentParser(description="Extract baseItemId values from inventory JSON.")
    parser.add_argument("-f", "--file", help="Path to inventory JSON file", required=True)
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            data = f.read()
            new_base_ids = extract_base_item_ids(data)

            known_base_ids = load_known_objects()
            initial_count = len(known_base_ids)

            known_base_ids.update(new_base_ids)
            final_count = len(known_base_ids)

            with open("known_objects.list", "w") as out_file:
                json.dump(sorted(known_base_ids), out_file, indent=4)

            print(f"[+] Added {final_count - initial_count} new baseItemId(s) to known_objects.list")
            print(f"[+] Total unique baseItemId(s): {final_count}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    print("[+] Starting extraction...")
    print("[+] This script will extract baseItemId values from the provided inventory JSON file.")
    print("[+] The extracted values will be added to known_objects.list (no duplicates).")
    print("[+] Example usage: python add_to_known_objects.py -f inventory.json")
    print("[+] You can paste your inventory JSON exported from MongoDB into a file and use that.")
    main()
