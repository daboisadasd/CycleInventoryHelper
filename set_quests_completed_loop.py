import time
import json
from pymongo import MongoClient

DB_URI = "mongodb://localhost:27017"
DB_NAME = "ProspectDb"
COLLECTION_NAME = "PlayFabUserData"
KEY_NAME = "ContractsActive"
UPDATE_INTERVAL_SECONDS = 5

client = MongoClient(DB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print(f"[+] Monitoring and updating '{KEY_NAME}' every {UPDATE_INTERVAL_SECONDS} seconds...")

while True:
    try:
        doc = collection.find_one({"Key": KEY_NAME})
        if not doc:
            print("[!] Document with key 'ContractsActive' not found.")
        else:
            value = doc.get("Value")
            if isinstance(value, str):
                value = json.loads(value)

            updated = False
            if "contracts" in value:
                for contract in value["contracts"]:
                    if "progress" in contract:
                        contract["progress"] = [20] * len(contract["progress"])
                        updated = True

            if updated:
                result = collection.update_one(
                    {"Key": KEY_NAME},
                    {"$set": {"Value": json.dumps(value)}}
                )
                print(f"[+] Updated contract progress at {time.strftime('%X')}.")
            else:
                print("[i] No progress fields found to update.")

    except Exception as e:
        print(f"[!] Error during update: {e}")

    time.sleep(UPDATE_INTERVAL_SECONDS)
