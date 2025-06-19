import arcade
import math
import time
import os


class Weapon:
    def __init__(self, game):
        self.game = game  # Reference to the main game for screen size, etc.
        self.shake_speed = 0
        self.shake_intensity = 0
        self.shake_direction = 1

    def update(self, delta_time):
        pass

    def draw(self):
        pass

    def start_transition(self, to_ADS: bool):
        """
        Start the transition animation for ADS in or out.
        :param to_ADS: True if transitioning into ADS, False if out of ADS
        """
        self.in_transition = True
        if to_ADS:
            self.transition_frame = 0
        else:
            self.transition_frame = len(self.ADS_transition_textures) - 1
        self.time_since_last_frame = 0

    def update_transition(self, delta_time, to_ADS: bool):
        if not self.in_transition:
            return
        # stop shooting animation if in transition

        self.time_since_last_frame += delta_time
        # Always move by one frame per animation_speed, regardless of direction
        # Added a small buffer to ensure smooth transition
        if self.time_since_last_frame >= self.animation_speed - 0.01:
            if to_ADS:
                if self.transition_frame < len(self.ADS_transition_textures) - 1:
                    self.transition_frame += 1
                else:
                    self.in_transition = False
            else:
                if self.transition_frame > 0:
                    self.transition_frame -= 1
                else:
                    self.in_transition = False
            self.time_since_last_frame = 0


