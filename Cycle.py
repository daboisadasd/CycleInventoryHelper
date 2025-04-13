"""{
    "itemId": "51c6d9d2-1bb5-4a9f-9d2b-1de0897732ee",
    "baseItemId": "Light",
    "primaryVanityId": 0,
    "secondaryVanityId": 0,
    "amount": 234,
    "durability": -1,
    "modData": {
      "m": []
    },
    "rolledPerks": [],
    "insurance": "",
    "insuranceOwnerPlayfabId": "",
    "insuredAttachmentId": "",
    "origin": {
      "t": "",
      "p": "",
      "g": ""
    }
  },{"itemId": "834d12c0-495d-469f-916a-254dcf0e1d6c", "baseItemId": "helmet", "primaryVanityId": 0, "secondaryVanityId": 0, "amount": 2, "durability": -1, "modData": {"m": []}, "rolledPerks": [], "insurance": "None", "insuranceOwnerPlayfabId": "", "insuredAttachmentId": "", "origin": {"t": "", "p": "", "g": ""}}
"""
import argparse
import uuid
import json
import ast
inventoryJsonString = ""
outputFilePath = ""
defaultPort = 27017
address = "localhost"
ObjectArray = []
items = ""
verbose = False
def parseItemId(item, itemObject):
    ItemID = None
    if item.find("itemid") != -1:
        index = item.find("itemid:")
        customUuid = item[index:].split(":")
        ItemID = customUuid[1]
        itemObject.ItemID = ItemID
    else:
        itemObject.ItemID = str(uuid.uuid4())
def parseItemBaseId(item, itemObject):
    itemObject.BaseItemID = item
    #todo check if item is a valid base item id
def parseVanityId(item, itemObject):
    if item.find("primaryvanityid") != -1:
        index = item.find("primaryvanityid:")
        vanityId = item[index:].split(":")
        ItemID = vanityId[1]
        itemObject.PrimaryVanityID = ItemID
    else:
        itemObject.PrimaryVanityID = 0
def parseSecondaryVanityId(item, itemObject):
    if item.find("secondaryvanityid") != -1:
        index = item.find("secondaryvanityid:")
        vanityId = item[index:].split(":")
        ItemID = vanityId[1]
        itemObject.SecondaryVanityID = int(ItemID)
    else:
        itemObject.SecondaryVanityID = 0
def parseAmount(item, itemObject):
    if item.find("amount") != -1:
        index = item.find("amount:")
        amount = item[index:].split(":")
        ItemID = amount[1]
        itemObject.Amount = ItemID
    else:
        itemObject.Amount = 1
def parseDurability(item, itemObject):
    if item.find("durability") != -1:
        index = item.find("durability:")
        durability = item[index:].split(":")
        ItemID = durability[1]
        itemObject.Durability = ItemID
    else:
        itemObject.Durability = -1
def parseModData(item, itemObject):
    if item.find("moddatA") != -1:               #todo add moddata parsing
        index = item.find("moddata:")
        modData = item[index:].split(":")
        ItemID = modData[1]
        itemObject.ModData = ItemID
    else:
        itemObject.ModData = {"m": []}
def parseRolledPerks(item, itemObject):
    if item.find("rolledperks") != -1:
        index = item.find("rolledperks:")
        rolledPerks = item[index:].split(":")
        ItemID = rolledPerks[1]
        itemObject.RolledPerks = ItemID
    else:
        itemObject.RolledPerks = []
def parseInsurance(item, itemObject):
    if item.find("insurance") != -1:
        index = item.find("insurance:")
        insurance = item[index:].split(":")
        ItemID = insurance[1]
        itemObject.Insurance = ItemID
    else:
        itemObject.Insurance = "None"
def parseInsuranceOwnerPlayfabId(item, itemObject):
    if item.find("insuranceownerplayfabid") != -1:
        index = item.find("insuranceownerplayfabid:")
        insuranceOwnerPlayfabId = item[index:].split(":")
        ItemID = insuranceOwnerPlayfabId[1]
        itemObject.InsuranceOwnerPlayfabID = ItemID
    else:
        itemObject.InsuranceOwnerPlayfabID = ""
def parseInsuredAttachmentId(item, itemObject):
    if item.find("insuredattachmentid") != -1:
        index = item.find("insuredattachmentid:")
        insuredAttachmentId = item[index:].split(":")
        ItemID = insuredAttachmentId[1]
        itemObject.InsuredAttachmentID = ItemID
    else:
        itemObject.InsuredAttachmentID = ""
