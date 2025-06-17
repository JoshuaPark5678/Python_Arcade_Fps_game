import arcade
from pyglet.math import Mat4, Vec3
import math

import enemy


def get_walls():
    """
    Get the wall objects for the level.
    Now generates a circular colosseum of normal walls.
    """
    
    uv = 2
    
    walls = [
        {
        "name": "wall_001",
        "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, uv,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                -6, -2, -42,        uv, uv,  # Bottom Right
                -6, 6, -42,         uv, 0,  # Top Right
        ],
        },
        {
            "name": "wall_002",
            "buffer_data": [
                # Position         UV
                6, -2, -30,       0, uv,  # Bottom Left
                6, 6, -30,        0, 0,   # Top Left
                6, -2, -42,        uv, uv,  # Bottom Right
                6, 6, -42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_004",
            "buffer_data": [
                # Position         UV
                -6, -2, 30,       0, uv,  # Bottom Left
                -6, 6, 30,        0, 0,   # Top Left
                -6, -2, 42,        uv, uv,  # Bottom Right
                -6, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_005",
            "buffer_data": [
                # Position         UV
                6, -2, 30,       0, uv,  # Bottom Left
                6, 6, 30,        0, 0,   # Top Left
                6, -2, 42,        uv, uv,  # Bottom Right
                6, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_006",
            "buffer_data": [
                # Position         UV
                -30, -2, 6,       0, uv,  # Bottom Left
                -30, 6, 6,        0, 0,   # Top Left
                -42, -2, 6,        uv, uv,  # Bottom Right
                -42, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_007",
            "buffer_data": [
                # Position         UV
                -30, -2, -6,       0, uv,  # Bottom Left
                -30, 6, -6,        0, 0,   # Top Left
                -42, -2, -6,        uv, uv,  # Bottom Right
                -42, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_008",
            "buffer_data": [
                # Position         UV
                30, -2, 6,       0, uv,  # Bottom Left
                30, 6, 6,        0, 0,   # Top Left
                42, -2, 6,        uv, uv,  # Bottom Right
                42, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_009",
            "buffer_data": [
                # Position         UV
                30, -2, -6,       0, uv,  # Bottom Left
                30, 6, -6,        0, 0,   # Top Left
                42, -2, -6,        uv, uv,  # Bottom Right
                42, 6, -6,         uv, 0,  # Top Right
            ],
        },
        
    ]
    
    
    center = Vec3(0, -2, 0)  # Center of the colosseum (adjust as needed)
    radius = 40                # Radius of the colosseum
    height = 8                 # Wall height
    num_segments = 32          # Number of wall segments (higher = smoother)
    
    for i in range(num_segments):
        angle0 = 2 * math.pi * i / num_segments
        angle1 = 2 * math.pi * (i + 1) / num_segments
        x0 = center.x + radius * math.cos(angle0)
        z0 = center.z + radius * math.sin(angle0)
        x1 = center.x + radius * math.cos(angle1)
        z1 = center.z + radius * math.sin(angle1)
        wall = {
            "name": f"colosseum_wall_{i:03}",
            "buffer_data": [
                # Position         UV
                x0, center.y, z0,   0, uv,   # Bottom Left
                x0, center.y + height, z0,   0, 0,    # Top Left
                x1, center.y, z1,   uv, uv,  # Bottom Right
                x1, center.y + height, z1,   uv, 0,   # Top Right
            ],
        }
        walls.append(wall)
        
        
    return walls


def get_doors(program):
    doors = [
        {
            "name": "red_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 3,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, 1,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                6, -2, -30,        1, 1,  # Bottom Right
                6, 6, -30,         1, 0,  # Top Right
            ],
        },
    ]
    return doors


def get_enemy_walls():
    """Get the walls that only for enemies.
    These walls are invisible to player but visible to enemies.
    """
    uv = 2
    walls = [

    ]
    return []


def get_Enemies(game, program):
    enemies = [
        # FIRST ROOM ENEMIES
        


    ]
    return enemies


def get_buttons(program):
    buttons = [
        {
            "name": "button_001",
            "id": 20,
            "program": program,
            "position": Vec3(0, -2, 88),
            "rotation": Vec3(0, 0, 0),
            "active": True,
            "action": "open_door",
            "target": "red_door_001"
        }
    ]
    return buttons


def room_triggers():
    """Get the room triggers for the level.
    These are used to change the room when the player enters a specific area.
    """
    triggers = [
        {
            "name": "room_trigger_001",
            "buffer_data": [
                # Position         UV
                -5, -2, -5,       0, 1,  # Bottom Left
                -5, 6, -5,        0, 0,   # Top Left
                5, -2, 5,        1, 1,  # Bottom Right
                5, 6, 5,         1, 0,  # Top Right
            ],
            "room": 1,
        },
    ]
    return triggers


def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(0, 1, -36),
        "destination": 3,
    }
    return exit
