import json

with open("test_data/login_data.json", "r") as file:
    test_data = json.load(file)

for test in test_data:
    print(test["id"])
    print(test["username"])
    print(test["password"])
    print("----------------")