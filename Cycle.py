import argparse
import uuid
import json
import add_to_known_objects
from pymongo import MongoClient
import sys
import os

# Globals
inventoryJsonString = ""
outputFilePath = ""
defaultPort = 27017
address = "localhost"
ObjectArray = []
items = ""
verbose = False
knownItems = []

# Helper class
def safe_split(s, delimiter=":", index=1, default=None):
    try:
        return s.split(delimiter)[index].strip()
    except IndexError:
        return default

class CycleObject:
    def __init__(self, ItemId=None, BaseItemId=None, PrimaryVanityId=0, SecondaryVanityId=0, Amount=1, Durability=-1,
                 ModData=None, RolledPerks=None, Insurance="", InsuranceOwnerPlayfabId="", InsuredAttachmentId="",
                 Origin=None):
        self.ItemID = ItemId or str(uuid.uuid4())
        self.BaseItemID = BaseItemId
        self.PrimaryVanityID = int(PrimaryVanityId)
        self.SecondaryVanityID = int(SecondaryVanityId)
        self.Amount = int(Amount)
        self.Durability = int(Durability)
        self.ModData = ModData if ModData is not None else {"m": []}
        self.RolledPerks = RolledPerks if RolledPerks is not None else []
        self.Insurance = Insurance
        self.InsuranceOwnerPlayfabID = InsuranceOwnerPlayfabId
        self.InsuredAttachmentID = InsuredAttachmentId
        self.Origin = Origin if Origin is not None else {"t": "", "p": "", "g": ""}

def parseItemString(itemString):
    if os.path.exists(itemString):
        with open(itemString, 'r') as f:
            itemString = f.read().strip()

    items = itemString.split("+")
    for item in items:
        item = item.strip()
        if not item:
            continue

        if ":" not in item:
            obj = CycleObject(BaseItemId=item)
        else:
            baseItemId = item.split(":")[0]
            obj = CycleObject(BaseItemId=baseItemId)
            lowered = item.lower()
            obj.ItemID = safe_split(lowered, "itemid:") or obj.ItemID
            obj.PrimaryVanityID = safe_split(lowered, "primaryvanityid:", default=0)
            obj.SecondaryVanityID = safe_split(lowered, "secondaryvanityid:", default=0)
            obj.Amount = safe_split(lowered, "amount:", default=1)
            obj.Durability = safe_split(lowered, "durability:", default=-1)
            obj.Insurance = safe_split(lowered, "insurance:", default="None")
            obj.InsuranceOwnerPlayfabID = safe_split(lowered, "insuranceownerplayfabid:", default="")
            obj.InsuredAttachmentID = safe_split(lowered, "insuredattachmentid:", default="")

        ObjectArray.append(obj)

        if verbose:
            print(json.dumps(obj.__dict__, indent=2))

def try_parse_inventory(raw):
    try:
        if raw.strip().lower() == "mongo":
            return fetch_inventory_from_mongo()
        elif os.path.exists(raw):
            with open(raw, 'r') as f:
                raw = f.read()
        parsed = json.loads(raw.strip())
        return parsed if isinstance(parsed, list) else [parsed]
    except Exception as e:
        print(f"[!] Failed to parse inventory JSON: {e}")
        return []

def fetch_inventory_from_mongo(uri="mongodb://localhost:27017", db="ProspectDb", collection="PlayFabUserData", key="Inventory", save_to_file=None):
    try:
        print(f"[DEBUG] Connecting to MongoDB at {uri}...")
        client = MongoClient(uri)
        col = client[db][collection]
        print(f"[DEBUG] Querying documents where 'Key' == '{key}' in '{db}.{collection}'...")
        doc = col.find_one({"Key": key})
        if not doc:
            print(f"[!] No document found with Key == '{key}'")
            return []

        raw_value = doc.get("Value")
        print(f"[DEBUG] Raw 'Value' field (first 100 chars): {str(raw_value)[:100]}")

        if isinstance(raw_value, str):
            parsed = json.loads(raw_value)
            print(f"[+] Parsed {len(parsed)} item(s) from 'Value'.")
            if save_to_file:
                with open(save_to_file, "w") as f:
                    f.write(raw_value.strip())
                    print(f"[+] Mongo inventory saved to '{save_to_file}'")
            return parsed
        elif isinstance(raw_value, list):
            print(f"[+] 'Value' is already a list with {len(raw_value)} item(s).")
            if save_to_file:
                with open(save_to_file, "w") as f:
                    f.write(json.dumps(raw_value))
                    print(f"[+] Mongo inventory saved to '{save_to_file}'")
            return raw_value
        else:
            print(f"[!] Unsupported 'Value' format: {type(raw_value)}")
            return []
    except Exception as e:
        print(f"[!] MongoDB error: {e}")
        return []

def convertCycleObjectToJson(obj):
    try:
        return {
            "itemId": obj.ItemID,
            "baseItemId": obj.BaseItemID,
            "primaryVanityId": int(obj.PrimaryVanityID),
            "secondaryVanityId": int(obj.SecondaryVanityID),
            "amount": int(obj.Amount),
            "durability": int(obj.Durability),
            "modData": obj.ModData,
            "rolledPerks": obj.RolledPerks,
            "insurance": obj.Insurance,
            "insuranceOwnerPlayfabId": obj.InsuranceOwnerPlayfabID,
            "insuredAttachmentId": obj.InsuredAttachmentID,
            "origin": obj.Origin
        }
    except Exception as e:
        print(f"[!] Error converting item to JSON: {e}")
        return None

