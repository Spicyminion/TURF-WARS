import json

class DummyShop:
    def __init__(self):
        self.main_categories = []
        self.categories = {}
        with open("entity_list.json") as json_file:
            self.entities = json.load(json_file) # convert to dict
        self.initialize_shop()

    def initialize_shop(self):
        for main_category in self.entities:
           self.main_categories.append(main_category)

    def make_purchase(self, item, player):
        if item["cost"] <= player.money:
            print(f"item: {item} purchased")
            # ADD ITEM TO PLAYER INVENTORY (UNFINISHED)
            return True
        else:
            print("Not enough money!")
            return False

# categories is dynamically updated in shop renderer