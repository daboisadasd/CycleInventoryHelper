import json
import argparse
import os
from pymongo import MongoClient

def extract_base_item_ids(data):
    try:
        print(f"[DEBUG] Extracting baseItemId from {len(data)} item(s)...")
        return [item.get("baseItemId") for item in data if isinstance(item, dict) and "baseItemId" in item]
    except Exception as e:
        print(f"[!] Failed to extract baseItemId: {e}")
        return []

def load_known_objects(filename="known_objects.list"):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return set(json.load(f))
        except Exception as e:
            print(f"[!] Failed to load existing known objects: {e}")
    return set()

def fetch_inventory_from_mongo(uri, db_name, collection_name, inventory_key):
    try:
        print(f"[DEBUG] Connecting to MongoDB at {uri}...")
        client = MongoClient(uri)
        collection = client[db_name][collection_name]

        # Find the document where "Key" == "Inventory"
        print(f"[DEBUG] Querying documents where 'Key' == '{inventory_key}' in '{db_name}.{collection_name}'...")
        document = collection.find_one({"Key": inventory_key})
        if not document:
            print(f"[!] No document found where 'Key' == '{inventory_key}'.")
            return []

        # Extract and parse the "Value" field
        raw_value = document.get("Value")
        print(f"[DEBUG] Raw 'Value' field (first 100 chars): {str(raw_value)[:100]}")

        if isinstance(raw_value, str):
            try:
                parsed = json.loads(raw_value)
                if isinstance(parsed, list):
                    print(f"[+] Parsed {len(parsed)} item(s) from 'Value'.")
                    return parsed
                else:
                    print(f"[!] Parsed value is not a list. Type: {type(parsed)}")
                    return []
            except Exception as e:
                print(f"[!] Failed to parse 'Value' JSON: {e}")
                return []
        elif isinstance(raw_value, list):
            print(f"[+] 'Value' is already a list with {len(raw_value)} item(s).")
            return raw_value
        else:
            print(f"[!] Unsupported 'Value' format: {type(raw_value)}")
            return []

    except Exception as e:
        print(f"[!] MongoDB error: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Extract baseItemId values from inventory JSON or MongoDB.")
    parser.add_argument("-f", "--file", help="Path to inventory JSON file")
    parser.add_argument("-c", "--connect", help="Use MongoDB instead of file", action="store_true")
    parser.add_argument("--mongo", help="MongoDB connection URI", default="mongodb://localhost:27017")
    parser.add_argument("--db", help="MongoDB database name", default="ProspectDb")
    parser.add_argument("--collection", help="MongoDB collection name", default="PlayFabUserData")
    parser.add_argument("--record", help="Document key that holds inventory data", default="Inventory")
    args = parser.parse_args()

    inventory_data = []

    if args.connect and args.file:
        print("[!] You cannot use both --file and --connect at the same time.")
        return

    if args.connect:
        inventory_data = fetch_inventory_from_mongo(args.mongo, args.db, args.collection, args.record)
    elif args.file:
        if os.path.exists(args.file):
            with open(args.file, "r") as f:
                inventory_data = json.load(f)
        else:
            print(f"[!] File not found: {args.file}")
            return
    else:
        print("[!] You must provide either --file or --connect.")
        return

    new_base_ids = extract_base_item_ids(inventory_data)
    known_base_ids = load_known_objects()
    initial_count = len(known_base_ids)

    known_base_ids.update(new_base_ids)
    final_count = len(known_base_ids)

    with open("known_objects.list", "w") as out_file:
        json.dump(sorted(known_base_ids), out_file, indent=4)

    print(f"[+] Added {final_count - initial_count} new baseItemId(s) to known_objects.list")
    print(f"[+] Total unique baseItemId(s): {final_count}")

if __name__ == "__main__":
    print("[+] Starting extraction from JSON or MongoDB inventory...")
    main()