def parseOrigin(item, itemObject):                                  
    if item.find("origin") != -1:
        index = item.find("origin:")
        origin = item[index:].split(":")
        ItemID = origin[1]
        itemObject.Origin = ItemID
    else:
        itemObject.Origin = {"t": "", "p": "", "g": ""}
class CycleObject: 
    def __init__(self, ItemId=None, BaseItemId=None, PrimaryVanityId=0, SecondaryVanityId=0, Amount=1, Durability=-1, ModData=None, RolledPerks=None, Insurance="", InsuranceOwnerPlayfabId="", InsuredAttachmentId="", Origin=None):
        self.ItemID = ItemId
        self.BaseItemID = BaseItemId
        self.PrimaryVanityID = PrimaryVanityId
        self.SecondaryVanityID = SecondaryVanityId
        self.Amount = Amount
        self.Durability = Durability
        self.ModData = ModData if ModData is not None else {"m": []}
        self.RolledPerks = RolledPerks if RolledPerks is not None else []
        self.Insurance = Insurance
        self.InsuranceOwnerPlayfabID = InsuranceOwnerPlayfabId
        self.InsuredAttachmentID = InsuredAttachmentId
        self.Origin = Origin if Origin is not None else {"t": "", "p": "", "g": ""}
    def convertmodtoCycleString(self):
        return "{" + str(self.ModData) + "}"
    def convertRolledPerkstoCycleString(self):
        print("RolledPerks:")
        
def parseItemString(itemString):
    try:
        items = itemString.split("+")
        for item in items:
            item = item.strip()
            itemObject = CycleObject()
            item = item.lower()
            if item == "":
                continue
            if item.find(":") == -1:
                print(f"Invalid item string '{item}'")
                continue
            baseItemId = item.split(":")[0]
            parseItemId(item, itemObject)
            parseItemBaseId(baseItemId, itemObject)
            parseVanityId(item, itemObject)
            parseSecondaryVanityId(item, itemObject)
            parseAmount(item, itemObject)
            parseDurability(item, itemObject)
            parseModData(item, itemObject) #I dont have an item with moddata so I don't know what it does. If you know how the moddata field works / affects an item, message me on discord and I will add it to the code. my username is x_ref#0
            parseRolledPerks(item, itemObject) #I dont have an item with rolled perks so I don't know what it does. If you know how the rolled perks field works / affects an item, message me on discord and I will add it to the code. my username is x_ref#0
            parseInsurance(item, itemObject) 
            parseInsuranceOwnerPlayfabId(item, itemObject) #
            parseInsuredAttachmentId(item, itemObject) 
            parseOrigin(item, itemObject) #todo add origin parsing
            ObjectArray.append(itemObject)
            if(verbose):
                print(f"ItemID: {itemObject.ItemID}")
                print(f"BaseItemID: {itemObject.BaseItemID}")
                print(f"PrimaryVanityID: {itemObject.PrimaryVanityID}")
                print(f"SecondaryVanityID: {itemObject.SecondaryVanityID}")
                print(f"Amount: {itemObject.Amount}")
                print(f"Durability: {itemObject.Durability}")
                print(f"ModData: {itemObject.ModData}")             #todo add moddata parsing
                print(f"RolledPerks: {itemObject.RolledPerks}")     #todo add rolled perks parsing
                print(f"Insurance: {itemObject.Insurance}")
                print(f"InsuranceOwnerPlayfabID: {itemObject.InsuranceOwnerPlayfabID}")
                print(f"InsuredAttachmentID: {itemObject.InsuredAttachmentID}")
                print(f"Origin: {itemObject.Origin}")
    except (IndexError, ValueError) as e:
        print(f"Error parsing item string '{itemString}': {e}")
        return None, None, None
def try_parse_inventory(raw: str):
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
        elif isinstance(parsed, dict):
            return [parsed]
        else:
            return []
    except Exception as e:
        print(f"[!] Failed to parse inventory: {e}")
        return []


def convertCycleObjectToJson(itemObject):
    try:
        return {
            "itemId": itemObject.ItemID,
            "baseItemId": itemObject.BaseItemID,
            "primaryVanityId": int(itemObject.PrimaryVanityID),
            "secondaryVanityId": int(itemObject.SecondaryVanityID),
            "amount": int(itemObject.Amount),
            "durability": int(itemObject.Durability),
            "modData": {"m": []},
            "rolledPerks": [],
            "insurance": itemObject.Insurance,
            "insuranceOwnerPlayfabId": itemObject.InsuranceOwnerPlayfabID,
            "insuredAttachmentId": itemObject.InsuredAttachmentID,
            "origin": {"t": "", "p": "", "g": ""}
        }
    except Exception as e:
        print(f"[!] Error in convertCycleObjectToJson: {e}")
        return None

