import json

storage = {}

with open("entity_list.json") as file:
    file = json.load(file)

for category in file:
    print(category)

    #for thing in file[item]:
    #    print(thing)
    #    for char in file[item][thing]:
    #        print(char)
