import pygame
import pygame_gui
import math
import json

class ShopRenderer:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.config = game.config
        self.ui_manager = game.ui_manager
        self.shop = game.shop

        self.images = {}
        for name, img in self.config.assets.imgs.items():
            self.images[name] = img

        self.rows = 3
        self.cols = 4
        self.frame_height = None
        self.frame_width = None

        self.item_buttons = {}  # if any of these are triggered, send output back to ShopState
        self.shop_menu_buttons = {}
        self.shop_page_buttons = {}
        self.other_buttons = [self.shop_menu_buttons, self.shop_page_buttons] # if any of these are triggered, renderer internally handles command
        self.main_categories = game.shop.main_categories
        self.shop_page = 1
        self.active_category = None
        self.current_depth = 0
        self._init()

    def _init(self):

        self.frame_height = self.images["test_char_frame"].get_height()
        self.frame_width = self.images["test_char_frame"].get_width()

        self.start_x = (self.config.screen_width / 2) - (self.frame_width * (self.cols / 2))
        self.start_y = (self.config.screen_height / 2) - (self.frame_height * (self.rows / 2))


    def load_shop(self):
        print("hi")
        pass

    def open_shop_page(self):
        category_list = list(self.shop.entities.keys()) # ex. tier_1_chars, special_weapons, etc.
        num_categories = len(category_list)
        size = 100 # need to make this dynamically adjustable in future
        starting_x = (self.config.screen_width / 2) - (num_categories / 2 * size)
        starting_y = self.config.screen_height - size # start almost at bottom
        for index in range(num_categories):
            button_x = starting_x + (size * index)
            button_y = starting_y
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, button_y), (size, size)), # need to change this be dynamic
                text=f'{category_list[index]}',
                manager=self.ui_manager,
            )
            self.shop_menu_buttons[button] = lambda cat=category_list[index]: self.change_category(cat) # we will then call in the main dictionary
        #self.generate_items()

    def go_back(self):
        pass
        # go back to main screen

    def change_category(self, category_name):
        # need to add if/else statement depending if we already have an active category
        self.active_category = category_name
        self.shop_page = 1
        self.generate_items()

    def change_page(self, page):
        self.shop_page = page
        self.generate_items()

    def handle_button_pressed(self, event):
        # CHECK IF WE'RE CHANGING ITEMS DISPLAYED
        for button_group in self.other_buttons:
            button_clicked = button_group.get(event.ui_element)
            if button_clicked:
                break
        if button_clicked:
            button_clicked()  # Need to implement this with lambda
            return None

        # CHECK IF WE'RE SELECTING AN ITEM TO PURCHASE
        item_clicked = self.item_buttons.get(event.ui_element)
        if item_clicked:
            print(f"Attempting to purchase: {item_clicked}")
            print(f"item: info: {self.shop.categories[self.active_category][item_clicked]}")
            return item_clicked
        return None

    def generate_items(self):
        print("GENERATE ITEMS")
        # CLEAR OLD ITEM BUTTONS
        for button in self.item_buttons:
            button.kill()

        # GENERATE BUTTONS FOR NUMBER OF POSSIBLE PAGES (MAKE DYNAMICALLY ADJUSTABLE...)
        item_list = list(self.shop.categories[self.active_category].keys())
        print(f"NUMBER OF ITEMS SELECTED: {len(item_list)}")
        size = 100
        starting_y = self.config.screen_width - size
        starting_x = self.config.screen_width / 2
        pages = math.ceil(len(item_list) / (self.rows * self.cols))
        for page in range(pages):
            button_x = starting_x
            button_y = starting_y + (size * page)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, button_y), (size, size)),
                text=f"page {page}",
                manager=self.ui_manager,
            )
            self.shop_page_buttons[button] = lambda p=page: self.change_page(page)

        # GENERATE ITEMS FOR CURRENT PAGE
        items_on_page = self.rows * self.cols
        index = 0 + (self.shop_page * items_on_page) - 12
        while index < len(item_list) and index < items_on_page:
            row = index // self.cols // self.shop_page
            col = index % self.cols
            button_x = self.start_x + (col * self.frame_width)
            button_y = self.start_y + (row * self.frame_height)

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, button_y), (self.frame_width, self.frame_height)),
                text=item_list[index],
                manager=self.ui_manager,
            )
            self.item_buttons[button] = item_list[index]
            index += 1
        pass

    def make_purchase(self, item, player):
        if self.shop.make_purchase(item, player):
            return item
        else:
            return False

    def cleanup(self):
        for button in self.item_buttons:
            button.kill()
        for button in self.shop_menu_buttons:
            button.kill()
