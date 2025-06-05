import arcade
from pyglet.math import Mat4, Vec3

import enemy

def get_walls():
    """Get the wall objects for the level.
    walls dimensions are 8x8 and have 0 width
    """
    uv = 2
    walls = [
        {
            "name": "wall_001",
            "buffer_data": [
                # Position         UV
                -4, -2, 8,       0, uv,  # Bottom Left
                -4, 6, 8,        0, 0,   # Top Left
                4, -2, 8,        uv, uv,  # Bottom Right
                4, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_002",
            "buffer_data": [
                # Position         UV
                -4, -2, -4,       0, uv,  # Bottom Left
                -4, 6, -4,        0, 0,   # Top Left
                -4, -2, 8,        uv, uv,  # Bottom Right
                -4, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_003",
            "buffer_data": [
                # Position         UV
                4, -2, -4,       0, uv,  # Bottom Left
                4, 6, -4,        0, 0,   # Top Left
                4, -2, 8,        uv, uv,  # Bottom Right
                4, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_004",
            "buffer_data": [
                # Position         UV
                -4, -2, -4,       0, uv,  # Bottom Left
                -4, 6, -4,        0, 0,   # Top Left
                -16, -2, -4,      uv, uv,  # Bottom Right
                -16, 6, -4,       uv, 0,  # Top Right
            ],
        }
    ]
    return walls

def get_doors(program):
    doors = [
        {
            "name": "door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 3,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                16, -2, -4,       0, 1,  # Bottom Left
                16, 6, -4,        0, 0,   # Top Left
                28, -2, -4,       1, 1,  # Bottom Right
                28, 6, -4,        1, 0,   # Top Right
            ],
        }
    ]
    return []
    return doors

def get_enemy_walls():
    """Get the walls that only for enemies.
    These walls are invisible to player but visible to enemies.
    """
    uv = 2
    walls = [
        {
            "name": "enemy_wall_001",
            "buffer_data": [
                # Position         UV
                16, -2, -40,   0, 1,  # Bottom Left
                16,  6,  -40,   0, 0,   # Top Left
                28, -2, -40,   1, 1,  # Bottom Right
                28,  6,  -40,   1, 0,  # Top Right
            ],
        },
    ]
    return []
    return walls


def get_Enemies(player, program):
    enemies = [
        {
            "name": "enemy1_001",
            "object": enemy.Enemy(player, get_walls(), get_enemy_walls(), Vec3(35, -2, -30), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_002",
            "object": enemy.Enemy(player, get_walls(), get_enemy_walls(), Vec3(35, -2, -20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        }
    ]
    return []
    return enemies

def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(10, 1, 2),
    }
    return exit
