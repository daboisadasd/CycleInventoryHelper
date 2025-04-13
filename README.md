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

Final Inventory JSON:
[{itemId:51c6d9d2-1bb5-4a9f-9d2b-1de0897732ee,baseItemId:Light,primaryVanityId:0,secondaryVanityId:0,amount:234,durability:-1,modData:{m:[]},rolledPerks:[],insurance:,insuranceOwnerPlayfabId:,insuredAttachmentId:,origin:{t:,p:,g:}},{"itemId": "c3a2606c-3c2f-4ceb-9b9d-8aa6b24bc9f0", "baseItemId": "light", "primaryVanityId": 0, "secondaryVanityId": 0, "amount": 1, "durability": "-1", "modData": {"m": []}, "rolledPerks": [], "insurance": "None", "insuranceOwnerPlayfabId": "", "insuredAttachmentId": "", "origin": {"t": "", "p": "", "g": ""}}]