def main():
    global inventoryJsonString, ObjectArray

    # Load existing inventory JSON (from file or direct input)
    existing_inventory = []
    if inventoryJsonString.strip():
        existing_inventory = try_parse_inventory(inventoryJsonString.strip())
        if not isinstance(existing_inventory, list):
            print("[!] Warning: existing inventory input is not a list. Skipping merge.")
            existing_inventory = []

    # Parse new items from --items string
    parseItemString(items)

    # Convert new CycleObjects to JSON-ready dicts
    new_items = []
    for obj in ObjectArray:
        item_dict = convertCycleObjectToJson(obj)
        if item_dict:
            new_items.append(item_dict)

    # Merge inventories
    final_inventory = existing_inventory + new_items

    # Output merged JSON
    final_json = json.dumps(final_inventory)

    if outputFilePath:
        with open(outputFilePath, 'w') as f:
            f.write(final_json)
            print(f"Inventory JSON written to {outputFilePath}")
    else:
        print("\nFinal Inventory JSON:")
        print(final_json)



def sconvertCycleObjectToJson(itemObject):
    
    try:
        #Still need to add rolled perks and moddata parsing
        itemObject.ModData = "{\"m\": []}"
        itemObject.RolledPerks = "[]"
        itemObject.Origin = "{\"t\": \"\", \"p\": \"\", \"g\": \"\"}"
        itemJson = "{\"itemId\": \""+ itemObject.ItemID+"\"," + \
            "\"baseItemId\": \""+  str(itemObject.BaseItemID)+"," + \
            "\"primaryVanityId\":" + str(itemObject.PrimaryVanityID)+"," + \
            "\"secondaryVanityId\":" +str(itemObject.SecondaryVanityID)+"," + \
            "\"amount\":" + str(itemObject.Amount)+"," + \
            "\"durability\":" + str(itemObject.Durability)+"," + \
            "\"modData\":" + itemObject.ModData+"\"," + \
            "\"rolledPerks\":"+  itemObject.RolledPerks+"\"," + \
            "\"insurance\":" + itemObject.Insurance+"\"," + \
            "\"insuranceOwnerPlayfabId\":" + itemObject.InsuranceOwnerPlayfabID+"\"," + \
            "\"insuredAttachmentId\":" + itemObject.InsuredAttachmentID+"\"," + \
            "\"origin\":" + itemObject.Origin+"\"}"
        print(f"Item JSON: {itemJson}")
        return itemJson
    except Exception as e:
        print(f"Error converting CycleObject to JSON: {e}")
        return None
def smain():
    global inventoryJsonString, ObjectArray
    parseItemString(items)
    for x in ObjectArray:
        itemJson = convertCycleObjectToJson(x)
        if inventoryJsonString == "":
            inventoryJsonString = "[" + itemJson + "]"
        else:
            inventoryJsonString = inventoryJsonString[:-1] + "," + itemJson + "]"
    if(outputFilePath != ""):
        with open(outputFilePath, 'w') as f:
            f.write(inventoryJsonString)
            print(f"Inventory JSON written to {outputFilePath}")
    else:
        print("\nFinal Inventory JSON:")
        print(inventoryJsonString)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inventory modifier")
    parser.add_argument("-i", "--inventory", help="Inventory JSON string with [] brackets")
    parser.add_argument("--items", help="Items to add, + separated, = instead of : (e.g., Light:amount:10+Helmet:durability=500)")
    parser.add_argument("--output", help="Output file path. If not provided, prints to console")
    parser.add_argument("--input", help="Load inventory JSON from file")
    parser.add_argument("-a", "--address", help="Optional server address (e.g., 127.0.0.1 or localhost:6680)")
    parser.add_argument("-p", "--port", type=int, help="Port of the server to connect to. Default is 27017")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Global values
    verbose = False
    inventoryJsonString = ""
    outputFilePath = ""
    defaultPort = 27017
    address = "localhost"
    items = ""

    # Handle args
    if args.input:
        with open(args.input, 'r') as f:
            print(f"Loading inventory from {args.input}")   
            inventoryJsonString = f.read()
    elif args.inventory:
        inventoryJsonString = args.inventory

    if args.items:
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

    if args.verbose:
        verbose = True

    main()

