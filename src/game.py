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

# ----- UTILS ----- #
import gltf_utils
import raycast

# Constants for screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Player:
    def __init__(self):
        self.health = 5  # Player's health
        self.max_health = 5  # Player's maximum health
        self.is_alive = True  # Player's alive status

    def apply_damage(self, damage):
        """
        Apply damage to the player and check if the player is still alive.
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            self.health = 0


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
            level2
        ]

        # debug variable
        self.debugVal = 0
        self.debugMode = False  # Debug mode flag

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

                uniform vec4 base_color_factor;  // Base color (RGBA)

                out vec4 fragColor;

                void main() {
                    vec4 base_color = base_color_factor;

                    fragColor = base_color;  // Output the final color
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
        door_texture = arcade.load_texture(
            f"{self.file_dir}/texture/green_door.png"
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
            size=(door_texture.width, door_texture.height),
            components=4,
            data=door_texture.image.tobytes(),
        )

        # Set the texture filtering mode to GL_NEAREST to remove blurriness
        self.texture1.filter = self.ctx.NEAREST, self.ctx.NEAREST
        self.texture2.filter = self.ctx.NEAREST, self.ctx.NEAREST
        self.texture3.filter = self.ctx.NEAREST, self.ctx.NEAREST

    def setup_revolver_textures(self):
        start = time.time()
        self.currentLoading = 0
        self.totalLoading = len(os.listdir(f"{self.file_dir}/model_ui/revolver/shoot/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/revolver/ADS_shoot/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/revolver/ADS_transition/")) + \
            len(os.listdir(f"{self.file_dir}/model_ui/revolver/Reload/"))

        # if debug mode is enabled, load only one frame of each animation
        if self.debugMode:
            self.revolver_textures = [arcade.load_texture(
                f"{self.file_dir}/model_ui/revolver/shoot/0001.png")]
            self.revolver_ADS_textures = [arcade.load_texture(
                f"{self.file_dir}/model_ui/revolver/ADS_shoot/0001.png")]
            self.revolver_ADS_transition_textures = [arcade.load_texture(
                f"{self.file_dir}/model_ui/revolver/ADS_transition/0001.png")]
            self.revolver_reload_textures = [arcade.load_texture(
                f"{self.file_dir}/model_ui/revolver/Reload/0001.png")]
            self.isLoaded = True  # Set flag when done
            return

        for i in range(1, 17):  # Assuming the images are named 0001.png to 0016.png
            texture_path = f"{self.file_dir}/model_ui/revolver/shoot/{i:04d}.png"
            self.revolver_textures.append(arcade.load_texture(texture_path))
            self.currentLoading += 1

        for i in range(1, 17):  # Assuming the images are named 0001.png to 0016.png
            texture_path = f"{self.file_dir}/model_ui/revolver/ADS_shoot/{i:04d}.png"
            self.revolver_ADS_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1

        for i in range(1, 9):  # Assuming the images are named 0001.png to 0008.png
            texture_path = f"{self.file_dir}/model_ui/revolver/ADS_transition/{i:04d}.png"
            self.revolver_ADS_transition_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1

        for i in range(1, 73):
            texture_path = f"{self.file_dir}/model_ui/revolver/Reload/{i:04d}.png"
            self.revolver_reload_textures.append(
                arcade.load_texture(texture_path))
            self.currentLoading += 1

        print("Revolver textures loaded")
        print("Textures loaded in", time.time() - start, "seconds")
        self.isLoaded = True  # Set flag when done

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

        # Ground geometry
        ground_buffer = self.ctx.buffer(
            data=array(
                'f',
                [
                    # Position         UV
                    -60, -2, 60,       0, 60,  # Top Left
                    -60, -2, -60,      0, 0,   # Bottom Left
                    60, -2, 60,        60, 60,  # Top Right
                    60, -2, -60,       60, 0,  # Bottom Right
                ]
            )
        )

        ceiling_buffer = self.ctx.buffer(
            data=array(
                'f',
                [
                    # Position         UV
                    -60, 6, 60,       0, 60,  # Top Left
                    -60, 6, -60,      0, 0,   # Bottom Left
                    60, 6, 60,        60, 60,  # Top Right
                    60, 6, -60,       60, 0,  # Bottom Right
                ]
            )
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

        self.enemy1_path = [f"{self.file_dir}/models/crazy_boy_test.gltf",
                       f"{self.file_dir}/models/crazy_boy_test.bin"]
        
        self.load_level(1)  # Load the first level
        
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
        self.player_currency = 0  # Player's currency

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
        # revolver animation
        self.revolver_textures = []  # List to store all textures for the animation
        self.revolver_ADS_textures = []  # List to store all textures for the ADS animation
        # List to store all textures for the ADS transition animation
        self.revolver_ADS_transition_textures = []
        # List to store all textures for the reload animation
        self.revolver_reload_textures = []

        self.current_frame = 0  # Current frame index
        self.animation_speed = 0.1  # Time (in seconds) between frames
        self.time_since_last_frame = 0  # Time accumulator for frame updates
        self.weapon_anim_running = False  # Flag to control animation
        self.revolver_in_transition = False  # Flag to control transition animation
        self.revolver_transition_frame = 0  # Frame index for the transition animation
        self.revolver_in_reload = False  # Flag to control reload animation
        self.revolver_reload_frame = 0  # Frame index for the reload animation

        self.isLoaded = False  # Flag to check if the textures are loaded
        
        threading.Thread(target=self.setup_revolver_textures,
                         daemon=True).start()

        # Set ammos
        self.max_ammo = 5  # Maximum ammo count
        self.cylinder_spin = 0  # Cylinder spin angle
        # Chamber state (1 for loaded, 0 for empty)
        self.chamber = [1] * self.max_ammo

        # set time
        self.time = 0  # UNIVERSAL TIME

        # set forward and right vectors
        self.forward = Vec3(0, 0, 0)  # Forward vector
        self.right = Vec3(0, 0, 0)  # Right vector

        # Each ray is (start: Vec3, end: Vec3, color: tuple)
        self.debug_rays = []

    def on_draw(self):
        if self.texture1 is None or self.texture2 is None or self.texture3 is None:
            self.setup_textures()

        if not self.isLoaded:
            # draw loading screen
            arcade.draw_xywh_rectangle_filled(
                0, 0, self.screen_width, self.screen_height, arcade.color.BLACK)
            # Draw loading bar
            loading_bar_width = (self.currentLoading / self.totalLoading)
            arcade.draw_text(f"Loading textures... {self.currentLoading}/{self.totalLoading} ({loading_bar_width * 100:.2f}%)",
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
                self.texture2.use(obj["texture"])
                obj["program"]["texture"] = obj["texture"]
                obj["program"]["opacity"] = obj["opacity"]
                obj["program"]["model"] = translate @ rotate_y @ rotate_x @ rotate_z
                obj["geometry"].render(obj["program"])
            elif obj["id"] == 2:
                # Bind the wall texture to the shader program
                self.texture3.use(obj["texture"])
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
                self.exit_portal["geometry"].render(self.exit_portal["program"])
            elif obj["id"] == 4:
                # Render projectiles
                obj["program"]["projection"] = self.proj
                obj["program"]["model"] = Mat4.from_translation(Vec3(
                    obj["model"].x, obj["model"].y, obj["model"].z)) @ rotate_y @ rotate_x  # Correctly set the model matrix
                obj["geometry"].render(obj["program"])

            # Render the enemy object
            elif obj["id"] == 10:  # Render enemy objects
                # Bind the GLTF program
                obj["program"]["projection"] = self.proj

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

                for i, enemy_geometry in enumerate(obj["geometry"]):

                    # Set material properties
                    obj["program"]["base_color_factor"] = enemy_geometry["base_color_factor"]

                    # Render the geometry
                    enemy_geometry["geometry"].render(obj["program"])

        for ray_start, ray_end, color, timestamp in self.debug_rays:

            # remove the exprired rays
            if self.time - timestamp > 0.5:  # Remove rays older than 0.5 seconds
                self.debug_rays.remove((ray_start, ray_end, color, timestamp))

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
            return  # Skip drawing the rest of the game when paused

    def draw_UI(self):
        try:
            # ==========================UI========================= #
            # =======================WEAPON======================== #

            # If the revolver is in transition, use the transition textures

            if self.revolver_in_reload:
                # If the revolver is reloading, use the reload textures
                current_texture = self.revolver_reload_textures[abs(
                    math.floor(self.revolver_reload_frame))]
            # transition anim is 8 frames contrary to the 16 frames of the shooting anim
            elif self.revolver_in_transition and self.is_ADS and not self.revolver_in_reload:
                # If aiming down sights, use the ADS transition textures
                current_texture = self.revolver_ADS_transition_textures[abs(
                    self.revolver_transition_frame)]
            elif self.revolver_in_transition and not self.is_ADS and not self.revolver_in_reload:
                # If not aiming down sights, use the transition in reverse
                current_texture = self.revolver_ADS_transition_textures[abs(
                    self.revolver_transition_frame-7)]
            else:
                # If the revolver is not in transition, use the regular textures
                if self.is_ADS:
                    # If aiming down sights, use the ADS textures
                    current_texture = self.revolver_ADS_textures[self.current_frame]
                else:
                    # If not aiming down sights, use the regular textures
                    current_texture = self.revolver_textures[self.current_frame]
            # Draw the revolver texture
            arcade.draw_texture_rectangle(
                # X position (center of the screen)
                (self.screen_width // 2) + math.sin(
                    time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 200,
                # Y position (center of the screen)
                (self.screen_height // 2 - 60) + math.sin(
                    time.time() * self.shake_speed) * self.shake_intensity * self.shake_direction * 100,
                self.screen_width,  # Width of the texture
                self.screen_height + 20,  # Height of the texture
                current_texture  # The texture to draw
            )

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
            # ========================INFO========================== #
            # display health bar
            arcade.draw_ellipse_filled(
                self.screen_width // 2, self.screen_height // 22, self.screen_width // 8, self.screen_height // 14, arcade.color.DARK_GRAY)
            arcade.draw_text("Health", self.screen_width // 2, self.screen_height // 16,
                             arcade.color.BLACK, 12, font_name="Kenney Future", anchor_x="center", anchor_y="center", bold=True)
            arcade.draw_xywh_rectangle_filled(
                self.screen_width // 2 - (self.screen_width // 8) / 2, self.screen_height // 22 - (self.screen_height // 28), self.screen_width // 8 * (self.player.health / self.player.max_health), self.screen_height // 32, arcade.color.RED)

            for i in range(1, 6):
                # evenly cut the health bar into 5 parts
                arcade.draw_rectangle_outline(
                    self.screen_width // 2 - (self.screen_width // 8) / 1.7 + (self.screen_width // 8) / 5 * i, self.screen_height // 36, self.screen_width // 8 / 5, self.screen_height // 32, arcade.color.BLACK, 4)
            arcade.draw_rectangle_outline(
                self.screen_width // 2, self.screen_height // 36, self.screen_width // 8, self.screen_height // 32, arcade.color.BLACK, 4)

            # display CYLINDER
            cylinder_radius = self.screen_width // 10
            if self.current_frame < 8:
                cylinder_radius += self.current_frame // 2
            else:
                cylinder_radius -= (self.current_frame - 8) // 2

            # center of the cylinder
            center = [self.screen_width -
                      cylinder_radius // 2, cylinder_radius // 2]

            # Draw the cylinder body
            arcade.draw_circle_filled(
                center[0], center[1], cylinder_radius, (45, 45, 55))
            arcade.draw_circle_filled(
                center[0], center[1], cylinder_radius // 1.2, arcade.color.GRAY)
            arcade.draw_circle_outline(
                center[0], center[1], cylinder_radius, arcade.color.BLACK, 4
            )
            # draw the cylinder middle thingy
            arcade.draw_circle_filled(
                center[0], center[1], cylinder_radius // 6, (55, 55, 65))
            arcade.draw_circle_outline(
                center[0], center[1], cylinder_radius // 6, arcade.color.BLACK, 4)

            # draw the cylinder bullets (5 bullets)
            angle = 360 / 5

            # chamber is self.chamber's first 5 elements.
            # If self.chamber length is less than 5, fill the rest with 0
            chamber = self.chamber[:5] + [0] * (5 - len(self.chamber))
            # all bullets that are > 0
            ammo = len([bullet for bullet in chamber if bullet > 0])
            back_cycle = 90
            if self.current_frame > 0:
                # If the revolver is in the shooting animation
                back_cycle = 162

            for i in range(5):
                # Calculate the position of each bullet
                bullet_angle = math.radians(
                    angle * i) + math.radians(back_cycle) - math.radians(self.cylinder_spin)
                # Calculate the bullet's position based on the angle
                bullet_x = center[0] + \
                    cylinder_radius // 2 * math.cos(bullet_angle)
                bullet_y = center[1] + \
                    cylinder_radius // 2 * math.sin(bullet_angle)

                # Draw the bullet starting from the top of the cylinder
                top_bullet = chamber[i - (self.cylinder_spin // 72) % 5]
                if top_bullet == 1:
                    arcade.draw_circle_filled(
                        bullet_x, bullet_y, cylinder_radius // 6, arcade.color.DARK_GRAY)
                elif top_bullet == 2:
                    arcade.draw_circle_filled(
                        bullet_x, bullet_y, cylinder_radius // 6, arcade.color.GOLD)
                else:
                    arcade.draw_circle_filled(
                        bullet_x, bullet_y, cylinder_radius // 6, arcade.color.BLACK)

                # Draw the bullet outline
                arcade.draw_circle_outline(
                    bullet_x, bullet_y, cylinder_radius // 6, arcade.color.BLACK, 2)

            # ========================GAME_INFO========================== #

            # Display camera position
            arcade.draw_text(
                f"Camera Position: ({self.camera_pos.x:.6f}, {self.camera_pos.y:.6f}, {self.camera_pos.z:.6f})",
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
        except Exception as e:
            print(f"Error drawing texture: {e}")

    def on_update(self, delta_time: float):
        if self.is_paused:
            return  # Skip updating the game when paused

        # Update the time
        self.time += delta_time

        if not self.isLoaded:
            # If textures are not loaded, skip the update
            return

        # Update object list
        self.objects.sort(key=self.get_distance, reverse=True)

        # set mouse active
        self.set_mouse_visible(not self.mouse_locked)
        self.set_exclusive_mouse(self.mouse_locked)
        
        enemy_count = 0  # Count the number of enemies
        for obj in self.objects:
            if obj["id"] == 10:
                obj["object"].move(-self.camera_pos)
                if obj["object"].is_dead():
                    self.objects.remove(obj)
                else:
                    enemy_count += 1

        if enemy_count == 0:
            for door in self.doors:
                if door["name"] == "door_001":
                    # Unlock the door if all enemies are defeated
                    door["lock"] = False
                    door["opacity"] = 0.5  # Update opacity based on lock state

        # Update the revolver animation frame
        if self.is_ADS:
            # Zoom in
            if self.fov > 70:
                # Zoom in
                self.fov -= 3
            self.mouse_sensitivity = 0.0005
        else:
            if self.fov < 90:
                # Zoom out
                self.fov += 3
            self.mouse_sensitivity = 0.001

        if self.revolver_in_reload:
            # Update the reload animation frame
            self.revolver_reload_frame += 0.75
            if self.revolver_reload_frame >= len(self.revolver_reload_textures):
                self.revolver_in_reload = False
                self.revolver_reload_frame = 0

        if self.revolver_in_transition and not self.revolver_in_reload:
            self.revolver_transition_frame += 1
            if self.revolver_transition_frame >= len(self.revolver_ADS_transition_textures):
                self.revolver_in_transition = False
                self.revolver_transition_frame = 0  # Reset the transition frame

            if self.revolver_transition_frame == len(self.revolver_ADS_transition_textures)-1:
                self.cylinder_spin = 0

        if self.revolver_in_reload:
            intFrame = int(self.revolver_reload_frame +
                           (self.revolver_reload_frame / 0.75 * 0.25))

            try:
                if intFrame > 15 and intFrame < 21:
                    try:
                        self.chamber[intFrame - 16] = 0
                    except IndexError:
                        self.chamber.append(0)

                if intFrame > 39 and intFrame < 45:
                    self.chamber[intFrame - 40] = 1
                # spin the cylinder during reload

                if intFrame > 41:
                    self.cylinder_spin += 12
                    # Reset the spin if it exceeds 360 degrees
                    if self.cylinder_spin >= 360:
                        self.cylinder_spin = self.cylinder_spin - 360

                else:
                    if intFrame > 12:
                        # spin the cylinder
                        self.cylinder_spin -= 4
                        # Reset the spin if it exceeds 360 degrees
                        if self.cylinder_spin >= 360:
                            self.cylinder_spin = 0
            except IndexError:
                # nothing
                pass

            if intFrame == len(self.revolver_reload_textures)-1:
                self.cylinder_spin = 0
                if self.is_ADS:
                    self.revolver_in_transition = True
                    self.revolver_transition_frame = 0
                else:
                    self.revolver_in_transition = False
                    self.revolver_transition_frame = 0

        if self.weapon_anim_running and not self.revolver_in_reload:
            # Calculate the spin based on the current frame
            # 12 frames to spin 72 degrees
            if self.current_frame > 3:
                self.cylinder_spin += 6
            # Reset the spin if it exceeds 360 degrees
            if self.cylinder_spin >= 360:
                self.cylinder_spin = 0

            # Update the revolver animation frame
            if self.current_frame < 3:
                if self.is_ADS:
                    self.camera_rot.x -= 0.005  # Adjust the camera rotation for the animation
                else:
                    self.camera_rot.x -= 0.01  # Adjust the camera rotation for the animation
            # Update the time accumulator
            self.time_since_last_frame += 0.5
            # Check if it's time to update the frame
            if self.time_since_last_frame >= self.animation_speed:
                self.time_since_last_frame = 0  # Reset the time accumulator
                self.current_frame += 1  # Move to the next frame

                # Loop back to the first frame if we reach the end
                if self.current_frame >= len(self.revolver_textures):
                    self.current_frame = 0
                    self.cylinder_spin = 0
                    self.weapon_anim_running = False  # Stop the animation after one cycle
        
        for obj in self.objects:
            if obj["id"] == 4:
                # Update the projectile's position based on its velocity
                obj["model"] = obj["model"] + obj["velocity"]
                # Check if the projectile is out of bounds and remove it
                if (obj["model"].x < -100 or obj["model"].x > 100 or
                        obj["model"].y < -100 or obj["model"].y > 100 or
                        obj["model"].z < -100 or obj["model"].z > 100) or obj["model"].y < -2:
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
        gravity = 0.02  # Gravity strength
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
        if key == arcade.key.ESCAPE:
            self.is_paused = not self.is_paused
            self.mouse_locked = not self.is_paused
            self.set_mouse_visible(not self.mouse_locked)
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
                self.vertical_velocity = -0.3  # Set jump power
        elif key == arcade.key.ESCAPE:
            self.mouse_locked = not self.mouse_locked
            self.set_mouse_visible(not self.mouse_locked)
            self.set_exclusive_mouse(self.mouse_locked)  # Toggle mouse capture

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
            # Reload the revolver
            print("Reloading!")
            self.revolver_in_reload = True
            if self.debugMode:
                # Fill the chamber with bullets for debugging
                self.chamber = [1] * self.max_ammo

            # self.chamber = [1] * self.max_ammo  # Fill the chamber with bullets

            # if len(self.chamber) < self.max_ammo:
            #     self.chamber.append(1)  # Add a bullet to the chamber

        elif key == arcade.key.F:
            for rays in self.debug_rays:
                print("Ray Start:", rays[0], "Ray End:",
                      rays[1], "Color:", rays[2])

        elif key == arcade.key.E:
            # move the enemy object forward
            for obj in self.objects:
                if obj["id"] == 10:
                    # Move the enemy object forward according to its rotation
                    rotation = obj["object"].get_rotation()
                    forward = Vec3(
                        math.sin(rotation.y), 0, math.cos(rotation.y))
                    # Move forward by 0.1 units
                    obj["object"].move(forward.scale(0.1))

        elif key == arcade.key.Q:
            pass

        elif key == arcade.key.T:
            for door in self.doors:
                door["lock"] = not door["lock"]  # Toggle door lock state
                # Update opacity based on lock state
                door["opacity"] = 0.5 if door["lock"] else 1.0

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_locked:
            self.camera_rot.y += dx * self.mouse_sensitivity
            self.camera_rot.x -= dy * self.mouse_sensitivity  # Invert pitch adjustment

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.isLoaded:
            # If textures are not loaded, skip key presses
            return
        if button == arcade.MOUSE_BUTTON_LEFT:
            # check if there are ammo
            if len([bullet for bullet in self.chamber if bullet > 0]) > 0:
                if not self.weapon_anim_running:  # Start the animation only if it's not already running
                    print("Shooting!")
                    # Decrease ammo count
                    self.chamber.pop(0)

                    self.weapon_anim_running = True
                    self.current_frame = 0  # Reset to the first frame

                    # # shoot projectile
                    # projectile = {
                    #     "id": 4,
                    #     "model": Vec3(-self.camera_pos.x, -self.camera_pos.y, -self.camera_pos.z),
                    #     "velocity": Vec3(0, 0, 0),
                    #     "program": self.sphere_program,
                    #     "geometry": self.generate_sphere(
                    #         0.1, 10, 10, position=self.camera_pos),
                    # }
                    # # Set the projectile's velocity based on the camera direction
                    # projectile["velocity"] = Vec3(
                    #     math.sin(self.camera_rot.y),
                    #     -math.sin(self.camera_rot.x),
                    #     -math.cos(self.camera_rot.y),
                    # )

                    # self.projectiles.append(projectile)
                    # # Add the projectile to the list of objects
                    # self.objects.append(projectile)

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
                        -math.cos(self.camera_rot.y),
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
                                    20)  # Apply 20 damage for headshot
                                print("Headshot!")
                            else:
                                raycast_result["object"].apply_damage(
                                    10)  # Apply 10 damage if no headshot
            else:
                self.revolver_in_reload = True

        if button == arcade.MOUSE_BUTTON_RIGHT:
            # Check if the right mouse button is pressed
            self.revolver_in_transition = True
            self.is_ADS = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            # Check if the right mouse button is released
            self.revolver_in_transition = True
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

        return distance
        
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
            wall["texture"] = 1  # Set texture ID for walls
            # Use the same shader program for walls
            wall["program"] = self.plane
            wall["opacity"] = 1.0  # Set default opacity for walls
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
        self.enemies = self.levels[level - 1].get_Enemies(self.player, self.GLTF_program)

        self.enemy1_gltf = GLTF2().load(self.enemy1_path[0])

        with open(self.enemy1_path[1], "rb") as f:
            self.enemy1_bin_data = f.read()

        # Add the enemy to the list of objects
        for enemy in self.enemies:
            self.objects.append(enemy)
            enemy["geometry"] = gltf_utils.load_gltf(
                self, self.enemy1_gltf, self.enemy1_bin_data, scale=Vec3(0.2, 0.2, 0.2))
            
        self.isLoaded = True

    def exit_level(self):
        # Logic to exit the level, e.g., load the next level or return to the main menu
        self.isLoaded = False
        print("Exiting level...")
        self.change_level(2)

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
        self.vertical_velocity = 0
        self.current_speed = 0
        self.movement_vector = Vec3(0, 0, 0)