def search_known_objects(term, known_file="known_objects.list"):
    if not os.path.exists(known_file):
        print(f"[!] Known objects file not found: {known_file}")
        return -1

    with open(known_file, "r") as f:
        try:
            known_objects = json.load(f)
            matches = [item for item in known_objects if term.lower() in item.lower()]
            if matches:
                print("[+] Matches:")
                for match in matches:
                    print(f" - {match}")
            else:
                print("[!] No matches found.")
                return -1
        except Exception as e:
            print(f"[!] Error reading known objects file: {e}")
            return -1

def main():
    global ObjectArray, items, knownItems

    # Load existing inventory
    if args.input:
        if args.input.strip().lower() == "mongo":
            inventory = fetch_inventory_from_mongo(
                uri=f"mongodb://{address}:{defaultPort}",
                db=args.db,
                collection=args.collection,
                key=args.record,
                save_to_file=args.mongo_save_file
            )
        elif os.path.exists(args.input):
            with open(args.input, 'r') as f:
                inventory = json.load(f)
        else:
            try:
                inventory = json.loads(args.input.strip())
            except Exception as e:
                print(f"[!] Failed to parse input: {e}")
                return
    else:
        inventory = []

    # Parse new items
    raw_items = args.items
    if raw_items and os.path.exists(raw_items):
        with open(raw_items, 'r') as f:
            raw_items = f.read().strip()

    if raw_items:
        parseItemString(raw_items)

    new_items = [convertCycleObjectToJson(obj) for obj in ObjectArray if convertCycleObjectToJson(obj)]

    if not args.no_check_item_id:
        for dic in new_items:
            if not any(dic["baseItemId"].lower() in known.lower() for known in knownItems):
                if search_known_objects(dic["baseItemId"]) != -1:
                    print("Perhaps you meant one of the above?")
                print("[!] Item id not in known list. Use --no-check-item-id to bypass this check.")
                return -1

    final_inventory = inventory + new_items
    final_json = json.dumps(final_inventory, indent=2)

    # Handle output
    if args.output:
        if args.output.strip().lower() == "mongo":
            try:
                client = MongoClient(f"mongodb://{address}:{defaultPort}")
                collection = client[args.db][args.collection]
                result = collection.update_one({"Key": args.record}, {"$set": {"Value": final_json}}, upsert=True)
                if result.modified_count:
                    print("[+] MongoDB inventory updated successfully.")
                else:
                    print("[!] No document was modified.")
            except Exception as e:
                print(f"[!] Failed to update MongoDB: {e}")
        else:
            with open(args.output, 'w') as f:
                f.write(final_json)
                print(f"[+] Inventory written to {args.output}")
    else:
        print("\nFinal Inventory JSON:")
        print(final_json if verbose else final_json.replace(" ", "").replace("\n", ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inventory Modifier")
    parser.add_argument("-i", "--inventory", help="Path to inventory JSON file")
    parser.add_argument("--items", help="Items to add, + separated (e.g., Light:amount=10+Helmet:durability=500 or just Light+Fabric)")
    parser.add_argument("--items-file", help="Path to file containing items to add")
    parser.add_argument("--output", help="Output file path. If not provided, prints to console")
    parser.add_argument("--input", help="Load inventory JSON from file")
    parser.add_argument("-a", "--address", help="Server address (e.g., localhost or 127.0.0.1:27017)")
    parser.add_argument("-p", "--port", type=int, help="MongoDB port. Default is 27017")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--mongo", action="store_true", help="Use MongoDB for inventory")
    parser.add_argument("--db", default="ProspectDb", help="MongoDB database name")
    parser.add_argument("--collection", default="PlayFabUserData", help="MongoDB collection name")
    parser.add_argument("--record", default="Inventory", help="Document key that holds inventory data")
    parser.add_argument("--mongo-save-file", help="File path to save raw inventory JSON from MongoDB")
    parser.add_argument("--search", help="Search known_objects.list for matching entries")
    parser.add_argument("--replace-mongo", action="store_true", help="Replace existing inventory in MongoDB with new one")
    parser.add_argument("--no-check-item-id", action="store_true", help="Disable verifying that a baseItemId is in the known list before adding it")
    parser.add_argument("--good-item-ids", help="Path to file that contains known valid baseItemIds")
    args = parser.parse_args()

    verbose = args.verbose

    if args.search:
        search_known_objects(args.search)

    if args.good_item_ids:
        if os.path.exists(args.good_item_ids):
            with open(args.good_item_ids, 'r') as f:
                knownItems = json.load(f)
        else:
            print(f"[!] Known item ID list file not found: {args.good_item_ids}")
            sys.exit(1)


    if args.items_file:
        if os.path.exists(args.items_file):
            with open(args.items_file, 'r') as f:
                items = f.read().strip()
        else:
            print(f"[!] Items file not found: {args.items_file}")
            sys.exit(1)
    elif args.items:
        items = args.items

    if args.output:
        outputFilePath = args.output

    if args.address:
        if ":" in args.address:
            address, port = args.address.split(":")
            defaultPort = int(port)
        else:
            address = args.address

    if args.port:
        defaultPort = args.port

    main()