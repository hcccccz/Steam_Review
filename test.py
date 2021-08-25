import json
with open("time.json","r+") as file:
    f = json.loads(file.read())

    print(f)
