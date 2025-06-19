import arcade
import math

class TitleScreenView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.time = 0
        self.button_hover = False
        self.button_pressed = False
        self.button_rect = None  # (x, y, width, height)
        self.button_text = "Start Game"
        self.button_font_size = 20
        self.button_color = (180, 180, 200)
        self.button_color_hover = arcade.color.RED
        self.level_select_rects = []
        self.selected_level = 1
        self.level_count = 6  # Change if you have more/less levels

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()
        # Subtle animated background gradient
        for i in range(0, self.window.height, 4):
            t = i / self.window.height
            phase = self.time * 0.3
            gray = int(30 + 40 * (0.5 + 0.5 * math.sin(phase + t * 1.5)))
            arcade.draw_lrtb_rectangle_filled(
                0, self.window.width, self.window.height - i, self.window.height - i - 4, (gray, gray, gray + 10)
            )
        # Animated title: fade in/out and slight vertical movement
        pulse = 0.5 + 0.5 * math.sin(self.time * 1.5)
        y_offset = int(10 * math.sin(self.time * 0.8))
        title_color = (180, 180, 200 + int(30 * pulse))
        font_size = 48 + int(4 * pulse)
        arcade.draw_text(
            "TERMINUS",
            self.window.width // 2,
            self.window.height // 2 + 60 + y_offset,
            title_color,
            font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True,
            font_name="Kenney Future"
        )
        # --- Draw clickable Start button ---
        button_text = self.button_text
        button_font_size = self.button_font_size
        button_x = self.window.width // 2
        button_y = self.window.height // 2 - 40
        text_img = arcade.create_text_image(
            button_text, arcade.color.WHITE, button_font_size, font_name="Kenney Future")
        text_width, text_height = text_img.width, text_img.height
        button_w = text_width + 120
        button_h = text_height + 20
        self.button_rect = (
            button_x - button_w // 2, button_y - button_h // 2, button_w, button_h)
        # Detect hover/click color
        if self.button_pressed:
            color = arcade.color.RED
        elif self.button_hover:
            color = arcade.color.RED
        else:
            color = (180, 180, 200)
        # Draw button background (optional, subtle)
        arcade.draw_xywh_rectangle_filled(
            self.button_rect[0], self.button_rect[1], button_w, button_h, (
                60, 60, 60, 80)
        )
        # Draw button border
        arcade.draw_xywh_rectangle_outline(
            self.button_rect[0], self.button_rect[1], button_w, button_h, color, 3
        )
        # Draw button text
        arcade.draw_text(
            button_text,
            button_x,
            button_y,
            color,
            button_font_size,
            anchor_x="center",
            anchor_y="center",
            font_name="Kenney Future"
        )
        # --- Draw Shop button ---
        shop_text = "Shop"
        shop_font_size = 20
        shop_x = self.window.width * 4 // 5
        shop_y = self.window.height // 2 - 40
        shop_text_img = arcade.create_text_image(
            shop_text, arcade.color.WHITE, shop_font_size, font_name="Kenney Future")
        shop_text_width, shop_text_height = shop_text_img.width, shop_text_img.height
        shop_w = shop_text_width + 80
        shop_h = shop_text_height + 20
        self.shop_button_rect = (
            shop_x - shop_w // 2, shop_y - shop_h // 2, shop_w, shop_h)
        shop_color = arcade.color.RED if getattr(self, 'shop_button_hover', False) else (180, 180, 200)
        arcade.draw_xywh_rectangle_filled(
            self.shop_button_rect[0], self.shop_button_rect[1], shop_w, shop_h, (60, 60, 60, 80)
        )
        arcade.draw_xywh_rectangle_outline(
            self.shop_button_rect[0], self.shop_button_rect[1], shop_w, shop_h, shop_color, 3
        )
        arcade.draw_text(
            shop_text,
            shop_x,
            shop_y,
            shop_color,
            shop_font_size,
            anchor_x="center",
            anchor_y="center",
            font_name="Kenney Future"
        )
        # --- Draw level select ---
        self.level_select_rects = []
        levels = list(range(1, self.level_count + 1))
        select_y = self.window.height // 2 - 200
        button_x = self.window.width // 2
        for i, lvl in enumerate(levels):
            rect_w = 50
            rect_h = 40
            rect_x = button_x + i*60 - (rect_w + 10)*len(levels) // 2
            rect_y = select_y
            rect = (rect_x, rect_y, rect_w, rect_h)
            self.level_select_rects.append((rect, lvl))
            color = arcade.color.YELLOW if self.selected_level == lvl else (120, 120, 120)
            arcade.draw_xywh_rectangle_filled(rect_x, rect_y, rect_w, rect_h, (40, 40, 40, 200))
            arcade.draw_xywh_rectangle_outline(rect_x, rect_y, rect_w, rect_h, color, 3)
            arcade.draw_text(f"{lvl}", rect_x+rect_w//2, rect_y+rect_h//2, color, 18, anchor_x="center", anchor_y="center", font_name="Kenney Future")
        arcade.draw_text("Select Level", button_x, select_y+70, arcade.color.LIGHT_GRAY, 16, anchor_x="center", anchor_y="center", font_name="Kenney Future")
        # Draw custom cursor on title screen
        self.draw_custom_cursor()

    def draw_custom_cursor(self):
        # Draw a simple custom cursor (replace with image if desired)
        x, y = self._last_mouse_pos if hasattr(self, '_last_mouse_pos') else (self.window.width // 2, self.window.height // 2)
        arcade.draw_circle_filled(x, y, 10, arcade.color.YELLOW)

    def on_mouse_motion(self, x, y, dx, dy):
        self.button_hover = self._mouse_in_button(x, y)
        self.shop_button_hover = False
        self._last_mouse_pos = (x, y)
        # Shop button hover
        if hasattr(self, 'shop_button_rect'):
            bx, by, bw, bh = self.shop_button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.shop_button_hover = True
        # Level select hover (optional highlight)
        for rect, lvl in self.level_select_rects:
            bx, by, bw, bh = rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                arcade.draw_xywh_rectangle_outline(bx, by, bw, bh, arcade.color.RED, 3)

    def on_mouse_press(self, x, y, button, modifiers):
        if self._mouse_in_button(x, y):
            self.button_pressed = True
        # Check if a level select rect was clicked
        for rect, lvl in self.level_select_rects:
            bx, by, bw, bh = rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.selected_level = lvl

    def on_mouse_release(self, x, y, button, modifiers):
        # Check if shop button was clicked
        if hasattr(self, 'shop_button_rect'):
            bx, by, bw, bh = self.shop_button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                print("Shop button clicked")
                # Import here to avoid circular import
                from shop_screen import ShopScreenView
                self.window.show_view(ShopScreenView(self.game_view))
                # change state to shop view
                self.game_view.set_state("SHOP")
                return
        # Check if a level select rect was clicked
        for rect, lvl in self.level_select_rects:
            bx, by, bw, bh = rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.selected_level = lvl
                return
        # Otherwise, check if start button was clicked
        if self.button_pressed and self._mouse_in_button(x, y):
            print(f"Starting game with level {self.selected_level}")
            # load the selected level
            self.game_view.selected_level = self.selected_level
            self.game_view.load_level(self.selected_level)
            self.button_pressed = False
            self.window.set_mouse_visible(False)
            self.game_view.set_state("GAME")
        else:
            self.button_pressed = False

    def _mouse_in_button(self, x, y):
        if not self.button_rect:
            return False
        bx, by, bw, bh = self.button_rect
        return bx <= x <= bx + bw and by <= y <= by + bh

    def on_update(self, delta_time):
        self.time += delta_time

    def on_key_press_TITLE(self, key, modifiers):
        # Allow level selection with arrow keys
        if key == arcade.key.LEFT:
            self.selected_level = max(1, self.selected_level - 1)
            self.game_view.selected_level = self.selected_level
        elif key == arcade.key.RIGHT:
            self.selected_level = min(self.level_count, self.selected_level + 1)
            self.game_view.selected_level = self.selected_level
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            self.window.set_mouse_visible(False)
            self.game_view.selected_level = self.selected_level
            self.game_view.load_level(self.selected_level)
            self.game_view.set_state("GAME")
