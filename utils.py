import json
import os
import hashlib
import time

# JSON helpers
def read_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def write_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Patient data logic
def add_patient(patient_id, name, age, gender):
    patients = read_json("patients.json")
    for p in patients:
        if p["id"] == patient_id:
            return False
    patients.append({
        "id": patient_id,
        "name": name,
        "age": age,
        "gender": gender
    })
    write_json("patients.json", patients)
    return True

def get_all_patients():
    return read_json("patients.json")

# Blockchain logic
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode()).hexdigest()

def get_chain():
    return read_json("chain.json")

def add_block(data):
    chain = get_chain()
    if len(chain) == 0:
        previous_hash = "0"
        index = 0
    else:
        previous_hash = chain[-1]["hash"]
        index = len(chain)

    block = Block(index, data, previous_hash)
    chain.append(block.__dict__)
    write_json("chain.json", chain)
