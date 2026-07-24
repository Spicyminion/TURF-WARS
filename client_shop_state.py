from base_state import GameState
import json

class ShopState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.buttons ={}
        self.renderer = game.shop_renderer
        self._init()

    def _init(self):
        self.renderer.load_shop()

    def handle_click(self, x, y):
        pass

    def handle_button_pressed(self, event):
        # FIRST CHECK IF ANY STATE BUTTONS WERE CLICK
        button_clicked = self.buttons.get(event.ui_element)
        if button_clicked:
            button_clicked()
        # OTHERWISE PASS TO SHOP RENDERER TO CHECK
        else:
            item_clicked = self.renderer.handle_button_pressed(event)
            if item_clicked:
                print(f"item is {item_clicked}")

    def make_purchase(self, item_clicked):
        print("PURCHASING TEST (CLIENT -> SERVER)")
        message_id = f"{self.game.player_id}_{self.game.message_counter}"
        msg = {"action": "PURCHASE",
                        "item": item_clicked,
                        "category": "TBD",
                        "message_id": message_id}
        #self.game.client.send_to_server(msg)

    def handle_continuous_inputs(self, keys):
        pass

    def draw(self):
        pass
        #self.renderer.draw()

    def cleanup(self):
        for button in self.buttons:
            button.kill()
        self.renderer.cleanup()