class Revolver(Weapon):
    def __init__(self, game):
        super().__init__(game)
        self.type = "REVOLVER"
        self.max_ammo = 5
        self.shoot_textures = []
        self.ADS_shoot_textures = []
        self.ADS_transition_textures = []
        self.reload_textures = []
        self.current_frame = 0
        self.in_reload = False
        self.reload_frame = 0
        self.in_transition = False
        self.transition_frame = 0
        self.weapon_anim_running = False
        self.time_since_last_frame = 0
        self.animation_speed = 0.02
        self.chamber = [1] * self.max_ammo
        self.cylinder_spin = 0  # Spin of the cylinder
        self.spin_aim = 0  # The cylinder spin till reaching the aim
        self.sound_volume = 0.2  # Default sound volume
        self.shoot_sound = None
        self.reload_sound = None
        # Upgradeable stats
        self.damage = 10
        self.HS_multiplier = 1.5
        # ...add more as needed...

    def draw_cylinder(self):
        # display CYLINDER
        cylinder_radius = self.game.screen_width // 10
        if self.current_frame < 8:
            cylinder_radius += self.current_frame // 2
        else:
            cylinder_radius -= (self.current_frame - 8) // 2

        # center of the cylinder
        center = [self.game.screen_width -
                  cylinder_radius // 2, cylinder_radius // 2]

        # Draw the cylinder body
        arcade.draw_circle_filled(
            center[0], center[1], cylinder_radius, (45, 45, 55))
        arcade.draw_circle_filled(center[0], center[1], int(
            cylinder_radius // 1.2), arcade.color.GRAY)
        arcade.draw_circle_outline(
            center[0], center[1], cylinder_radius, arcade.color.BLACK, 4)
        # draw the cylinder middle thingy
        arcade.draw_circle_filled(
            center[0], center[1], cylinder_radius // 6, (55, 55, 65))
        arcade.draw_circle_outline(
            center[0], center[1], cylinder_radius // 6, arcade.color.BLACK, 4)

        # draw the cylinder bullets (5 bullets)
        angle = 360 / 5
        back_cycle = 90 if self.current_frame < 1 else 162
        # The top chamber (to fire) is always chamber[0], then chamber[1], ...
        for i in range(5):
            bullet_angle = math.radians(angle * i + back_cycle - self.cylinder_spin)
            bullet_x = center[0] + cylinder_radius // 2 * math.cos(bullet_angle)
            bullet_y = center[1] + cylinder_radius // 2 * math.sin(bullet_angle)
            # Visual chamber order: top is chamber[0], then [1], ...
            bullet = self.chamber[i] if i < len(self.chamber) else 0
            if bullet == 1:
                arcade.draw_circle_filled(
                    bullet_x, bullet_y, cylinder_radius // 6, arcade.color.DARK_GRAY)
            elif bullet == 2:
                arcade.draw_circle_filled(
                    bullet_x, bullet_y, cylinder_radius // 6, arcade.color.GOLD)
            else:
                arcade.draw_circle_filled(
                    bullet_x, bullet_y, cylinder_radius // 6, arcade.color.BLACK)
            arcade.draw_circle_outline(
                bullet_x, bullet_y, cylinder_radius // 6, arcade.color.BLACK, 2)

    def draw(self):
        try:
            if self.in_reload:
                arcade.draw_texture_rectangle(
                    (self.game.screen_width // 2) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                    (self.game.screen_height // 2 - 60) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                    self.game.screen_width,
                    self.game.screen_height + 20,
                    self.reload_textures[self.reload_frame]
                )
            elif self.in_transition:
                arcade.draw_texture_rectangle(
                    (self.game.screen_width // 2) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                    (self.game.screen_height // 2 - 60) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                    self.game.screen_width,
                    self.game.screen_height + 20,
                    self.ADS_transition_textures[self.transition_frame]
                )
            else:
                # If ADSed, use ADS textures for normal draw
                if self.game.weapon_manager.is_ADS and len(self.ADS_shoot_textures) > 0:
                    arcade.draw_texture_rectangle(
                        (self.game.screen_width // 2) + math.sin(
                            time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                        (self.game.screen_height // 2 - 60) + math.sin(
                            time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                        self.game.screen_width,
                        self.game.screen_height + 20,
                        self.ADS_shoot_textures[self.current_frame]
                    )
                else:
                    arcade.draw_texture_rectangle(
                        (self.game.screen_width // 2) + math.sin(
                            time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                        (self.game.screen_height // 2 - 60) + math.sin(
                            time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                        self.game.screen_width,
                        self.game.screen_height + 20,
                        self.shoot_textures[self.current_frame]
                    )
        except IndexError:
            print(
                "Error: Texture index out of range. Ensure textures are loaded correctly.")

        self.draw_cylinder()

    def draw_UI(self):
        # display CYLINDER
        self.draw_cylinder()

    def shoot(self):
        if not self.in_reload:
            self.current_frame = 0
            self.weapon_anim_running = True
            self.time_since_last_frame = 0

            self.spin_aim = (self.cylinder_spin + 72) % 360

            # play the shoot sound
            self.shoot_sound.play(volume=self.sound_volume)

    def reload_weapon(self):
        if not self.in_reload:
            self.in_reload = True
            self.reload_frame = 0
            self.time_since_last_frame = 0
            
            self.reload_sound.play(speed=2.0, volume=self.sound_volume)

    def update(self, delta_time):
        self.shake_speed = self.game.shake_speed
        self.shake_intensity = self.game.shake_intensity
        self.shake_direction = self.game.shake_direction

        # Handle ADS transition
        if self.in_transition:
            self.update_transition(delta_time, self.game.weapon_manager.is_ADS)
            return  # Only play transition animation during transition

        if self.in_reload:
            self.time_since_last_frame += delta_time
            if self.time_since_last_frame >= self.animation_speed:
                self.reload_frame += 1
                if self.reload_frame >= len(self.reload_textures):
                    self.in_reload = False
                    self.reload_frame = 0
                    self.weapon_anim_running = False
                self.time_since_last_frame = 0

        # Update shooting animation
        if self.weapon_anim_running and not self.in_reload and not self.in_transition:
            self.time_since_last_frame += delta_time
            if self.time_since_last_frame >= self.animation_speed:
                self.current_frame += 1
                if self.game.weapon_manager.is_ADS and len(self.ADS_shoot_textures) > 0:
                    if self.current_frame >= len(self.ADS_shoot_textures):
                        self.current_frame = 0
                        self.weapon_anim_running = False
                else:
                    if self.current_frame >= len(self.shoot_textures):
                        self.current_frame = 0
                        self.weapon_anim_running = False
                self.time_since_last_frame = 0
                
        if not self.in_reload and not self.in_transition and not self.weapon_anim_running:
            # Reset current frame if not animating
            self.current_frame = 0

        self.update_revolver_animation(delta_time)

    def update_revolver_animation(self, delta_time):
        if self.in_reload:
            # Handle chamber and cylinder spin during reload
            try:
                if 15 < self.reload_frame < 21:
                    try:
                        self.chamber[self.reload_frame - 16] = 0
                    except IndexError:
                        self.chamber.append(0)
                if 39 < self.reload_frame < 45:
                    self.chamber[self.reload_frame - 40] = 1
                if self.reload_frame > 41:
                    self.cylinder_spin += 12
                    if self.cylinder_spin >= 360:
                        self.cylinder_spin -= 360
                else:
                    if self.reload_frame > 12:
                        self.cylinder_spin -= 4
                        if self.cylinder_spin >= 360:
                            self.cylinder_spin = 0
            except Exception:
                pass

            if self.reload_frame == len(self.reload_textures) - 1:
                self.cylinder_spin = 0
                if getattr(self, 'is_ADS', False):
                    self.in_transition = True
                    self.transition_frame = 0
                else:
                    self.in_transition = False
                    self.transition_frame = 0

        # ON SHOOT animate the cylinder spin by exactly 72 degrees per shot
        if self.weapon_anim_running and not self.in_reload and not self.in_transition:
            # Animate the cylinder spin smoothly over the first few frames of the shot
            if self.current_frame >= 3 and self.cylinder_spin < self.spin_aim:
                self.cylinder_spin += 6
                # print("Cylinder spin:", self.cylinder_spin)
            elif self.current_frame > 12:
                self.cylinder_spin = self.spin_aim
            # Reset the spin if it exceeds 360 degrees
            if self.cylinder_spin >= 360:
                self.cylinder_spin -= 360


class Shotgun(Weapon):
    def __init__(self, game):
        super().__init__(game)
        self.type = "SHOTGUN"
        self.max_ammo = 4
        self.shoot_textures = []
        self.ADS_shoot_textures = []
        self.ADS_transition_textures = []
        self.reload_textures = []
        self.current_frame = 0
        self.in_reload = False
        self.reload_frame = 0
        self.in_transition = False
        self.transition_frame = 0
        self.anim_running = False
        self.time_since_last_frame = 0
        self.animation_speed = 0.03
        self.chamber = [1] * self.max_ammo
        self.sound_volume = 0.2  # Default sound volume
        self.shoot_sound = None
        self.reload_sound = None
        # Upgradeable stats
        self.damage = 5
        self.HS_multiplier = 1.5
        # ...add more as needed...

    def draw(self):
        try:
            if self.in_reload:
                arcade.draw_texture_rectangle(
                    (self.game.screen_width // 2) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                    (self.game.screen_height // 2 - 60) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                    self.game.screen_width,
                    self.game.screen_height + 20,
                    self.reload_textures[self.reload_frame]
                )
            elif self.in_transition:
                arcade.draw_texture_rectangle(
                    (self.game.screen_width // 2) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                    (self.game.screen_height // 2 - 60) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                    self.game.screen_width,
                    self.game.screen_height + 20,
                    self.ADS_transition_textures[self.transition_frame]
                )
            elif self.game.weapon_manager.is_ADS:
                arcade.draw_texture_rectangle(
                    (self.game.screen_width // 2) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                    (self.game.screen_height // 2 - 60) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                    self.game.screen_width,
                    self.game.screen_height + 20,
                    self.ADS_shoot_textures[self.current_frame]
                )
            else:
                arcade.draw_texture_rectangle(
                    (self.game.screen_width // 2) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                    (self.game.screen_height // 2 - 60) + math.sin(
                        time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                    self.game.screen_width,
                    self.game.screen_height + 20,
                    self.shoot_textures[self.current_frame]
                )
        except IndexError:
            print(
                "Error: Texture index out of range. Ensure textures are loaded correctly.")
            
        self.draw_UI()
            
    def draw_UI(self):
        # draw the shotgun shells
        shell_height = self.game.screen_height // 12
        shell_width = shell_height // 2
        shell_x = self.game.screen_width - shell_width - shell_width * 4
        shell_y = self.game.screen_height * 0.05

        for i in range(self.max_ammo):
            if self.chamber[i] == 1:
                arcade.draw_xywh_rectangle_filled(
                    shell_x + i * (shell_width + 5),
                    shell_y,
                    shell_width,
                    shell_height,
                    arcade.color.RED
                )
                arcade.draw_xywh_rectangle_filled(
                    shell_x + i * (shell_width + 5),
                    shell_y,
                    shell_width,
                    shell_height // 4,
                    arcade.color.GOLD
                )
                arcade.draw_xywh_rectangle_outline(
                    shell_x + i * (shell_width + 5),
                    shell_y,
                    shell_width,
                    shell_height,
                    arcade.color.BLACK,
                    2
                )

    def shoot(self):
        if not self.in_reload:
            self.current_frame = 0
            self.anim_running = True
            self.time_since_last_frame = 0
            
            # play the shoot sound
            self.shoot_sound.play(volume=self.sound_volume)

    def reload_weapon(self):
        if not self.in_reload:
            self.in_reload = True
            self.reload_frame = 0
            self.time_since_last_frame = 0
            self.anim_running = True

            self.reload_sound.play(volume=self.sound_volume)

    def update(self, delta_time):
        self.shake_speed = self.game.shake_speed
        self.shake_intensity = self.game.shake_intensity
        self.shake_direction = self.game.shake_direction

        # Handle ADS transition
        if self.in_transition:
            self.update_transition(delta_time, self.game.weapon_manager.is_ADS)
            return  # Only play transition animation during transition

        if self.in_reload:
            self.time_since_last_frame += delta_time
            if self.time_since_last_frame >= self.animation_speed:
                self.reload_frame += 1
                if self.reload_frame >= len(self.reload_textures):
                    self.in_reload = False
                    self.reload_frame = 0
                    self.anim_running = False
                self.time_since_last_frame = 0

        # Update shooting animation
        if self.anim_running and not self.in_reload and not self.in_transition:
            self.time_since_last_frame += delta_time
            if self.time_since_last_frame >= self.animation_speed:
                self.current_frame += 1
                if self.game.weapon_manager.is_ADS and len(self.ADS_shoot_textures) > 0:
                    if self.current_frame >= len(self.ADS_shoot_textures):
                        self.current_frame = 0
                        self.anim_running = False
                elif self.current_frame == len(self.shoot_textures) - 10:
                    self.reload_sound.play(volume=self.sound_volume)
                else:
                    if self.current_frame >= len(self.shoot_textures):
                        self.current_frame = 0
                        self.anim_running = False
                self.time_since_last_frame = 0
                
        if not self.in_reload and not self.in_transition and not self.anim_running:
            # Reset current frame if not animating
            self.current_frame = 0
        self.update_shotgun_animation(delta_time)
        
    def update_shotgun_animation(self, delta_time):
        if self.in_reload:
            # Handle chamber and cylinder spin during reload
            try:
                if 39 < self.reload_frame < 45:
                    self.chamber[self.reload_frame - 40] = 1
            except Exception:
                pass

            if self.reload_frame == len(self.reload_textures) - 1:
                if getattr(self, 'is_ADS', False):
                    self.in_transition = True
                    self.transition_frame = 0
                else:
                    self.in_transition = False
                    self.transition_frame = 0


class WeaponManager:
    def __init__(self, game):
        self.game = game
        self.isLoaded = False
        self.weapons = {
            "REVOLVER": Revolver(game),
            "SHOTGUN": Shotgun(game)
        }
        self.current = self.weapons["REVOLVER"]

        self.file_dir = game.file_dir
        self.currentLoading = 0
        self.totalLoading = 100

        self.is_ADS = False

        self.setup_sounds(game)

    def setup_sounds(self, game):
        self.weapons["REVOLVER"].shoot_sound = arcade.load_sound(
            f"{game.file_dir}/sounds/revolver_shoot.wav")
        self.weapons["SHOTGUN"].shoot_sound = arcade.load_sound(
            f"{game.file_dir}/sounds/shotgun_shoot.wav")
        self.weapons["REVOLVER"].reload_sound = arcade.load_sound(
            f"{game.file_dir}/sounds/revolver_spin.wav")
        self.weapons["SHOTGUN"].reload_sound = arcade.load_sound(
            f"{game.file_dir}/sounds/shotgun_pump.wav")

    def switch(self, weapon_name):
        if weapon_name in self.weapons:
            self.current = self.weapons[weapon_name]
            # Always cancel ADS state and transition when switching weapons
            self.is_ADS = False
            self.current.in_transition = False
            self.current.transition_frame = 0
            # Also call ADS(False) to ensure any stuck state is cleared
            self.ADS(False)

    def shoot(self):
        # Only allow shooting if not in reload, not in transition, and not in shooting animation
        if not self.current.in_reload and not self.current.in_transition and not getattr(self.current, 'weapon_anim_running', False) and not getattr(self.current, 'anim_running', False):
            # If not, proceed to shoot
            if self.current.chamber.count(1) > 0:
                self.current.shoot()
                # Remove one bullet from the chamber
                self.current.chamber[self.current.chamber.index(1)] = 0
                return True
        else:
            return False

    def reload_weapon(self):
        self.current.reload_weapon()

    def ADS(self, to_ADS: bool):
        """
        Start the ADS transition animation.
        :param to_ADS: True to enter ADS, False to exit ADS
        """
        self.current.start_transition(to_ADS)
        self.is_ADS = to_ADS

    def update(self, delta_time):
        # Handle ADS transition direction and state here
        # Transition is now handled in weapon's update
        # Always cancel ADS if reloading
        if self.current.in_reload and self.is_ADS:
            self.ADS(False)
        self.current.update(delta_time)

    def draw(self):
        # Draw weapon icons in the UI (bottom left corner)
        icon_size_selected = 96
        icon_size_unselected = 64
        padding = 24
        base_x = padding + icon_size_selected // 2
        base_y = padding + icon_size_selected // 2
        
        # Make shotgun icon longer (wider)
        shotgun_selected_width = int(icon_size_selected * 1.5)
        shotgun_unselected_width = int(icon_size_unselected * 1.5)
        shotgun_selected_height = icon_size_selected
        shotgun_unselected_height = icon_size_unselected
        
        # Draw revolver icon
        if self.current.type == "REVOLVER":
            # Selected revolver
            arcade.draw_texture_rectangle(
                base_x, base_y, icon_size_selected, icon_size_selected, self.game.revolver_icon, alpha=255
            )
            # Unselected shotgun (longer)
            arcade.draw_texture_rectangle(
                base_x + icon_size_selected + padding, base_y, shotgun_unselected_width, shotgun_unselected_height, self.game.shotgun_icon, alpha=180
            )
        else:
            # Unselected revolver
            arcade.draw_texture_rectangle(
                base_x, base_y, icon_size_unselected, icon_size_unselected, self.game.revolver_icon, alpha=180
            )
            # Selected shotgun (longer)
            arcade.draw_texture_rectangle(
                base_x + icon_size_selected + padding, base_y, shotgun_selected_width, shotgun_selected_height, self.game.shotgun_icon, alpha=255
            )
        
        # Draw the current weapon (main view)
        self.current.draw()

    def setup_weapon_textures(self):
        start = time.time()
        revolver = self.weapons["REVOLVER"]
        shotgun = self.weapons["SHOTGUN"]
        self.currentLoading = 0
        self.totalLoading = len(os.listdir(f"{self.file_dir}/model_ui/revolver/shoot/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/revolver/ADS_shoot/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/revolver/ADS_transition/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/revolver/Reload/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/shotgun/shoot/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/shotgun/ADS_shoot/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/shotgun/ADS_transition/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/shotgun/Reload/"))

        # REVOLVER TEXTURES
        for i in range(1, 17):
            texture_path = f"{self.file_dir}/model_ui/revolver/shoot/{i:04d}.png"
            revolver.shoot_textures.append(arcade.load_texture(texture_path))
            self.currentLoading += 1
        for i in range(1, 17):
            texture_path = f"{self.file_dir}/model_ui/revolver/ADS_shoot/{i:04d}.png"
            revolver.ADS_shoot_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1
        for i in range(1, 9):
            texture_path = f"{self.file_dir}/model_ui/revolver/ADS_transition/{i:04d}.png"
            revolver.ADS_transition_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1
        for i in range(1, 73):
            texture_path = f"{self.file_dir}/model_ui/revolver/Reload/{i:04d}.png"
            revolver.reload_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1
        print("Revolver textures loaded")
        # SHOTGUN TEXTURES
        for i in range(1, 27):
            texture_path = f"{self.file_dir}/model_ui/shotgun/shoot/{i:04d}.png"
            shotgun.shoot_textures.append(arcade.load_texture(texture_path))
            self.currentLoading += 1
        for i in range(1, 27):
            texture_path = f"{self.file_dir}/model_ui/shotgun/ADS_shoot/{i:04d}.png"
            shotgun.ADS_shoot_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1
        for i in range(1, 9):
            texture_path = f"{self.file_dir}/model_ui/shotgun/ADS_transition/{i:04d}.png"
            shotgun.ADS_transition_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1
        for i in range(1, 65):
            texture_path = f"{self.file_dir}/model_ui/shotgun/Reload/{i:04d}.png"
            shotgun.reload_textures.append(arcade.load_texture(texture_path))
            self.currentLoading += 1
        print("Shotgun textures loaded")
        print("Textures loaded in", time.time() - start, "seconds")
        self.isLoaded = True
