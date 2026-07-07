from client_ui import Button
import pygame_gui
from client_character import Character, Bob, Joe, Xub

class DummyShop:
    def __init__(self):
        self.categories = {
            "tier_1_characters": {
                "Character": {"item": Character, "count": 2},
                "Bob": {"item": Bob, "count": 1},
                "Joe": {"item": Joe, "count": 1}
            },

            "tier_2_characters": {
                "Xub": {"item": Xub, "count": 1},
                "Bob": {"item": Bob, "count": 1}
            },
            "tier_3_characters": {},
            "tier_4_characters": {},
            "regular_weapons": {},
            "special_weapons": {}
        }


    def make_purchase(self, item, player):
        if item["cost"] <= player.money:
            player.money -= item["cost"]
            purchased_item = None # ADD LATER
            print("item \"purchased\"")
            # ADD ITEM TO PLAYER INVENTORY (UNFINISHED)
            return True
        else:
            print("Not enough money!")
            return False