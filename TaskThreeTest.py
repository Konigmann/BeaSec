from fastapi import FastAPI, HTTPException
from typing import Dict
import json
import os

app = FastAPI()
DB_FILE = "db.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
def read_all():
    return load_data()

@app.get("/{port}")
def read_entry(port: str):
    data = load_data()
    for entry in data:
        if port in entry:
            return {port: entry[port]}
    raise HTTPException(status_code=404, detail="Port not found")

@app.post("/")
def create_entry(entry: Dict[str, str]):
    data = load_data()
    for k in entry:
        if any(k in e for e in data):
            raise HTTPException(status_code=400, detail="Port already exists")
        data.append(entry)
    save_data(data)
    return {"message": "Entry added", "data": entry}

@app.put("/{port}")
@app.patch("/{port}")
def update_entry(port: str, updated: Dict[str, str]):
    data = load_data()
    for i, entry in enumerate(data):
        if port in entry:
            entry[port] = updated.get(port, entry[port])
            data[i] = entry
            save_data(data)
            return {"message": "Entry updated", "data": entry}
    raise HTTPException(status_code=404, detail="Port not found")

@app.delete("/{port}")
def delete_entry(port: str):
    data = load_data()
    new_data = [entry for entry in data if port not in entry]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Port not found")
    save_data(new_data)
    return {"message": "Entry deleted"}