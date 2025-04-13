# 🛠️ Cycle Inventory Helper

A command-line tool to create, merge, and manage inventory JSON data for **The Cycle Frontier: Reborn**.

> ⚠️ **Early Beta Notice:**  
> This tool is in active development. Expect missing features, bugs, and breaking behavior. Feedback and contributions are welcome!

---

## 💡 Features

- ✅ Convert simple item strings like `Light:durability:8` into full item JSON objects.
- ✅ Merge new items into an existing inventory (`--input` or `--inventory`).
- ✅ Outputs clean, formatted JSON to a file or directly to the console.
- ✅ Supports custom fields:
  - `itemid`, `amount`, `durability`, `vanityId`, `modData`, `insurance`, etc.
- ✅ Auto-generates UUIDs for `itemId` when not provided.

---

## 🚀 Usage

### 🔧 Basic Item Generation

```
python Cycle.py --items "Light:itemid:myId123:amount:50+Helmet:durability:200" --output inventory.json
```

> ⚠️ You must provide **at least one field** with each item.  
> `Light` alone will not work — use something like `Light:durability:-1`.

---

### 🔁 Merging with Existing Inventory

You can merge new items into a previously saved inventory.

#### 🔹 From a direct JSON string:
```
python Cycle.py --inventory '[{"itemId":"...","baseItemId":"Light",...}]' --items "Light:durability:-1"
```

#### 🔹 From a JSON file:
```
python Cycle.py --input out.json --items "Helmet:amount:2+Light:durability:5"
```

Example output:
```
Loading inventory from out.json

Final Inventory JSON:
[
    {
        "itemId": "0b4c27e4-...",
        "baseItemId": "light",
        ...
    },
    {
        "itemId": "834d12c0-...",
        "baseItemId": "helmet",
        ...
    }
]
```

---

## 📄 Input Format for `--items`

You can chain multiple items with `+`, and each property with `:`:

```
"Light:amount:3:durability:-1+Helmet:amount:1"
```

Each entry will become a full JSON object with the default structure auto-filled where needed.

---

## 🧪 Dev Notes

- Written in Python 3.8+
- I have a very barebones list of known items right now, you can use the custom unique base finder script to find new ones!
- No external libraries required
- Designed for testing and modifying inventories in Cycle Frontier Reborn

---

## 🧑‍💻 Contributing

PRs welcome!  
If you want to help with `modData` or `rolledPerks` support, message me on Discord: `x_ref#0`
