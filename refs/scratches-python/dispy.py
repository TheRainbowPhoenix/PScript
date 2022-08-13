import json

with open("opname.json") as f:
    opname = json.load(f)

print(opname)