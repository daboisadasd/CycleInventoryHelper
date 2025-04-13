# 🛠️ Cycle Inventory Helper

A simple command-line utility for generating and modifying inventory item data in **The Cycle Frontier: Reborn**.

> ⚠️ **Early Beta Notice:**  
> This tool is in early beta. Expect bugs, missing features, and things that don’t work quite right yet. Feel free to contribute or report issues.

---

## 💡 What It Does

- Parses item strings into proper inventory JSON format.
- Supports adding new items with custom properties like durability, vanity IDs, mod data, etc.
- Outputs to either console or a specified file.
- Useful for testing, modding, and debugging inventory systems.

---

## 🚀 How to Use

### 📦 Installation

Clone or download the repo and just run the script with Python 3.x:
> ⚠️ **Early Beta Notice:**  
> The tool requires that when adding an item, it has at least one field. So "Light" wont work but "Light:durability:-1" will
```bash
python Cycle.py --items "Light:itemid:myId123:amount:50+Helmet:durability:200" --output inventory.json
```
The script can add items to your inventory too!
```bash
python Cycle.py -i [{"itemId":"51c6d9d2-1bb5-4a9f-9d2b-1de0897732ee","baseItemId":"Light","primaryVanityId":0,"secondaryVanityId":0,"amount":234,"durability":-1,"modData":{"m":[]},"rolledPerks":[],"insurance":"","insuranceOwnerPlayfabId":"","insuredAttachmentId":"","origin":{"t":"","p":"","g":""}}] --items "Light:durability:-1"

python Cycle.py --input out.json --items "Helmet:amount:2+Light:durability:5"
Loading inventory from out.json

Final Inventory JSON:
[{"itemId": "0b4c27e4-8340-4a5c-96b1-79d7f857bf6e", "baseItemId": "light", "primaryVanityId": 0, "secondaryVanityId": 0, "amount": 1, "durability": 8, "modData": {"m": []}, "rolledPerks": [], "insurance": "None", "insuranceOwnerPlayfabId": "", "insuredAttachmentId": "", "origin": {"t": "", "p": "", "g": ""}}, {"itemId": "834d12c0-495d-469f-916a-254dcf0e1d6c", "baseItemId": "helmet", "primaryVanityId": 0, "secondaryVanityId": 0, "amount": 2, "durability": -1, "modData": {"m": []}, "rolledPerks": [], "insurance": "None", "insuranceOwnerPlayfabId": "", "insuredAttachmentId": "", "origin": {"t": "", "p": "", "g": ""}}, {"itemId": "4a144d6b-cab1-43a9-a3cf-e83861dc51a2", "baseItemId": "helmet", "primaryVanityId": 0, "secondaryVanityId": 0, "amount": 2, "durability": -1, "modData": {"m": []}, "rolledPerks": [], "insurance": "None", "insuranceOwnerPlayfabId": "", "insuredAttachmentId": "", "origin": {"t": "", "p": "", "g": ""}}, {"itemId": "a5af5dfa-292f-44a4-9f90-9a8a4beefbc5", "baseItemId": "light", "primaryVanityId": 0, "secondaryVanityId": 0, "amount": 1, "durability": 5, "modData": {"m": []}, "rolledPerks": [], "insurance": "None", "insuranceOwnerPlayfabId": "", "insuredAttachmentId": "", "origin": {"t": "", "p": "", "g": ""}}]

