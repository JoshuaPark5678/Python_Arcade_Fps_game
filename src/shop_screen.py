import arcade
import copy

class ShopScreenView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        # Use persistent shop_items from game_view
        self.items = self.game_view.shop_items
        self.selected = 0
        self.button_rects = []
        self.button_item_indices = []  # <-- Track mapping to self.items
        self._last_mouse_pos = (0, 0)
        self._hover = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()
        # Draw semi-transparent shop panel
        panel_w, panel_h = 500, 600
        panel_x = self.window.width // 2 - panel_w // 2
        panel_y = self.window.height // 2 - panel_h // 2
        arcade.draw_xywh_rectangle_filled(panel_x, panel_y, panel_w, panel_h, (20, 20, 40, 230))
        arcade.draw_xywh_rectangle_outline(panel_x, panel_y, panel_w, panel_h, arcade.color.YELLOW, 4)
        # Shop title
        arcade.draw_text("SHOP", self.window.width//2, panel_y + panel_h - 50, arcade.color.YELLOW, 48, anchor_x="center", font_name="Kenney Future")
        # Group items for layout
        health_items = [item for item in self.items if 'Health' in item['name']]
        revolver_items = [item for item in self.items if 'REVOLVER' in item['name']]
        shotgun_items = [item for item in self.items if 'SHOTGUN' in item['name']]
        y = panel_y + panel_h - 70  # Move items up, reduce gap after SHOP
        self.button_rects = []
        self.button_item_indices = []  # <-- Track mapping to self.items
        global_idx = 0
        section_gap = 32
        item_gap = 18
        button_height = 42
        button_width = panel_w - 80
        label_x = panel_x + 40
        # Health section
        if health_items:
            arcade.draw_text("Player", label_x, y, arcade.color.LIGHT_GREEN, 20, font_name="Kenney Future", anchor_y="top")
            y -= section_gap
            for item in health_items:
                bx, by, bw, bh = label_x, y - button_height, button_width, button_height
                # Shadow
                arcade.draw_xywh_rectangle_filled(bx+2, by-2, bw, bh, (0,0,0,60))
                # Highlight
                if self.selected == global_idx or self._hover == global_idx:
                    grad_color = arcade.color.YELLOW_ORANGE if self.selected == global_idx else arcade.color.LIGHT_YELLOW
                    arcade.draw_xywh_rectangle_filled(bx, by, bw, bh, grad_color + (60,))
                # Button bg
                arcade.draw_xywh_rectangle_filled(bx, by, bw, bh, (40, 40, 60, 220))
                arcade.draw_xywh_rectangle_outline(bx, by, bw, bh, arcade.color.YELLOW if self.selected == global_idx or self._hover == global_idx else arcade.color.LIGHT_GRAY, 2)
                # Icon (colored circle)
                icon_color = arcade.color.GREEN
                arcade.draw_circle_filled(bx+24, by+bh//2, 14, icon_color)
                # Item name/price
                arcade.draw_text(f"{item['name']}", bx+48, by+bh//2, arcade.color.WHITE, 12, anchor_y="center", font_name="Kenney Future")
                arcade.draw_text(f"${item['price']}", bx+bw-16, by+bh//2, arcade.color.YELLOW, 16, anchor_y="center", anchor_x="right", font_name="Kenney Future")
                self.button_rects.append((bx, by, bw, bh))
                # Map button to correct index in self.items
                self.button_item_indices.append(self.items.index(item))
                y = by - item_gap
                global_idx += 1

        # Revolver section
        if revolver_items:
            arcade.draw_text("Revolver", label_x, y, arcade.color.LIGHT_BLUE, 20, font_name="Kenney Future", anchor_y="top")
            y -= section_gap
            for item in revolver_items:
                bx, by, bw, bh = label_x, y - button_height, button_width, button_height
                # Shadow
                arcade.draw_xywh_rectangle_filled(bx+2, by-2, bw, bh, (0,0,0,60))
                if self.selected == global_idx or self._hover == global_idx:
                    grad_color = arcade.color.YELLOW_ORANGE if self.selected == global_idx else arcade.color.LIGHT_YELLOW
                    arcade.draw_xywh_rectangle_filled(bx, by, bw, bh, grad_color + (60,))
                arcade.draw_xywh_rectangle_filled(bx, by, bw, bh, (40, 40, 60, 220))
                arcade.draw_xywh_rectangle_outline(bx, by, bw, bh, arcade.color.YELLOW if self.selected == global_idx or self._hover == global_idx else arcade.color.LIGHT_GRAY, 2)
                icon_color = arcade.color.LIGHT_BLUE
                arcade.draw_circle_filled(bx+24, by+bh//2, 14, icon_color)
                arcade.draw_text(f"{item['name']}", bx+48, by+bh//2, arcade.color.WHITE, 12, anchor_y="center", font_name="Kenney Future")
                arcade.draw_text(f"${item['price']}", bx+bw-16, by+bh//2, arcade.color.YELLOW, 16, anchor_y="center", anchor_x="right", font_name="Kenney Future")
                self.button_rects.append((bx, by, bw, bh))
                self.button_item_indices.append(self.items.index(item))
                y = by - item_gap
                global_idx += 1
        # Shotgun section
        if shotgun_items:
            arcade.draw_text("Shotgun", label_x, y, arcade.color.LIGHT_CORAL, 20, font_name="Kenney Future", anchor_y="top")
            y -= section_gap
            for item in shotgun_items:
                bx, by, bw, bh = label_x, y - button_height, button_width, button_height
                arcade.draw_xywh_rectangle_filled(bx+2, by-2, bw, bh, (0,0,0,60))
                if self.selected == global_idx or self._hover == global_idx:
                    grad_color = arcade.color.YELLOW_ORANGE if self.selected == global_idx else arcade.color.LIGHT_YELLOW
                    arcade.draw_xywh_rectangle_filled(bx, by, bw, bh, grad_color + (60,))
                arcade.draw_xywh_rectangle_filled(bx, by, bw, bh, (40, 40, 60, 220))
                arcade.draw_xywh_rectangle_outline(bx, by, bw, bh, arcade.color.YELLOW if self.selected == global_idx or self._hover == global_idx else arcade.color.LIGHT_GRAY, 2)
                icon_color = arcade.color.LIGHT_CORAL
                arcade.draw_circle_filled(bx+24, by+bh//2, 14, icon_color)
                arcade.draw_text(f"{item['name']}", bx+48, by+bh//2, arcade.color.WHITE, 12, anchor_y="center", font_name="Kenney Future")
                arcade.draw_text(f"${item['price']}", bx+bw-16, by+bh//2, arcade.color.YELLOW, 16, anchor_y="center", anchor_x="right", font_name="Kenney Future")
                self.button_rects.append((bx, by, bw, bh))
                self.button_item_indices.append(self.items.index(item))
                y = by - item_gap
                global_idx += 1

        # Draw currency in the top-left corner, out of the way
        currency = getattr(self.game_view.player, 'currency', 0)
        arcade.draw_xywh_rectangle_filled(24, self.window.height-62, 140, 38, (30, 30, 60, 200))
        arcade.draw_xywh_rectangle_outline(24, self.window.height-62, 140, 38, arcade.color.YELLOW, 2)
        arcade.draw_text(f"$ {currency}", 94, self.window.height-43, arcade.color.YELLOW, 22, anchor_x="center", anchor_y="center", font_name="Kenney Future")
        # Draw exit button in the top right of the shop panel
        exit_bw, exit_bh = 120, 40
        bx = panel_x + panel_w - exit_bw - 16
        by = panel_y + panel_h - exit_bh - 16
        color = arcade.color.RED if self._hover == 'exit' else arcade.color.LIGHT_GRAY
        arcade.draw_xywh_rectangle_filled(bx, by, exit_bw, exit_bh, (60, 0, 0, 220))
        arcade.draw_xywh_rectangle_outline(bx, by, exit_bw, exit_bh, color, 3)
        arcade.draw_text("Exit Shop", bx+exit_bw//2, by+exit_bh//2, color, 10, anchor_x="center", anchor_y="center", font_name="Kenney Future")
        self.exit_rect = (bx, by, exit_bw, exit_bh)

        # Draw purchased upgrades on the right side of the shop
        upgrades_y = panel_y + panel_h - 60
        upgrades_x = panel_x + panel_w + 30
        arcade.draw_text("Upgrades Purchased", upgrades_x, upgrades_y, arcade.color.YELLOW, 18, font_name="Kenney Future")
        upgrades_y -= 32
        for item in self.items:
            if item['count'] > 0:
                arcade.draw_text(f"{item['name']}: {item['count']}", upgrades_x, upgrades_y, arcade.color.WHITE, 16, font_name="Kenney Future")
                upgrades_y -= 26

    def on_mouse_motion(self, x, y, dx, dy):
        self._last_mouse_pos = (x, y)
        self._hover = None
        # Defensive: ensure exit_rect exists (draw must have run at least once)
        if not hasattr(self, 'exit_rect'):
            return
        for i, (bx, by, bw, bh) in enumerate(self.button_rects):
            if bx <= x <= bx+bw and by <= y <= by+bh:
                self._hover = i
        bx, by, bw, bh = self.exit_rect
        if bx <= x <= bx+bw and by <= y <= by+bh:
            self._hover = 'exit'

    def on_mouse_press(self, x, y, button, modifiers):
        if self._hover == 'exit':
            self.game_view.set_state("TITLE")
            return
        if isinstance(self._hover, int):
            self.selected = self._hover
            # Use button_item_indices to get the correct item index
            item_idx = self.button_item_indices[self.selected]
            self.buy_item(item_idx)

    def on_key_press_SHOP(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected = (self.selected - 1) % len(self.button_item_indices)
        elif key == arcade.key.DOWN:
            self.selected = (self.selected + 1) % len(self.button_item_indices)
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            item_idx = self.button_item_indices[self.selected]
            self.buy_item(item_idx)
        elif key == arcade.key.ESCAPE or key == arcade.key.T and self.game_view.state == "SHOP":
            self.game_view.set_state("TITLE")
            
    def buy_item(self, idx):
        item = self.items[idx]
        player = getattr(self.game_view, 'player', None)
        wm = getattr(self.game_view, 'weapon_manager', None)
        if player and getattr(player, 'currency', 0) >= item['price']:
            player.currency -= item['price']
            # Apply item effect
            if item['name'] == 'Health +1':
                if hasattr(player, 'health'):
                    if player.health < player.max_health:
                        player.health += 1
                    else:
                        # give back money
                        player.currency += item['price']
                        return
            elif item['name'] == 'REVOLVER DMG+' and wm:
                if hasattr(wm.weapons["REVOLVER"], "damage"):
                    wm.weapons["REVOLVER"].damage += 5
            elif item['name'] == 'SHOTGUN DMG+' and wm:
                if hasattr(wm.weapons["SHOTGUN"], "damage"):
                    wm.weapons["SHOTGUN"].damage += 2
            elif item['name'] == 'REVOLVER HS+' and wm:
                if hasattr(wm.weapons["REVOLVER"], "HS_multiplier"):
                    wm.weapons["REVOLVER"].HS_multiplier += 0.5
            elif item['name'] == 'SHOTGUN HS+' and wm:
                if hasattr(wm.weapons["SHOTGUN"], "HS_multiplier"):
                    wm.weapons["SHOTGUN"].HS_multiplier += 0.5
            elif item['name'] == 'REVOLVER SPD+' and wm:
                if hasattr(wm.weapons["REVOLVER"], "animations_speed"):
                    wm.weapons["REVOLVER"].animations_speed = max(0.001, wm.weapons["REVOLVER"].animations_speed * 0.6)
            elif item['name'] == 'SHOTGUN SPD+' and wm:
                if hasattr(wm.weapons["SHOTGUN"], "animations_speed"):
                    wm.weapons["SHOTGUN"].animations_speed = max(0.001, wm.weapons["SHOTGUN"].animations_speed * 0.6)
            # Scale price and count
            item['count'] += 1
            item['price'] = int(item['base_price'] * (1.5 ** item['count']))
