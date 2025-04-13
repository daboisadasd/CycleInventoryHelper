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

```bash
python Cycle.py --items "Light:itemid:myId123:amount:50+Balls:durability:200" --output inventory.json
