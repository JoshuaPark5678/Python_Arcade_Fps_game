# Organize imports
import arcade
import arcade.resources
import pyglet
from pyglet.math import Mat4, Vec3
from array import array
from arcade.gl import BufferDescription
import math
from pygltflib import GLTF2
import time
import os
import random
import threading

# Import the necessary files

# ----- LEVELS ----- #
import level1
import level2
import level3
import level4
import level5
import level6

# ----- UTILS ----- #
import gltf_utils
import raycast
import weapons
from title_screen import TitleScreenView
from shop_screen import ShopScreenView

# Constants for screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Player:
    def __init__(self):
        self.max_health = 5  # Player's maximum health
        self.health = self.max_health  # Player's health
        self.is_alive = True  # Player's alive status
        self.currency = 5000  # Player's currency

    def apply_damage(self, damage):
        """
        Apply damage to the player and check if the player is still alive.
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            self.health = 0

    def add_currency(self, amount):
        """
        Add currency to the player.
        """
        self.currency += amount
        print(f"Currency added: {amount}. Total: {self.currency}")


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,
                         "Simple 3D Plane", resizable=True)
        # FILE LOCATION
        self.file_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        print(self.file_dir)

        self.icon = pyglet.image.load(f"{self.file_dir}/texture/cat1.jpg")
        arcade.get_window().set_icon(self.icon)

        self.levels = [
            level1,
            level2,
            level3,
            level4,
            level5,
            level6,
        ]

        # debug variable
        self.debugVal = 0
        self.debugMode = False  # Debug mode flag

        # set frame rate
        self.set_update_rate(1/60)

        # SCREEN DIMENSIONS
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        # Enable Timings for FPS
        arcade.enable_timings()
        # Set the window's position on the screen
        self.set_location(50, 50)  # X=100, Y=100
        # Enable depth testing
        self.ctx.enable(self.ctx.DEPTH_TEST)
        # Set blending mode
        self.ctx.enable(self.ctx.BLEND)
        # Set textures to None initially
        self.texture1 = None
        self.texture2 = None
        self.texture3 = None

        try:
            # Shader program for the object
            self.GLTF_program = self.ctx.program(
                vertex_shader="""
                #version 330

                uniform mat4 projection;
                uniform mat4 model;

                in vec3 in_pos;

                void main() {
                    // Apply the model and projection matrices
                    gl_Position = projection * model * vec4(in_pos, 1.0);
                }
                """,
                fragment_shader="""
                #version 330
                uniform vec4 base_color_factor;     // Base color (RGBA)
                out vec4 fragColor;

                void main() {
                    fragColor = base_color_factor;  // Set the fragment color
                }
                """
            )
        except Exception as e:
            print(f"Error creating shader program: {e}")

        self.line_program = self.ctx.program(
            vertex_shader="""
                #version 330
                uniform mat4 projection;
                uniform mat4 model;
                in vec3 in_pos;
                out float v_dist;
                void main() {
                    gl_Position = projection * model * vec4(in_pos, 1.0);
                    v_dist = gl_Position.z; // Pass depth for gradient
                }
            """,
            fragment_shader="""
                #version 330
                uniform vec3 color;
                out vec4 fragColor;
                void main() {
                    fragColor = vec4(color, 1.0);  // Set the color of the line
                }
            """
        )

        # Ground and wall shader program
        self.plane = self.ctx.program(
            vertex_shader="""
            #version 330

            uniform mat4 projection;
            uniform mat4 model;

            in vec3 in_pos;
            in vec2 in_uv;

            out vec2 uv;

            void main() {
                gl_Position = projection * model * vec4(in_pos, 1.0);
                uv = in_uv;
            }
            """,
            fragment_shader="""
            #version 330
            in vec2 uv;        // UV coordinates from the vertex shader
            out vec4 fragColor;

            uniform sampler2D texture;  // Texture sampler
            uniform float opacity;  // Opacity from the vertex shader
            
            void main() {
                // fragColor = texture2D(texture, uv);  // Sample the texture using UV coordinates
                vec4 tex = texture2D(texture, uv);
                tex.a *= opacity; // Apply opacity
                fragColor = tex;
            }
            """,
        )

        # Sphere shader program
        self.sphere_program = self.ctx.program(
            vertex_shader="""
            #version 330
            uniform mat4 projection;
            uniform mat4 model;
            in vec3 in_pos;
            in vec3 in_normal;
            in vec2 in_uv;
            out vec3 frag_pos;  // Pass the fragment position to the fragment shader
            out vec3 normal;    // Pass the normal to the fragment shader
            out vec2 uv;        // Pass the UV coordinates to the fragment shader
            out float local_y;

            void main() {
                frag_pos = (model * vec4(in_pos, 1.0)).xyz;
                normal = mat3(model) * in_normal;  // Transform the normal
                uv = in_uv;  // Pass UV coordinates
                local_y = in_pos.y;  // Pass the local Y position
                gl_Position = projection * model * vec4(in_pos, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            in vec3 frag_pos;
            in vec2 uv;
            in float local_y;  // Receive the local Y position
            uniform float time;  // <-- Add this line
            out vec4 fragColor;

            void main() {
                // Animate the gradient with time
                float t = clamp((local_y + 1.5 + sin(time)) / 4.0, 0.0, 1.0);
                vec3 color_bottom = vec3(0.09, 0.6, 0.8);
                vec3 color_top = vec3(1.0, 0.2, 0.8);
                vec3 color = mix(color_bottom, color_top, t);
                fragColor = vec4(color, 1.0);
            }
            """
        )

        self.game_music = arcade.load_sound(
            f"{self.file_dir}/sounds/game_music.mp3"
        )

        self.game_music.play(loop=True, volume=0.1)

        self.setup()

    def setup_textures(self):
        """
        Loads the textures and sets up the texture filtering mode to GL_NEAREST to remove blurriness.

        The textures are:
        - ground_texture: a grass texture
        - wall_texture: a dirt texture
        - cat_texture: a cat texture
        """

        ground_texture = arcade.load_texture(
            f"{self.file_dir}/texture/default.png"
        )
        wall_texture = arcade.load_texture(
            f"{self.file_dir}/texture/default2.png"
        )
        green_door_texture = arcade.load_texture(
            f"{self.file_dir}/texture/green_door.png"
        )
        red_door_texture = arcade.load_texture(
            f"{self.file_dir}/texture/red_door.png"
        )
        glass_texture = arcade.load_texture(
            f"{self.file_dir}/texture/glass.png"
        )

        self.texture1 = self.ctx.texture(
            size=(ground_texture.width, ground_texture.height),
            components=4,
            data=ground_texture.image.tobytes(),
        )
        self.texture2 = self.ctx.texture(
            size=(wall_texture.width, wall_texture.height),
            components=4,
            data=wall_texture.image.tobytes(),
        )
        self.texture3 = self.ctx.texture(
            size=(green_door_texture.width, green_door_texture.height),
            components=4,
            data=green_door_texture.image.tobytes(),
        )
        self.texture4 = self.ctx.texture(
            size=(red_door_texture.width, red_door_texture.height),
            components=4,
            data=red_door_texture.image.tobytes(),
        )
        self.texture5 = self.ctx.texture(
            size=(glass_texture.width, glass_texture.height),
            components=4,
            data=glass_texture.image.tobytes(),
        )

        # Set the texture filtering mode to GL_NEAREST to remove blurriness
        self.texture1.filter = self.ctx.NEAREST, self.ctx.NEAREST
        self.texture2.filter = self.ctx.NEAREST, self.ctx.NEAREST
        self.texture3.filter = self.ctx.NEAREST, self.ctx.NEAREST
        self.texture4.filter = self.ctx.NEAREST, self.ctx.NEAREST
        self.texture5.filter = self.ctx.NEAREST, self.ctx.NEAREST

    def setup(self):
        # Set the background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.fov = 90  # Field of view

        self.is_paused = False  # Flag to track if the game is paused

        # set up the player
        self.player = Player()  # Create a player instance

        # set up the ground
        self.proj = Mat4.perspective_projection(
            self.aspect_ratio, 0.01, 500, fov=self.fov,  # Set the field of view
        )
        # Set up the model matrix for the ground
        self.plane["projection"] = self.proj

        ground_array = array(
            'f',
            [
                # Position         UV
                -100, -2, 100,       0, 150,  # Top Left
                -100, -2, -200,      0, 0,   # Bottom Left
                100, -2, 100,        100, 150,  # Top Right
                100, -2, -200,       100, 0,  # Bottom Right
            ]
        )

        ceiling_array = array(
            'f',
            [
                # Position         UV
                -100, 6, 100,       0, 150,  # Top Left
                -100, 6, -200,      0, 0,   # Bottom Left
                100, 6, 100,        150, 150,  # Top Right
                100, 6, -200,       150, 0,  # Bottom Right
            ]
        )

        # Ground geometry
        ground_buffer = self.ctx.buffer(
            data=ground_array
        )

        ceiling_buffer = self.ctx.buffer(
            data=ceiling_array
        )

        # Create the ground geometry
        self.ground_geometry = self.ctx.geometry(
            content=[BufferDescription(
                ground_buffer, "3f 2f", ("in_pos", "in_uv"))],
            mode=self.ctx.TRIANGLE_STRIP,
        )
        self.ceiling_geometry = self.ctx.geometry(
            content=[BufferDescription(
                ceiling_buffer, "3f 2f", ("in_pos", "in_uv"))],
            mode=self.ctx.TRIANGLE_STRIP,
        )

        # Bind the ground texture to the shader program
        self.ground = self.plane
        self.ceiling = self.plane
        # set up Camera
        self.camera_pos = Vec3(0, -4, -5)
        self.camera_rot = Vec3(0, 0, 0)
        self.mouse_sensitivity = 0.001  # Lowered mouse sensitivity
        self.mouse_locked = True  # Mouse is initially locked
        self.set_mouse_visible(False)  # Hide the mouse cursor
        self.set_exclusive_mouse(True)  # Capture the mouse within the window

        # Initialize the list of objects
        self.objects = []

        # Bind the wall texture to the shader program
        self.wall = self.plane  # Use the same shader for walls

        self.enemy1_path = [f"{self.file_dir}/models/crazy_boy_noarm.gltf",
                            f"{self.file_dir}/models/crazy_boy_noarm.bin"]

        self.enemy2_path = [f"{self.file_dir}/models/tall_guy.gltf",
                            f"{self.file_dir}/models/tall_guy.bin"]

        self.button_path = [f"{self.file_dir}/models/button.gltf",
                            f"{self.file_dir}/models/button.bin"]

        self.miniboss1_path = [f"{self.file_dir}/models/miniboss_sword.gltf",
                               f"{self.file_dir}/models/miniboss_sword.bin"]

        self.miniboss2_path = [f"{self.file_dir}/models/miniboss_gun.gltf",
                               f"{self.file_dir}/models/miniboss_gun.bin"]

        self.final_boss_path = [f"{self.file_dir}/models/final_boss.gltf",
                                f"{self.file_dir}/models/final_boss.bin"]

        # Movement flags
        self.movement = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
        }

        # projectiles
        self.projectiles = []  # List to store projectiles

        # Money
        self.player_currency = self.player.currency  # Player's currency

        # Movement variables
        self.is_ADS = False  # Flag to track if the player is aiming down sights
        self.is_on_ground = False  # Flag to track if the player is on the ground
        self.vertical_velocity = 0  # Vertical velocity for jumping and gravity
        self.is_sliding = False  # Flag to track if the player is sliding
        self.slide_speed = 0.4  # Speed during the slide
        self.slide_duration = 0.4  # Duration of the slide in seconds
        self.slide_timer = 0  # Timer to track the slide duration
        self.slide_dir = Vec3(0, 0, 0)  # Direction of the slide
        self.default_speed = 2  # Default movement speed
        self.current_speed = 0.0  # Current movement speed
        self.max_speed = 0.5  # Maximum movement speed
        self.acceleration = 0.05  # Acceleration rate
        self.deceleration = 0.5  # Deceleration rate
        # shaking effect
        self.shake_intensity = 0  # Intensity of the shake
        self.shake_speed = 10.0  # Speed of the shake oscillation
        self.shake_decay = 0.9  # How quickly the shake effect decays
        # Direction of the shake (-1 for left, 1 for right)
        self.shake_direction = 0

        self.weapon_manager = weapons.WeaponManager(self)

        self.revolver_icon = arcade.load_texture(
            f"{self.file_dir}/model_ui/arsenal_icons/revolver_icon.png")

        self.shotgun_icon = arcade.load_texture(
            f"{self.file_dir}/model_ui/arsenal_icons/shotgun_icon.png")

        self.revolver_icon.filter = pyglet.gl.GL_NEAREST, pyglet.gl.GL_NEAREST
        self.shotgun_icon.filter = pyglet.gl.GL_NEAREST, pyglet.gl.GL_NEAREST

        self.hitmarker_timer = 0  # Timer for the hitmarker
        self.HS_hitmarker = False  # Flag for headshot hitmarker
        self.hitmarker = False  # Flag for hitmarker

        self.interactions = []  # List to store interactions with objects
        self.interaction_feedback = ""      # Message to show after interaction
        self.interaction_feedback_timer = 0  # Time until feedback disappears

        self.isLoaded = False  # Flag to check if the textures are loaded

        threading.Thread(target=self.weapon_manager.setup_weapon_textures,
                         daemon=True).start()

        # Set ammos
        self.revolver_max_ammo = 5  # Maximum ammo count
        self.shotgun_max_ammo = 4  # Maximum ammo count for shotgun

        self.cylinder_spin = 0  # Cylinder spin angle

        # Chamber state (1 for loaded, 0 for empty)
        self.chamber = [1] * self.revolver_max_ammo
        self.shell_holder = [1] * self.shotgun_max_ammo

        # set time
        self.time = 0  # UNIVERSAL TIME

        # set forward and right vectors
        self.forward = Vec3(0, 0, 0)  # Forward vector
        self.right = Vec3(0, 0, 0)  # Right vector

        # Each ray is (start: Vec3, end: Vec3, color: tuple)
        self.debug_rays = []

        # Persistent shop items for upgrades
        self.shop_items = [
            {"name": "Health +1", "base_price": 50, "price": 50, "count": 0},
            {"name": "REVOLVER DMG Up", "base_price": 100, "price": 100, "count": 0},
            {"name": "SHOTGUN DMG Up", "base_price": 100, "price": 100, "count": 0},
            {"name": "REVOLVER HS Mult Up", "base_price": 120, "price": 120, "count": 0},
            {"name": "SHOTGUN HS Mult Up", "base_price": 120, "price": 120, "count": 0},
        ]

        self.state = "TITLE"  # Add game state for title screen
        self.title_screen = TitleScreenView(self)
        self.shop_screen = ShopScreenView(self)
        self.selected_level = 1  # Default selected level for title/level select
        self.set_exclusive_mouse(False)

        
    def set_state(self, new_state):
        print(f"Changing state from {self.state} to {new_state}")
        self.state = new_state
        if new_state == "TITLE":
            self.mouse_locked = False
            self.set_exclusive_mouse(False)
        elif new_state == "GAME":
            self.mouse_locked = True
            self.set_exclusive_mouse(self.mouse_locked)
        elif new_state == "SHOP":
            self.mouse_locked = False
            self.set_exclusive_mouse(False)

    def draw_custom_cursor(self):
        # Only draw if not in exclusive mouse mode
        if getattr(self, 'mouse_locked', False):
            return
        x, y = self._last_mouse_pos if hasattr(self, '_last_mouse_pos') else (self.screen_width // 2, self.screen_height // 2)
        arcade.draw_circle_filled(x, y, 10, arcade.color.YELLOW)

    def on_draw(self):
        if self.state == "TITLE":
            self.title_screen.on_draw()
            # Draw custom cursor on title screen if not exclusive
            if not getattr(self, 'mouse_locked', False):
                if hasattr(self.title_screen, '_last_mouse_pos'):
                    x, y = self.title_screen._last_mouse_pos
                else:
                    x, y = self.screen_width // 2, self.screen_height // 2
                arcade.draw_circle_filled(x, y, 10, arcade.color.YELLOW)
            return
        if self.state == "SHOP":
            self.shop_screen.on_draw()
            return

        # Show mouse on title screen, hide otherwise (except loading/paused handled elsewhere)
        if self.state == "TITLE":
            self.clear()
            # Subtle animated background gradient (less colorful)
            for i in range(0, self.screen_height, 4):
                t = i / self.screen_height
                phase = self.time * 0.3
                gray = int(30 + 40 * (0.5 + 0.5 * math.sin(phase + t * 1.5)))
                arcade.draw_lrtb_rectangle_filled(
                    0, self.screen_width, self.screen_height -
                    i, self.screen_height - i - 4, (gray, gray, gray + 10)
                )

            # Animated title: fade in/out and slight vertical movement
            pulse = 0.5 + 0.5 * math.sin(self.time * 1.5)
            y_offset = int(10 * math.sin(self.time * 0.8))
            title_color = (180, 180, 200 + int(30 * pulse))
            font_size = 48 + int(4 * pulse)
            arcade.draw_text(
                "TERMINUS",
                self.screen_width // 2,
                self.screen_height // 2 + 60 + y_offset,
                title_color,
                font_size,
                anchor_x="center",
                anchor_y="center",
                bold=True,
                font_name="Kenney Future"
            )
            # --- Draw clickable Start button ---
            button_text = "Start Game"
            button_font_size = 20
            button_x = self.screen_width // 2
            button_y = self.screen_height // 2 - 40
            # Use arcade.create_text_image to get text size
            text_img = arcade.create_text_image(
                button_text, arcade.color.WHITE, button_font_size, font_name="Kenney Future")
            text_width, text_height = text_img.width, text_img.height
            button_w = text_width + 120
            button_h = text_height + 20
            self.title_button_rect = (
                button_x - button_w // 2, button_y - button_h // 2, button_w, button_h)
            # Detect hover/click color
            if self.title_button_pressed:
                color = arcade.color.RED
            elif self.title_button_hover:
                color = arcade.color.RED
            else:
                color = (180, 180, 200)
            # Draw button background (optional, subtle)
            arcade.draw_xywh_rectangle_filled(
                self.title_button_rect[0], self.title_button_rect[1], button_w, button_h, (
                    60, 60, 60, 80)
            )
            # Draw button border
            arcade.draw_xywh_rectangle_outline(
                self.title_button_rect[0], self.title_button_rect[1], button_w, button_h, color, 3
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
            
            self.level_select_rects = []
            levels = list(range(1, len(self.levels)+1))
            select_y = button_y - 160
            for i, lvl in enumerate(levels):
                rect_w = 50
                rect_h = 40
                rect_x = button_x + i*60 - (rect_w + 10)*len(levels) // 2
                rect_y = select_y
                rect = (rect_x, rect_y, rect_w, rect_h)
                self.level_select_rects.append((rect, lvl))
                color = arcade.color.YELLOW if self.selected_level == lvl else (
                    120, 120, 120)
                arcade.draw_xywh_rectangle_filled(
                    rect_x, rect_y, rect_w, rect_h, (40, 40, 40, 200))
                arcade.draw_xywh_rectangle_outline(
                    rect_x, rect_y, rect_w, rect_h, color, 3)
                arcade.draw_text(f"{lvl}", rect_x+rect_w//2, rect_y+rect_h//2, color,
                                18, anchor_x="center", anchor_y="center", font_name="Kenney Future")
            arcade.draw_text("Select Level", button_x, select_y+70, arcade.color.LIGHT_GRAY,
                            16, anchor_x="center", anchor_y="center", font_name="Kenney Future")
            return
        if self.texture1 is None or self.texture2 is None or self.texture3 is None:
            self.setup_textures()

        if not self.isLoaded:
            # draw loading screen
            arcade.draw_xywh_rectangle_filled(
                0, 0, self.screen_width, self.screen_height, arcade.color.BLACK)
            # Draw loading bar
            loading_bar_width = (
                self.weapon_manager.currentLoading / self.weapon_manager.totalLoading)
            arcade.draw_text(f"Loading textures... {self.weapon_manager.currentLoading}/{self.weapon_manager.totalLoading} ({loading_bar_width * 100:.2f}%)",
                             self.screen_width // 2, self.screen_height // 3, arcade.color.WHITE, 12, anchor_x="center", anchor_y="center")
            # draw outline
            arcade.draw_xywh_rectangle_outline(
                self.screen_width // 2 - 100, self.screen_height // 2 - 10, 200, 20, arcade.color.WHITE, 2)
            arcade.draw_xywh_rectangle_filled(
                self.screen_width // 2 - 100, self.screen_height // 2 - 10, 200 * loading_bar_width, 20, arcade.color.WHITE)
            return  # Exit the draw method if textures are not loaded

        self.clear()
        self.ctx.enable(self.ctx.DEPTH_TEST)  # Ensure depth testing is enabled

        # Define rotation matrices for the camera
        translate = Mat4.from_translation(self.camera_pos)
        rotate_x = Mat4.from_rotation(self.camera_rot.x, (1, 0, 0))
        rotate_y = Mat4.from_rotation(self.camera_rot.y, (0, 1, 0))
        rotate_z = Mat4.from_rotation(self.camera_rot.z, (0, 0, 1))

        # FOV update
        self.proj = Mat4.perspective_projection(
            self.aspect_ratio, 0.01, 500, fov=self.fov,  # Set the field of view
        )
        self.plane["projection"] = self.proj
        self.sphere_program["projection"] = self.proj
        self.GLTF_program["projection"] = self.proj

        # Bind the ground texture before rendering the ground
        self.texture1.use(0)
        self.ground["texture"] = 0
        self.ground["opacity"] = 1.0
        self.ceiling["texture"] = 0

        # Render the ground
        self.ground["model"] = translate @ rotate_y @ rotate_x @ rotate_z
        self.ground_geometry.render(self.ground)
        # Render the ceiling
        self.ceiling["model"] = translate @ rotate_y @ rotate_x @ rotate_z
        self.ceiling_geometry.render(self.ceiling)

        # Sort walls and projectiles by distance from the player (nearest first)
        self.objects.sort(key=self.get_distance, reverse=True)
        # Render the objects
        for obj in self.objects:
            if obj["id"] == 1:
                # Bind the wall texture to the shader program
                self.texture2.use(1)
                self.texture5.use(5)
                obj["program"]["texture"] = obj["texture"]
                obj["program"]["opacity"] = obj["opacity"]
                obj["program"]["model"] = translate @ rotate_y @ rotate_x @ rotate_z
                obj["geometry"].render(obj["program"])
            elif obj["id"] == 2:
                # Bind the wall texture to the shader program
                self.texture3.use(3)
                self.texture4.use(4)
                obj["program"]["texture"] = obj["texture"]
                obj["program"]["opacity"] = obj["opacity"]
                obj["program"]["model"] = translate @ rotate_y @ rotate_x @ rotate_z
                obj["geometry"].render(obj["program"])
            elif obj["id"] == 3:
                # Render the exit portal
                # self.time is your game's running time
                self.exit_portal["program"]["time"] = self.time * 2
                self.exit_portal["program"]["projection"] = self.proj
                self.exit_portal["program"]["model"] = translate @ rotate_y @ rotate_x @ rotate_z
                obj["geometry"].render(
                    self.exit_portal["program"])
            elif obj["id"] == 4:
                # Render projectiles relative to player and camera rotation
                obj["program"]["projection"] = self.proj
                obj["program"]["model"] = (
                    translate @ Mat4.from_translation(Vec3(
                        obj["model"].x, obj["model"].y, obj["model"].z)) @ rotate_y @ rotate_x @ rotate_z
                )
                obj["geometry"].render(obj["program"])

            # Render the enemy object
            elif obj["id"] == 10:  # Render enemy objects
                # Bind the GLTF program
                obj["program"]["projection"] = self.proj

                if obj["type"] == 4:
                    # For minibosses, use the miniboss shader program
                    if obj["object"].get_form() == 1:  # If the miniboss is a sword miniboss
                        geometry = obj["geometry"][0]
                    elif obj["object"].get_form() == 2:  # If the miniboss is a gun miniboss
                        geometry = obj["geometry"][1]
                else:
                    geometry = obj["geometry"]

                # Rotate the object around the Y-axis
                object_rotation_matrix = (Mat4.from_rotation(
                    obj["object"].get_rotation().y, (0, 1, 0)) - Mat4.from_translation(Vec3(0, 0, 0)))  # Rotate around Y-axis

                translation = (Mat4.from_translation(
                    self.camera_pos) @ Mat4.from_translation(obj["object"].get_world_position()))  # Get the world position of the object

                # Final model matrix
                obj["program"]["model"] = (
                    # Apply camera rotation
                    (translation + object_rotation_matrix)
                    @ (rotate_y @ rotate_x @ rotate_z))

                for i, enemy_geometry in enumerate(geometry):

                    obj["program"]["base_color_factor"] = enemy_geometry["base_color_factor"]

                    # Set material properties
                    if i == 0 and (obj["type"] == 3):
                        # For enemy3, use the special shader program
                        obj["program"]["base_color_factor"] = (
                            0.6, 0.1, 0.1, 1.0)  # Red color

                    # Render the geometry
                    enemy_geometry["geometry"].render(obj["program"])

            elif obj["id"] == 20:  # Render buttons (general GLTF objects)
                # Bind the GLTF program
                obj["program"]["projection"] = self.proj

                # Rotate the object around the Y-axis
                object_rotation_matrix = (Mat4.from_rotation(
                    obj["rotation"].y, (0, 1, 0)) - Mat4.from_translation(Vec3(0, 0, 0)))  # Rotate around Y-axis

                translation = (Mat4.from_translation(
                    self.camera_pos) @ Mat4.from_translation(obj["position"]))  # Get the world position of the object

                # Final model matrix
                obj["program"]["model"] = (
                    # Apply camera rotation
                    (translation + object_rotation_matrix)
                    @ (rotate_y @ rotate_x @ rotate_z))

                for i, button_geometry in enumerate(obj["geometry"]):
                    # Set material properties
                    obj["program"]["base_color_factor"] = button_geometry["base_color_factor"]

                    # Render the geometry
                    button_geometry["geometry"].render(obj["program"])

        for ray_start, ray_end, color, timestamp in self.debug_rays:
            # Create a buffer for the line's two endpoints
            line_buffer = self.ctx.buffer(data=array('f', [
                ray_start.x, ray_start.y, ray_start.z,
                ray_end.x, ray_end.y, ray_end.z,
            ]))
            line_geometry = self.ctx.geometry(
                content=[BufferDescription(line_buffer, "3f", ("in_pos",))],
                mode=self.ctx.LINES,
            )
            self.line_program["projection"] = self.proj
            # Identity
            self.line_program["model"] = translate @ rotate_y @ rotate_x @ rotate_z
            self.line_program["color"] = color  # Set the color for the line
            line_geometry.render(self.line_program)
            # remove the exprired rays
            # if self.time - timestamp > 0.5:  # Remove rays older than 0.5 seconds
            #     self.debug_rays.remove((ray_start, ray_end, color, timestamp))

        # draw UI
        self.draw_UI()

        # Draw pause overlay if paused
        if self.is_paused:
            arcade.draw_lrtb_rectangle_filled(
                0, self.screen_width, self.screen_height, 0, (0, 0, 0, 180)
            )
            arcade.draw_text(
                "PAUSED",
                self.screen_width // 2,
                self.screen_height // 2,
                arcade.color.WHITE,
                48,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )
            arcade.draw_text(
                "Press R to Retry | T for Title | Q to Exit | ESC to Resume",
                self.screen_width // 2,
                self.screen_height // 2 - 60,
                arcade.color.LIGHT_GRAY,
                20,
                anchor_x="center",
                anchor_y="center",
            )
            # Draw custom cursor in pause menu if not exclusive
            self.draw_custom_cursor()
            return  # Skip drawing the rest of the game when paused

        # Death screen
        if hasattr(self.player, "health") and self.player.health <= 0:
            self.clear()
            arcade.draw_lrtb_rectangle_filled(
                0, self.screen_width, self.screen_height, 0, (0, 0, 0, 220)
            )
            arcade.draw_text(
                "YOU DIED",
                self.screen_width // 2,
                self.screen_height // 2 + 40,
                arcade.color.RED,
                56,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )
            arcade.draw_text(
                "Press R to Retry | T for Title | Q to Exit",
                self.screen_width // 2,
                self.screen_height // 2 - 40,
                arcade.color.LIGHT_GRAY,
                24,
                anchor_x="center",
                anchor_y="center",
            )
            # Draw custom cursor in death screen if not exclusive
            self.draw_custom_cursor()
            return
        # Boss dead: end game and go to win screen, wait for SPACE to return to title
        finalbosses = [enemy["object"] for enemy in self.enemies if hasattr(
            enemy["object"], "__class__") and enemy["object"].__class__.__name__ == "FinalBoss" and enemy.get("spawned")]
        if self.state == "WIN":
            # Only show win screen, do not reset state here
            self.clear()
            arcade.draw_lrtb_rectangle_filled(
                0, self.screen_width, self.screen_height, 0, (0, 0, 0, 220)
            )
            arcade.draw_text(
                "YOU WIN!",
                self.screen_width // 2,
                self.screen_height // 2 + 80,
                arcade.color.GREEN,
                56,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )
            arcade.draw_text(
                "You have terminated the host computer and successfully completed your mission.",
                self.screen_width // 2,
                self.screen_height // 2,
                arcade.color.WHITE,
                20,
                anchor_x="center",
                anchor_y="center",
                bold=True,
                width=self.screen_width // 2,
            )
            arcade.draw_text(
                "Press ENTER to return to Title",
                self.screen_width // 2,
                self.screen_height // 2 - 80,
                arcade.color.LIGHT_GRAY,
                24,
                anchor_x="center",
                anchor_y="center",
            )
            return
        if finalbosses and all(boss.is_dead() for boss in finalbosses):
            self.state = "WIN"
            self.activated_rooms.clear()
            self.enemies.clear()
            self.objects.clear()
            self.player.health = self.player.max_health
            self.camera_pos = Vec3(0, -4, -5)
            self.camera_rot = Vec3(0, 0, 0)
            return
        # ...existing code...

    def draw_UI(self):
        try:

            self.weapon_manager.draw()

            # ======================CROSSHAIR====================== #

            # draw crosshair that has inverse color from the background
            # Capture the screen and get the color at the center
            screen_image = arcade.get_image()
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            pixel_color = screen_image.getpixel(
                (center_x, center_y))  # Get the color at the center

            # Calculate the inverse color
            inverse_color = (
                255 - pixel_color[0], 255 - pixel_color[1], 255 - pixel_color[2])

            # Draw the crosshair
            crosshair_size = 5  # Size of the crosshair
            line_thickness = 2  # Thickness of the crosshair lines

            # Horizontal line
            arcade.draw_line(
                center_x - crosshair_size, center_y,
                center_x + crosshair_size, center_y,
                inverse_color, line_thickness
            )

            # Vertical line
            arcade.draw_line(
                center_x, center_y - crosshair_size,
                center_x, center_y + crosshair_size,
                inverse_color, line_thickness
            )

            # HITMARKER
            if self.HS_hitmarker:
                # Draw hitmarker at the center of the screen
                hitmarker_size = 8
                hitmarker_thickness = 2
                offset = 3  # Offset for the hitmarker lines
                color = arcade.color.RED  # Color of the hitmarker
            elif self.hitmarker:
                # Draw hitmarker at the center of the screen
                hitmarker_size = 5
                hitmarker_thickness = 2
                offset = 3  # Offset for the hitmarker lines
                color = arcade.color.GRAY  # Color of the hitmarker
            if self.HS_hitmarker or self.hitmarker:
                # FOUR LINES FOR HITMARKER
                # Top left
                arcade.draw_line(
                    center_x - hitmarker_size - offset, center_y + hitmarker_size + offset,
                    center_x - offset, center_y + offset,
                    color, hitmarker_thickness
                )
                # Bottom left
                arcade.draw_line(
                    center_x - hitmarker_size - offset, center_y - hitmarker_size - offset,
                    center_x - offset, center_y - offset,
                    color, hitmarker_thickness
                )
                # Bottom right
                arcade.draw_line(
                    center_x + hitmarker_size + offset, center_y - hitmarker_size - offset,
                    center_x + offset, center_y - offset,
                    color, hitmarker_thickness
                )
                # Top right
                arcade.draw_line(
                    center_x + hitmarker_size + offset, center_y + hitmarker_size + offset,
                    center_x + offset, center_y + offset,
                    color, hitmarker_thickness
                )

            # ======================INTERACTIONS========================== #
            if len(self.interactions) > 0:
                if self.interactions[0]["active"]:
                    # Draw a brighter, more visible rectangle with a border
                    arcade.draw_xywh_rectangle_filled(
                        self.screen_width // 2 - 110,
                        self.screen_height // 2 - 110 - 30,
                        240,
                        60,
                        (30, 30, 30, 200)  # More opaque and darker
                    )
                    arcade.draw_xywh_rectangle_outline(
                        self.screen_width // 2 - 110,
                        self.screen_height // 2 - 110 - 30,
                        240,
                        60,
                        arcade.color.YELLOW,
                        3
                    )
                    arcade.draw_text(
                        "Press E to interact",
                        self.screen_width // 2 + 10,
                        self.screen_height // 2 - 75 - 30,
                        arcade.color.WHITE,
                        10,
                        font_name="Kenney Future",
                        anchor_x="center",
                        anchor_y="center",
                        bold=True
                    )

            # ========================INFO========================== #
            # display health bar
            bar_w = self.screen_width // 8
            bar_h = self.screen_height // 14
            bar_x = self.screen_width // 2
            bar_y = self.screen_height // 32
            # Draw the background ellipse
            arcade.draw_ellipse_filled(bar_x, bar_y + 10, bar_w, bar_h, arcade.color.DARK_GRAY)
            arcade.draw_text("Health", bar_x, self.screen_height // 16,
                             arcade.color.BLACK, 12, font_name="Kenney Future", anchor_x="center", anchor_y="center", bold=True)
            # Draw the filled health bar (more segments, same overall size)
            segment_count = max(self.player.max_health, 5)  # At least 10 segments for smoothness
            segment_gap = 2
            segment_w = (bar_w - (segment_count - 1) * segment_gap) / segment_count
            segment_h = bar_h * 0.5
            start_x = bar_x - bar_w // 2 + segment_w // 2
            arcade.draw_rectangle_filled(bar_x, self.screen_height // 36, bar_w, bar_h * 0.5, arcade.color.BLACK)
            for i in range(segment_count):
                seg_x = start_x + i * (segment_w + segment_gap)
                color = arcade.color.RED if i < self.player.health else arcade.color.GRAY
                arcade.draw_rectangle_filled(seg_x, bar_y, segment_w, segment_h, color)
            arcade.draw_rectangle_outline(bar_x, self.screen_height // 36, bar_w, bar_h * 0.5, arcade.color.BLACK, 4)

            # display currency
            arcade.draw_ellipse_filled(
                self.screen_width // 3, self.screen_height // 22, self.screen_width // 8, self.screen_height // 14, arcade.color.DARK_GRAY)
            arcade.draw_text(f"Currency: {self.player.currency}", self.screen_width // 3, self.screen_height // 22,
                             arcade.color.GREEN, 12, font_name="Kenney Future", anchor_x="center", anchor_y="center", bold=True)
            # ======================MINIBOSS HEALTH====================== #
            minibosses = [enemy["object"] for enemy in self.enemies if hasattr(
                enemy["object"], "__class__") and enemy["object"].__class__.__name__ == "Miniboss" and not enemy["object"].is_dead() and enemy.get("spawned")]  # Only show if spawned
            if minibosses:
                miniboss = minibosses[0]  # Show the first alive miniboss
                bar_w = self.screen_width // 2
                bar_h = 32
                bar_x = self.screen_width // 2 - bar_w // 2
                bar_y = self.screen_height - 60
                # Background
                arcade.draw_xywh_rectangle_filled(
                    bar_x, bar_y, bar_w, bar_h, (40, 0, 0, 200))
                # Health
                health_ratio = miniboss.health / miniboss.max_health
                arcade.draw_xywh_rectangle_filled(bar_x, bar_y, int(
                    bar_w * health_ratio), bar_h, arcade.color.RED)
                # Border
                arcade.draw_xywh_rectangle_outline(
                    bar_x, bar_y, bar_w, bar_h, arcade.color.BLACK, 4)
                # Text
                arcade.draw_text(f"MINIBOSS HP: {miniboss.health:.0f} / {miniboss.max_health}",
                                 self.screen_width // 2, bar_y + bar_h // 2,
                                 arcade.color.WHITE, 18, anchor_x="center", anchor_y="center", bold=True)

            # ======================FINALBOSS HEALTH====================== #
            finalbosses = [enemy["object"] for enemy in self.enemies if hasattr(
                enemy["object"], "__class__") and enemy["object"].__class__.__name__ == "FinalBoss" and not enemy["object"].is_dead() and enemy.get("spawned")]  # Only show if spawned
            if finalbosses:
                finalboss = finalbosses[0]  # Show the first alive final boss
                bar_w = self.screen_width // 2
                bar_h = 36
                bar_x = self.screen_width // 2 - bar_w // 2
                bar_y = self.screen_height - 110
                # Draw 3 phase segments (backgrounds)
                phase1_w = int(bar_w * (1/3))
                phase2_w = int(bar_w * (1/3))
                phase3_w = bar_w - phase1_w - phase2_w
                # Phase backgrounds
                arcade.draw_xywh_rectangle_filled(
                    bar_x, bar_y, phase1_w, bar_h, (60, 0, 0, 180))
                arcade.draw_xywh_rectangle_filled(
                    bar_x + phase1_w, bar_y, phase2_w, bar_h, (60, 30, 0, 180))
                arcade.draw_xywh_rectangle_filled(
                    bar_x + phase1_w + phase2_w, bar_y, phase3_w, bar_h, (0, 40, 80, 180))
                # Health overlay (color by phase)
                health_ratio = finalboss.health / finalboss.max_health
                if finalboss.phase == 1:
                    color = arcade.color.RED
                elif finalboss.phase == 2:
                    color = arcade.color.ORANGE
                else:
                    color = arcade.color.BLUE
                arcade.draw_xywh_rectangle_filled(
                    bar_x, bar_y, int(bar_w * health_ratio), bar_h, color)
                # Border
                arcade.draw_xywh_rectangle_outline(
                    bar_x, bar_y, bar_w, bar_h, arcade.color.BLACK, 4)
                # Phase dividers
                arcade.draw_line(bar_x + phase1_w, bar_y, bar_x +
                                 phase1_w, bar_y + bar_h, arcade.color.BLACK, 3)
                arcade.draw_line(bar_x + phase1_w + phase2_w, bar_y, bar_x +
                                 phase1_w + phase2_w, bar_y + bar_h, arcade.color.BLACK, 3)
                # Text
                arcade.draw_text(f"FINAL BOSS PHASE {finalboss.phase} HP: {finalboss.health:.0f} / {finalboss.max_health}",
                                 self.screen_width // 2, bar_y + bar_h // 2,
                                 arcade.color.WHITE, 20, anchor_x="center", anchor_y="center", bold=True)

            # ========================GAME_INFO========================== #

            # Display camera position
            arcade.draw_text(
                f"Camera Position: ({-self.camera_pos.x:.6f}, {-self.camera_pos.y:.6f}, {-self.camera_pos.z:.6f})",
                10,
                self.screen_height - 20,
                arcade.color.WHITE,
                12,
            )
            # Display camera position
            arcade.draw_text(
                f"Camera Rotation: ({self.camera_rot.x:.6f}, {self.camera_rot.y:.6f}, {self.camera_rot.z:.6f})",
                10,
                self.screen_height - 40,
                arcade.color.WHITE,
                12,
            )
            # Display camera position
            arcade.draw_text(
                f"Is Grounded: {self.is_on_ground}",
                10,
                self.screen_height - 60,
                arcade.color.WHITE,
                12,
            )
            # Display FPS
            arcade.draw_text(
                f"FPS: {arcade.get_fps():.2f}",
                self.screen_width - 100,
                self.screen_height - 20,
                arcade.color.WHITE,
                12,
            )
            # display time
            arcade.draw_text(
                f"Time: {self.time:.2f}",
                self.screen_width - 100,
                self.screen_height - 40,
                arcade.color.WHITE,
                12,
            )

            # Display Current Speed (Acceleration)
            arcade.draw_text(
                f"Current Speed: {self.current_speed:.2f}",
                10,
                self.screen_height - 80,
                arcade.color.WHITE,
                12,
            )

            # is ads
            arcade.draw_text(
                f"Is ADS: {self.is_ADS}",
                10,
                self.screen_height - 100,
                arcade.color.WHITE,
                12,
            )
        except Exception as e:
            print(f"Error drawing texture: {e}")

    def on_update(self, delta_time: float):
        # Always update time, even on title screen
        self.time += delta_time
        if self.state == "TITLE":
            self.title_screen.on_update(delta_time)
            return  # Skip updating the game when on the title screen
        if self.state == "SHOP":
            self.shop_screen.on_update(delta_time)
            return  # Skip updating the game when in the shop

        if self.is_paused:
            return  # Skip updating the game when paused

        if not self.weapon_manager.isLoaded:
            # If textures are not loaded, skip the update
            return
        elif not self.isLoaded:
            self.isLoaded = True

        # Update object list
        self.objects.sort(key=self.get_distance, reverse=True)

        # set mouse active
        self.set_exclusive_mouse(self.mouse_locked)

        # Check for player collision with room triggers (AABB, with z thickness)
        for trigger in getattr(self, 'room_triggers', []):
            positions = trigger["buffer_data"]
            num_vertices = len(positions) // 5
            min_x = min(positions[i * 5] for i in range(num_vertices))
            max_x = max(positions[i * 5] for i in range(num_vertices))
            min_y = min(positions[i * 5 + 1] for i in range(num_vertices))
            max_y = max(positions[i * 5 + 1] for i in range(num_vertices))
            min_z = min(positions[i * 5 + 2] for i in range(num_vertices))
            max_z = max(positions[i * 5 + 2] for i in range(num_vertices))
            # Expand z bounds for a thicker trigger box
            min_z -= 2
            max_z += 2
            # Player position (camera)
            px, py, pz = -self.camera_pos.x, -self.camera_pos.y, -self.camera_pos.z
            # Simple AABB check
            if (min_x <= px <= max_x and min_y <= py <= max_y and min_z <= pz <= max_z):
                print(
                    f"Player entered trigger {trigger['name']} for room {trigger.get('room', 1)} at pos ({px:.2f},{py:.2f},{pz:.2f})")
                room_num = trigger.get("room", 1)
                if room_num not in self.activated_rooms:
                    print(f"Activating room {room_num}")
                    self.activate_room(room_num)
                    self.activated_rooms.add(room_num)

        enemy_count = 0  # Count the number of enemies
        for obj in self.objects:
            if obj["id"] == 10:
                obj["object"].move(-self.camera_pos, self.enemies)
                if obj["object"].is_dead():
                    self.objects.remove(obj)
                else:
                    enemy_count += 1

        try:
            # Check if all enemies are dead
            room1_dead = (1 in self.activated_rooms) and all(
                enemy["object"].is_dead() for enemy in self.enemies if enemy.get("room", 0) == 1
            )
            room2_dead = (2 in self.activated_rooms) and all(
                enemy["object"].is_dead() for enemy in self.enemies if enemy.get("room", 0) == 2
            )
            room3_dead = (3 in self.activated_rooms) and all(
                enemy["object"].is_dead() for enemy in self.enemies if enemy.get("room", 0) == 3
            )
            room4_dead = (4 in self.activated_rooms) and all(
                enemy["object"].is_dead() for enemy in self.enemies if enemy.get("room", 0) == 4
            )
            # print(f"Enemies in Room 1 Dead: {room1_dead}, Room 2 Dead: {room2_dead}, Room 3 Dead: {room3_dead}, Room 4 Dead: {room4_dead}")
            # If all enemies in a room are dead, unlock the doors

            for door in self.doors:
                try:
                    if room1_dead and door["condition"] == "room1_dead":
                        door["lock"] = False
                        door["opacity"] = 0.5

                    elif room2_dead and door["condition"] == "room2_dead":
                        door["lock"] = False
                        door["opacity"] = 0.5

                    elif room3_dead and door["condition"] == "room3_dead":
                        door["lock"] = False
                        door["opacity"] = 0.5

                    elif room4_dead and door["condition"] == "room4_dead":
                        door["lock"] = False
                        door["opacity"] = 0.5
                except KeyError:
                    # If the door does not have a condition, skip it
                    continue
        except Exception as e:
            pass  # Ignore errors if no enemies are present

        # if close to a button, add it to the interactions list
        for obj in self.objects:
            if obj["id"] == 20:
                distance = math.sqrt(
                    (obj["position"].x + self.camera_pos.x) ** 2 +
                    (obj["position"].y + self.camera_pos.y) ** 2 +
                    (obj["position"].z + self.camera_pos.z) ** 2
                )
                if distance < 3 and obj not in self.interactions and obj["active"]:
                    self.interactions.append(obj)
                elif distance >= 3 and obj in self.interactions:
                    self.interactions.remove(obj)

        if self.is_ADS:
            # Zoom in
            if self.fov > 70:
                self.fov -= 3
            self.mouse_sensitivity = 0.0005
        else:
            if self.fov < 90:
                # Zoom out
                self.fov += 3
            self.mouse_sensitivity = 0.001

        if self.HS_hitmarker:
            if self.hitmarker_timer <= self.time:
                self.HS_hitmarker = False
                self.hitmarker_timer = 0  # Reset the hitmarker timer
        elif self.hitmarker:
            if self.hitmarker_timer <= self.time:
                self.hitmarker = False
                self.hitmarker_timer = 0  # Reset the hitmarker timer

        self.weapon_manager.update(delta_time)

        for obj in self.objects:
            if obj["id"] == 4:
                # Update the projectile's position based on its velocity
                obj["model"] = obj["model"] + obj["velocity"]
                # Check collision with player (simple sphere distance check)
                player_world_pos = -self.camera_pos
                proj_pos = obj["model"]
                distance = math.sqrt(
                    (player_world_pos.x - proj_pos.x) ** 2 +
                    (player_world_pos.y - proj_pos.y) ** 2 +
                    (player_world_pos.z - proj_pos.z) ** 2
                )
                if distance < 1.0:  # Adjust radius as needed
                    self.player.apply_damage(1)  # Deal 1 damage
                    self.objects.remove(obj)
                    continue
                # Check if the projectile is out of bounds and remove it
                if (obj["model"].x < -200 or obj["model"].x > 200 or
                        obj["model"].y < -200 or obj["model"].y > 200 or
                        obj["model"].z < -200 or obj["model"].z > 200) or obj["model"].y < -2:
                    self.objects.remove(obj)
            elif obj["id"] == 10:  # Assuming this is the enemy object

                # Calculate the direction vector from the enemy to the player
                enemy_position = obj["object"].get_world_position()
                direction = Vec3(
                    -self.camera_pos.x - enemy_position.x,
                    0,  # Ignore the Y-axis for horizontal rotation
                    -self.camera_pos.z - enemy_position.z
                )

                # Normalize the direction vector
                direction = direction.normalize()

                # Calculate the yaw (rotation around the Y-axis)
                yaw = math.atan2(direction.x, direction.z)

                # Update the enemy's rotation
                obj["object"].rotation.y = yaw  # Convert to degrees

        # check if player walks into a exit portal
        portal_radius = 2.0  # Define the radius of the exit portal
        if self.exit_portal and self.exit_portal["id"] == 3:
            distance_to_exit = math.sqrt(
                (self.camera_pos.x + self.exit_portal["model"].x) ** 2 +
                (self.camera_pos.y + self.exit_portal["model"].y) ** 2 +
                (self.camera_pos.z + self.exit_portal["model"].z) ** 2
            )
            if distance_to_exit < portal_radius:
                # Player has entered the exit portal
                print("You have exited the level!")
                # Use destination if present, otherwise default to next level
                dest = self.exit_portal.get("destination")
                if dest is not None:
                    self.change_level(dest)
                else:
                    self.exit_level()

        rotation_y = self.camera_rot.y

        # Forward vector (affects x and z based on yaw)
        forward_x = -math.sin(rotation_y)
        forward_z = math.cos(rotation_y)

        # Right vector (perpendicular to forward in the horizontal plane)
        right_x = math.cos(rotation_y)
        right_z = math.sin(rotation_y)

        # Set the forward and right vectors to the camera's rotation
        self.forward = Vec3(forward_x, 0, forward_z)
        self.right = Vec3(right_x, 0, right_z)

        # Movement logic
        self.movement_vector = Vec3(0, 0, 0)  # Initialize movement vector
        if self.movement["forward"]:  # Move forward
            self.movement_vector += self.forward
        if self.movement["backward"]:  # Move backward
            self.movement_vector -= self.forward
        if self.movement["left"]:  # Move left
            self.movement_vector += self.right
        if self.movement["right"]:  # Move right
            self.movement_vector -= self.right

        # Normalize the movement vector to ensure consistent speed
        if self.movement_vector.mag > 0:
            # Normalize the movement vector and Accelerate
            if self.is_on_ground and not self.is_sliding:
                self.current_speed -= (self.deceleration *
                                       delta_time) * 0.5  # Decelerate
            else:
                self.current_speed += (self.acceleration *
                                       delta_time)  # Accelerate
            if self.current_speed > self.max_speed:
                self.current_speed = self.max_speed  # Cap the speed
            self.movement_vector = self.movement_vector.normalize().scale(self.current_speed + 0.3)
            if self.current_speed < 0:
                self.current_speed = 0  # Prevent negative speed
        else:
            # Decelerate if no movement keys are pressed
            self.current_speed -= self.deceleration * delta_time
            if self.current_speed < 0:
                self.current_speed = 0  # Prevent negative speed

        # Calculate movement magnitude
        movement_magnitude = self.movement_vector.mag

        # Start shaking if the movement magnitude is large enough
        if movement_magnitude > 0.1 and self.camera_pos.y >= 0:
            self.shake_intensity = 0.01  # Scale shake intensity
            if self.movement["left"]:
                self.shake_direction = -1  # Shake to the left
            elif self.movement["right"]:
                self.shake_direction = 1  # Shake to the right

        # Apply smooth shake effect using a sine wave
        if self.shake_intensity > 0:
            self.camera_rot.z = math.sin(
                time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction
            self.shake_intensity *= self.shake_decay  # Decay the shake intensity over time
        else:
            self.camera_rot.z = 0  # Reset Z rotation when shake ends

        # Handle sliding
        if self.is_sliding:
            self.movement_vector = self.slide_dir.normalize().scale(
                self.slide_speed + self.current_speed)
            self.slide_speed -= self.deceleration * \
                delta_time * 0.5  # Decrease slide speed over time
            if self.current_speed < self.max_speed // 2:
                self.current_speed += self.acceleration * delta_time
            if self.slide_speed < 0:
                self.slide_speed = 0  # Prevent negative slide speed
        else:
            self.slide_speed = 0.4  # Reset slide speed when not sliding

        # Improved collision detection logic to adjust movement vector dynamically
        camera_radius = 1  # Define the radius of the camera's collision sphere

        # Sort walls by distance from the camera and take the first 10 closest walls
        closest_walls = sorted(self.walls, key=self.get_distance)[:5]
        for wall in closest_walls:
            positions = wall["buffer_data"]
            num_vertices = len(positions) // 5

            # Calculate the bounding box of the wall
            min_x = min(positions[i * 5] for i in range(num_vertices))
            max_x = max(positions[i * 5] for i in range(num_vertices))
            min_y = min(positions[i * 5 + 1] for i in range(num_vertices))
            max_y = max(positions[i * 5 + 1] for i in range(num_vertices))
            min_z = min(positions[i * 5 + 2] for i in range(num_vertices))
            max_z = max(positions[i * 5 + 2] for i in range(num_vertices))

            # Check for overlap between the camera sphere and the wall's bounding box
            closest_x = max(min_x, min(-self.camera_pos.x, max_x))
            closest_y = max(min_y, min(-self.camera_pos.y, max_y))
            closest_z = max(min_z, min(-self.camera_pos.z, max_z))

            distance_x = -self.camera_pos.x - closest_x
            distance_y = -self.camera_pos.y - closest_y
            distance_z = -self.camera_pos.z - closest_z

            distance = math.sqrt(
                distance_x ** 2 + distance_y ** 2 + distance_z ** 2)

            if distance < camera_radius:
                # Calculate the normal of the wall's surface
                normal = Vec3(distance_x, distance_y, distance_z).normalize()

                # Adjust movement vector to slide along the wall
                dot_product = self.movement_vector.dot(normal)
                if dot_product > 0:
                    # Calculate the projection of the movement vector onto the wall's normal
                    self.movement_vector -= normal.scale(abs(dot_product))
                    # Apply deceleration to the current speed
                    self.current_speed -= self.deceleration * delta_time * 0.1
                    if self.current_speed < 0:
                        self.current_speed = 0  # Prevent negative speed

                if distance < 0.3:
                    # Push the camera slightly out of the wall to avoid getting stuck
                    overlap = camera_radius - distance - 5
                    self.camera_pos += normal.scale(overlap * 0.001)
                # Push the camera slightly out of the wall to avoid getting stuck
                overlap = camera_radius - distance
                self.camera_pos += normal.scale(overlap * 0.001)

        for door in self.doors:
            if door["lock"]:
                positions = door["buffer_data"]
                num_vertices = len(positions) // 5

                # Calculate the bounding box of the door
                min_x = min(positions[i * 5] for i in range(num_vertices))
                max_x = max(positions[i * 5] for i in range(num_vertices))
                min_y = min(positions[i * 5 + 1] for i in range(num_vertices))
                max_y = max(positions[i * 5 + 1] for i in range(num_vertices))
                min_z = min(positions[i * 5 + 2] for i in range(num_vertices))
                max_z = max(positions[i * 5 + 2] for i in range(num_vertices))

                # Check for overlap between the camera sphere and the door's bounding box
                closest_x = max(min_x, min(-self.camera_pos.x, max_x))
                closest_y = max(min_y, min(-self.camera_pos.y, max_y))
                closest_z = max(min_z, min(-self.camera_pos.z, max_z))

                distance_x = -self.camera_pos.x - closest_x
                distance_y = -self.camera_pos.y - closest_y
                distance_z = -self.camera_pos.z - closest_z

                distance = math.sqrt(
                    distance_x ** 2 + distance_y ** 2 + distance_z ** 2)

                if distance < camera_radius:
                    # Calculate the normal of the wall's surface
                    normal = Vec3(distance_x, distance_y,
                                  distance_z).normalize()

                    # Adjust movement vector to slide along the wall
                    dot_product = self.movement_vector.dot(normal)
                    if dot_product > 0:
                        # Calculate the projection of the movement vector onto the wall's normal
                        self.movement_vector -= normal.scale(abs(dot_product))
                        # Apply deceleration to the current speed
                        self.current_speed -= self.deceleration * delta_time * 0.1
                        if self.current_speed < 0:
                            self.current_speed = 0  # Prevent negative speed

                    if distance < 0.3:
                        # Push the camera slightly out of the wall to avoid getting stuck
                        overlap = camera_radius - distance - 5
                        self.camera_pos += normal.scale(overlap * 0.001)
                    # Push the camera slightly out of the wall to avoid getting stuck
                    overlap = camera_radius - distance
                    self.camera_pos += normal.scale(overlap * 0.001)

        # Stop vertical velocity if on the ground
        self.camera_pos.y += self.vertical_velocity
        if self.is_sliding:
            trigger_position = Vec3(self.camera_pos.x,
                                    self.camera_pos.y, self.camera_pos.z)
        else:
            trigger_position = Vec3(self.camera_pos.x,
                                    self.camera_pos.y + 1, self.camera_pos.z)

        if trigger_position.y > 1.2:
            self.camera_pos.y -= 0.2  # Reset camera height if above ground
            self.is_on_ground = True
        elif trigger_position.y > 1:
            self.is_on_ground = True
        else:
            self.is_on_ground = False

        if self.movement_vector.mag < 0.2:
            # decrease acceleration if the player is not moving
            self.current_speed -= self.deceleration * delta_time * 2
            if self.current_speed < 0:
                self.current_speed = 0

        # Apply movement vector to camera position
        self.camera_pos += self.movement_vector

        # Apply gravity
        gravity = 0.01  # Gravity strength
        if not self.is_on_ground:
            self.vertical_velocity += gravity  # Apply gravity to vertical velocity
            self.camera_pos.y += self.vertical_velocity  # Update camera's Y position
        else:
            self.vertical_velocity = 0  # Reset vertical velocity when on the ground

        if self.camera_rot.x < -math.pi / 2:
            self.camera_rot.x = -math.pi / 2
        elif self.camera_rot.x > math.pi / 2:
            self.camera_rot.x = math.pi / 2

    def on_key_press(self, key, modifiers):
        if key == arcade.key.O:
            print(f"Current state: {self.state}")
        
        if self.state == "WIN":
            if key == arcade.key.ENTER or key == arcade.key.RETURN:
                self.set_state("TITLE")
                return
            return
        if self.state == "TITLE":
            self.title_screen.on_key_press_TITLE(key, modifiers)
            return  # Skip key presses when on the title screen
        if self.state == "SHOP":
            self.shop_screen.on_key_press_SHOP(key, modifiers)
            return
           
        # Exit from pause or death screen
        if self.is_paused or (hasattr(self.player, "health") and self.player.health <= 0):
            if key == arcade.key.Q:
                arcade.exit()
                return
            if hasattr(self.player, "health") and self.player.health <= 0:
                if key == arcade.key.R:
                    # Retry: reload current level
                    self.reload_level()
                    return
                elif key == arcade.key.T:
                    # Go to title screen
                    self.set_state("TITLE")
                    return
            if self.is_paused:
                if key == arcade.key.R:
                    self.reload_level()
                    self.is_paused = False
                    self.mouse_locked = True
                    self.set_exclusive_mouse(True)
                    return
                elif key == arcade.key.T:
                    self.exit_level()
                    return
                elif key == arcade.key.ESCAPE:
                    self.is_paused = False
                    self.mouse_locked = True
                    self.set_exclusive_mouse(True)
                    return
            return  # Ignore other keys while paused or dead

        if key == arcade.key.ESCAPE and self.state != "TITLE":
            self.is_paused = not self.is_paused
            self.mouse_locked = not self.is_paused
            self.set_exclusive_mouse(self.mouse_locked)
            return  # Don't process other actions when toggling pause

        if self.is_paused:
            return  # Ignore other keys while paused

        if not self.isLoaded:
            # If textures are not loaded, skip key presses
            return
        # Handle key presses for movement and actions
        if key == arcade.key.W:
            self.movement["forward"] = True
        elif key == arcade.key.S:
            self.movement["backward"] = True
        elif key == arcade.key.A:
            self.movement["left"] = True
        elif key == arcade.key.D:
            self.movement["right"] = True
        elif key == arcade.key.LCTRL:  # Slide
            if not self.is_sliding:
                self.is_sliding = True
                self.slide_timer = 0
                # Set the slide direction
                self.slide_dir = Vec3(
                    self.movement_vector.x, 0, self.movement_vector.z).normalize()
                if self.slide_dir.mag == 0:
                    self.slide_dir = self.forward
        elif key == arcade.key.SPACE:  # Jump
            if self.is_on_ground or self.camera_pos.y > -1:  # Only allow jumping if on the ground
                print("Jumping!")
                self.is_on_ground = False  # Set the flag to false when jumping
                self.vertical_velocity = -0.2  # Set jump power
        elif key == arcade.key.ESCAPE:
            self.mouse_locked = not self.mouse_locked
            self.set_exclusive_mouse(self.mouse_locked)  # Toggle mouse capture

        elif key == arcade.key.KEY_1:
            self.weapon_manager.switch("REVOLVER")

        elif key == arcade.key.KEY_2:
            self.weapon_manager.switch("SHOTGUN")

        elif key == arcade.key.G:
            # throw grenade
            grenade = {
                "id": 5,
                "model": Vec3(-self.camera_pos.x, -self.camera_pos.y, -self.camera_pos.z),
                "velocity": Vec3(0, 0, 0),
                "program": self.sphere_program,
                "geometry": self.generate_sphere(
                    0.1, 10, 10, position=self.camera_pos),
            }

        elif key == arcade.key.R:
            self.weapon_manager.reload_weapon()

        elif key == arcade.key.F:
            for rays in self.debug_rays:
                print("Ray Start:", rays[0], "Ray End:",
                      rays[1], "Color:", rays[2])

        elif key == arcade.key.E:
            # Interact with the closest button if available
            if self.interactions:
                # Find the closest button
                closest_button = min(
                    self.interactions,
                    key=lambda obj: math.sqrt(
                        (obj["position"].x + self.camera_pos.x) ** 2 +
                        (obj["position"].y + self.camera_pos.y) ** 2 +
                        (obj["position"].z + self.camera_pos.z) ** 2
                    )
                )
                if closest_button["action"] == "open_door":
                    # Open the door if the button is pressed
                    for door in self.doors:
                        if door["name"] == closest_button["target"]:
                            if door["lock"]:
                                self.interaction_feedback = "Interacted!"
                                self.interaction_feedback_timer = self.time + 0.7  # Show for 0.7 seconds
                                # Deactivate the button
                                closest_button["active"] = False
                                door["lock"] = False  # Unlock the door
                                # Update opacity based on lock state
                                door["opacity"] = 0.5

        elif key == arcade.key.Q:
            pass

        elif key == arcade.key.T:
            for door in self.doors:
                door["lock"] = not door["lock"]  # Toggle door lock state
                # Update opacity based on lock state
                if door["lock"]:
                    door["opacity"] = 0.9
                else:
                    door["opacity"] = 0.5

    def on_mouse_motion(self, x, y, dx, dy):
        if self.state == "TITLE":
            self.title_screen.on_mouse_motion(x, y, dx, dy)
            return
        if self.mouse_locked:
            self.camera_rot.y += dx * self.mouse_sensitivity
            self.camera_rot.x -= dy * self.mouse_sensitivity  # Invert pitch adjustment
        self._last_mouse_pos = (x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "TITLE":
            self.title_screen.on_mouse_press(x, y, button, modifiers)
            return
        elif self.state == "SHOP":
            self.shop_screen.on_mouse_press(x, y, button, modifiers)
            return  # Skip mouse presses when in the shop
        
            

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.weapon_manager.shoot():
                if self.weapon_manager.current.type == "REVOLVER":
                    self.debug_rays = []  # Clear debug rays

                    # raycast amd get the object hit
                    ray_start = Vec3(
                        -self.camera_pos.x,
                        -self.camera_pos.y,
                        -self.camera_pos.z
                    )
                    
                    ray_direction = Vec3(
                        math.sin(self.camera_rot.y),
                        -math.sin(self.camera_rot.x),
                        -math.cos(self.camera_rot.y)
                    )

                    raycast_result, hs = raycast.raycast(
                        ray_start, ray_direction, self.objects)
                    self.debug_rays.append(
                        (ray_start, ray_start + ray_direction.normalize().scale(100) + Vec3(
                            random.uniform(-0.1, 0.1),
                            random.uniform(-0.1, 0.1),
                            random.uniform(-0.1, 0.1)
                        ), (random.random(), random.random(),
                            random.random()), self.time  # Add a timestamp for the ray
                        ))
                    if raycast_result:
                        if raycast_result["id"] == 10:
                            # If the hit object is the enemy, apply damage
                            print("Hit enemy!")
                            if hs:
                                raycast_result["object"].apply_damage(
                                    self.weapon_manager.current.damage * self.weapon_manager.current.HS_multiplier) 
                                print("Headshot!")
                                self.HS_hitmarker = True
                                self.hitmarker_timer = self.time + 0.2  # Show hitmarker for 0.2 seconds
                            else:
                                raycast_result["object"].apply_damage(
                                    self.weapon_manager.current.damage)  
                                self.hitmarker = True
                                self.hitmarker_timer = self.time + 0.2  # Show hitmarker for 0.2 seconds
                        elif raycast_result["id"] == 1 and self.debugMode:
                            print(f"Hit wall {raycast_result['name']}!")
                        print(f"Hit: {raycast_result['name']}!")
                elif self.weapon_manager.current.type == "SHOTGUN":
                    self.debug_rays = []
                    ray_start = Vec3(
                        -self.camera_pos.x,
                        -self.camera_pos.y,
                        -self.camera_pos.z
                    )
                    for _ in range(5):  # Shoot 5 pellets
                        # Add random bloom to the direction
                        bloom_x = random.uniform(-0.04, 0.04)
                        bloom_y = random.uniform(-0.04, 0.04)
                        bloom_z = random.uniform(-0.04, 0.04)
                        ray_direction = Vec3(
                            math.sin(self.camera_rot.y) + bloom_x,
                            -math.sin(self.camera_rot.x) + bloom_y,
                            -math.cos(self.camera_rot.y) + bloom_z,
                        )
                        raycast_result, hs = raycast.raycast(
                            ray_start, ray_direction, self.objects)
                        # Draw debug ray for each pellet
                        self.debug_rays.append(
                            (ray_start, ray_start + ray_direction.normalize().scale(50) + Vec3(
                                random.uniform(-0.1, 0.1),
                                random.uniform(-0.1, 0.1),
                                random.uniform(-0.1, 0.1)
                            ), (random.random(), random.random(), random.random()), self.time)
                        )
                        if raycast_result:
                            if raycast_result["id"] == 10:
                                print("Hit enemy!")
                                if hs:
                                    raycast_result["object"].apply_damage(self.weapon_manager.current.damage * self.weapon_manager.current.HS_multiplier)
                                    print("Headshot!")
                                    self.HS_hitmarker = True
                                    self.hitmarker_timer = self.time + 0.2
                                else:
                                    raycast_result["object"].apply_damage(self.weapon_manager.current.damage)
                                    self.hitmarker = True
                                    self.hitmarker_timer = self.time + 0.2
                            elif raycast_result["id"] == 1 and self.debugMode:
                                print(f"Hit wall {raycast_result['name']}!")
                            print(f"Hit: {raycast_result['name']}!")
            else:
                if self.weapon_manager.current.chamber.count(1) == 0:
                    self.weapon_manager.reload_weapon()

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.weapon_manager.ADS(True)
            self.is_ADS = True

    def on_mouse_release(self, x, y, button, modifiers):
        if self.state == "TITLE":
            self.title_screen.on_mouse_release(x, y, button, modifiers)
            return
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.weapon_manager.ADS(False)
            self.is_ADS = False

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.movement["forward"] = False
        elif key == arcade.key.S:
            self.movement["backward"] = False
        elif key == arcade.key.A:
            self.movement["left"] = False
        elif key == arcade.key.D:
            self.movement["right"] = False
        elif key == arcade.key.UP:
            self.movement["up"] = False
        elif key == arcade.key.DOWN:
            self.movement["down"] = False
        elif key == arcade.key.LCTRL:
            self.is_sliding = False

    def on_resize(self, width, height):
        self.screen_width = width
        self.screen_height = height
        super().on_resize(width, height)

    def generate_sphere(self, radius, lat_segments, lon_segments, position=Vec3(0, 0, 0)):
        vertices = []
        indices = []
        px, py, pz = position  # Unpack the position tuple

        # Generate vertices with position only
        for lat in range(lat_segments + 1):
            theta = math.pi * lat / lat_segments  # Latitude angle
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)

            for lon in range(lon_segments + 1):
                phi = 2 * math.pi * lon / lon_segments  # Longitude angle

                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)

                # Calculate vertex position
                x = radius * sin_theta * cos_phi + px
                y = radius * cos_theta + py
                z = radius * sin_theta * sin_phi + pz

                # Add position to the vertex list
                vertices.extend([x, y, z])

        # Generate indices for triangle strips
        for lat in range(lat_segments):
            for lon in range(lon_segments):
                first = lat * (lon_segments + 1) + lon
                second = first + lon_segments + 1
                if lon < lon_segments:
                    indices.extend([first, second, first + 1])
                    indices.extend([second, second + 1, first + 1])

        # return the vertices and indices as a tuple of arrays
        sphere_array = array('f', vertices), array('I', indices)

        # convert to geometry
        sphere_buffer = self.ctx.buffer(data=sphere_array[0])
        sphere_geometry = self.ctx.geometry(
            content=[BufferDescription(
                sphere_buffer, "3f", ("in_pos",))],
            index_buffer=self.ctx.buffer(
                data=sphere_array[1]),  # Use index buffer
            mode=self.ctx.TRIANGLES,  # Use TRIANGLES for solid rendering
        )
        return sphere_geometry

    def get_distance(self, object):
        # Check if the buffer data has the expected number of values
        distance = 0
        if object["id"] == 1:
            # is colloseum wall
            if object["name"][:15] == "colosseum_wall":
                # always far away
                distance = 1000
            else:

                # Calculate the center of the wall by averaging all vertices' coordinates
                positions = object["buffer_data"]
                # Planes have 20 vertices (x, y, z, u, v)
                num_vertices = len(positions) // 5

                center_x = sum(positions[i * 5]
                               for i in range(num_vertices)) / num_vertices
                center_y = sum(positions[i * 5 + 1]
                               for i in range(num_vertices)) / num_vertices
                center_z = sum(positions[i * 5 + 2]
                               for i in range(num_vertices)) / num_vertices

                center = Vec3(center_x, center_y, center_z)

                # Calculate the distance between the camera and the wall's center
                distance = math.sqrt(
                    (self.camera_pos.x + center.x) ** 2 +
                    (self.camera_pos.y + center.y) ** 2 +
                    (self.camera_pos.z + center.z) ** 2
                )
        elif object["id"] == 2:
            # Calculate the center of the door by averaging all vertices' coordinates
            positions = object["buffer_data"]
            # Planes have 20 vertices (x, y, z, u, v)
            num_vertices = len(positions) // 5

            center_x = sum(positions[i * 5]
                           for i in range(num_vertices)) / num_vertices
            center_y = sum(positions[i * 5 + 1]
                           for i in range(num_vertices)) / num_vertices
            center_z = sum(positions[i * 5 + 2]
                           for i in range(num_vertices)) / num_vertices

            center = Vec3(center_x, center_y, center_z)

            # Calculate the distance between the camera and the wall's center
            distance = math.sqrt(
                (self.camera_pos.x + center.x) ** 2 +
                (self.camera_pos.y + center.y) ** 2 +
                (self.camera_pos.z + center.z) ** 2
            )
        elif object["id"] == 3:
            # Exit portal has only one vertex (x, y, z)
            exit_portal_position = object["model"]
            distance = math.sqrt(
                (self.camera_pos.x + exit_portal_position.x) ** 2 +
                (self.camera_pos.y + exit_portal_position.y) ** 2 +
                (self.camera_pos.z + exit_portal_position.z) ** 2
            )
        elif object["id"] == 4:
            # Projectiles have only one vertex (x, y, z)
            projectile_position = object["model"]
            distance = math.sqrt(
                (self.camera_pos.x + projectile_position[0]) ** 2 +
                (self.camera_pos.y + projectile_position[1]) ** 2 +
                (self.camera_pos.z + projectile_position[2]) ** 2
            )
        elif object["id"] == 10:
            # enemy1 has only one vertex (x, y, z)
            enemy1_position = object["object"].get_world_position()
            distance = math.sqrt(
                (self.camera_pos.x + enemy1_position.x) ** 2 +
                (self.camera_pos.y + enemy1_position.y) ** 2 +
                (self.camera_pos.z + enemy1_position.z) ** 2
            )
        elif object["id"] == 20:
            # buttons have only one vertex (x, y, z)
            button_position = object["position"]
            distance = math.sqrt(
                (self.camera_pos.x + button_position.x) ** 2 +
                (self.camera_pos.y + button_position.y) ** 2 +
                (self.camera_pos.z + button_position.z) ** 2
            )

        return distance

    def activate_room(self, room_number):
        # Only add enemies for the given room if not already present
        for enemy in self.enemies:
            if enemy.get("room", 1) == room_number and enemy not in self.objects:
                self.objects.append(enemy)
                enemy["spawned"] = True  # Mark as spawned when activated
                if "geometry" not in enemy:
                    if enemy["type"] == 1:
                        enemy["geometry"] = gltf_utils.load_gltf(
                            self, self.enemy1_gltf, self.enemy1_bin_data, scale=Vec3(0.6, 0.6, 0.6))
                    elif enemy["type"] == 2:
                        enemy["geometry"] = gltf_utils.load_gltf(
                            self, self.enemy2_gltf, self.enemy2_bin_data, scale=Vec3(3, 3, 3))
                    elif enemy["type"] == 3:
                        enemy["geometry"] = gltf_utils.load_gltf(
                            self, self.enemy1_gltf, self.enemy1_bin_data, scale=Vec3(1.2, 0.7, 1.2))
                    elif enemy["type"] == 4:
                        # mini boss enemy
                        enemy["geometry"] = [
                            gltf_utils.load_gltf(
                                self, self.miniboss1_gltf, self.miniboss1_bin_data, scale=Vec3(4, 4, 4)),
                            gltf_utils.load_gltf(
                                self, self.miniboss2_gltf, self.miniboss2_bin_data, scale=Vec3(4, 4, 4))
                        ]
                    elif enemy["type"] == 5:
                        # final boss enemy
                        enemy["geometry"] = gltf_utils.load_gltf(
                            self, self.final_boss_gltf, self.final_boss_bin_data, scale=Vec3(3, 3, 3))

    def load_level(self, level):
        self.isLoaded = False
        # Load the level data from a file or other source
        # Walls with buffer data and positions
        self.walls = self.levels[level - 1].get_walls()

        # Add the walls to the list of objects
        # Add geometry to the walls

        for wall in self.walls:
            self.objects.append(wall)
            wall_buffer = self.ctx.buffer(data=array('f', wall["buffer_data"]))
            wall["id"] = 1
            # if no texture is provided, use a default texture
            if "texture" not in wall:
                wall["texture"] = 1  # Set texture ID for walls
            if "opacity" not in wall:
                wall["opacity"] = 1.0  # Set default opacity for walls

            # Use the same shader program for walls
            wall["program"] = self.plane

            wall["geometry"] = self.ctx.geometry(
                content=[BufferDescription(
                    wall_buffer, "3f 2f", ("in_pos", "in_uv"))],
                mode=self.ctx.TRIANGLE_STRIP,  # Use TRIANGLE_STRIP for walls
            )

        self.doors = self.levels[level - 1].get_doors(self.plane)

        # Add the doors to the list of objects
        for door in self.doors:
            self.objects.append(door)
            door_buffer = self.ctx.buffer(data=array('f', door["buffer_data"]))
            door["id"] = 2
            door["geometry"] = self.ctx.geometry(
                content=[BufferDescription(
                    door_buffer, "3f 2f", ("in_pos", "in_uv"))],
                mode=self.ctx.TRIANGLE_STRIP,  # Use TRIANGLE_STRIP for doors
            )

        # get exit portal
        self.exit_portal = self.levels[level - 1].get_exit()
        self.exit_portal["id"] = 3
        self.exit_portal["program"] = self.sphere_program
        self.exit_portal["geometry"] = self.generate_sphere(
            2, 16, 16, position=self.exit_portal["model"])
        self.objects.append(self.exit_portal)

        # Initialize the enemy list
        self.enemies = self.levels[level -
                                   1].get_Enemies(self, self.GLTF_program)

        self.enemy1_gltf = GLTF2().load(self.enemy1_path[0])
        self.enemy2_gltf = GLTF2().load(self.enemy2_path[0])

        with open(self.enemy1_path[1], "rb") as f:
            self.enemy1_bin_data = f.read()

        with open(self.enemy2_path[1], "rb") as f:
            self.enemy2_bin_data = f.read()

        # mini boss
        self.miniboss1_gltf = GLTF2().load(self.miniboss1_path[0])
        self.miniboss2_gltf = GLTF2().load(self.miniboss2_path[0])

        with open(self.miniboss1_path[1], "rb") as f:
            self.miniboss1_bin_data = f.read()
        with open(self.miniboss2_path[1], "rb") as f:
            self.miniboss2_bin_data = f.read()

        # final boss
        self.final_boss_gltf = GLTF2().load(self.final_boss_path[0])
        with open(self.final_boss_path[1], "rb") as f:
            self.final_boss_bin_data = f.read()

        # Room triggers
        self.room_triggers = self.levels[level - 1].room_triggers()
        self.activated_rooms = set()

        # get buttons
        self.buttons = self.levels[level - 1].get_buttons(self.GLTF_program)
        self.button_gltf = GLTF2().load(self.button_path[0])
        with open(self.button_path[1], "rb") as f:
            self.button_bin_data = f.read()
        for button in self.buttons:
            self.objects.append(button)
            button["geometry"] = gltf_utils.load_gltf(
                self, self.button_gltf, self.button_bin_data, scale=Vec3(0.3, 0.16, 0.3))
        # Add a 'spawned' property to all enemies, miniboss is only 'spawned' when activated
        for enemy in self.enemies:
            enemy["spawned"] = False
        self.isLoaded = True

    def reload_level(self):
        # Logic to reload the level
        print("Reloading level...")
        self.objects.clear()
        self.walls.clear()
        self.doors.clear()
        self.exit_portal = None
        self.enemies.clear()
        self.activated_rooms = set()
        self.isLoaded = False
        self.player = Player()  # Reset player
        self.camera_pos = Vec3(0, -4, -5)
        self.camera_rot = Vec3(0, 0, 0)
        self.is_on_ground = True
        self.movement_vector = self.forward.scale(self.current_speed)
        self.load_level(self.selected_level)
        self.isLoaded = True
        
    def exit_level(self):
        # Logic to exit the level, e.g., go to the next level or end the game
        print("Exiting level...")
        self.objects.clear()
        self.walls.clear()
        self.doors.clear()
        self.exit_portal = None
        self.enemies.clear()
        self.activated_rooms = set()
        self.isLoaded = False
        self.player = Player()  # Reset player
        self.camera_pos = Vec3(0, -4, -5)
        self.camera_rot = Vec3(0, 0, 0)
        self.is_on_ground = True
        self.is_paused = False
        self.movement_vector = self.forward.scale(self.current_speed)
        # go to title screen
        self.set_state("TITLE")

    def change_level(self, level):
        # Clear existing objects and walls
        self.objects.clear()
        self.walls.clear()
        self.doors.clear()
        self.exit_portal = None

        # Load the new level
        self.load_level(level)

        # Reset camera position and rotation
        self.camera_pos = Vec3(0, 0, 0)
        self.camera_rot = Vec3(0, 0, 0)
        self.is_on_ground = True
        self.movement_vector = self.forward.scale(self.current_speed)
