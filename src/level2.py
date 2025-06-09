import arcade
from pyglet.math import Mat4, Vec3

import enemy

def get_walls():
    """Get the wall objects for the level.
    walls dimensions are 12x8 and have 0 width
    """
    uv = 2
    walls = [
        {
            "name": "wall_001",
            "buffer_data": [
                # Position         UV
                -6, -2, 8,       0, uv,  # Bottom Left
                -6, 6, 8,        0, 0,   # Top Left
                6, -2, 8,        uv, uv,  # Bottom Right
                6, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_002",
            "buffer_data": [
                # Position         UV
                -6, -2, -6,       0, uv,  # Bottom Left
                -6, 6, -6,        0, 0,   # Top Left
                -6, -2, 8,        uv, uv,  # Bottom Right
                -6, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_003",
            "buffer_data": [
                # Position         UV
                6, -2, -6,       0, uv,  # Bottom Left
                6, 6, -6,        0, 0,   # Top Left
                6, -2, 8,        uv, uv,  # Bottom Right
                6, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_004",
            "buffer_data": [
                # Position         UV
                -6, -2, -6,       0, uv,  # Bottom Left
                -6, 6, -6,        0, 0,   # Top Left
                -6, -2, -18,      uv, uv,  # Bottom Right
                -6, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_005",
            "buffer_data": [
                # Position         UV
                6, -2, -6,       0, uv,  # Bottom Left
                6, 6, -6,        0, 0,   # Top Left
                6, -2, -18,      uv, uv,  # Bottom Right
                6, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_006",
            "buffer_data": [
                # Position         UV
                -6, -2, -18,       0, uv,  # Bottom Left
                -6, 6, -18,        0, 0,   # Top Left
                -6, -2, -30,      uv, uv,  # Bottom Right
                -6, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_007",
            "buffer_data": [
                # Position         UV
                6, -2, -18,       0, uv,  # Bottom Left
                6, 6, -18,        0, 0,   # Top Left
                6, -2, -30,      uv, uv,  # Bottom Right
                6, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_008",
            "buffer_data": [
                # Position         UV
                6, -2, -30,       0, uv,  # Bottom Left
                6, 6, -30,        0, 0,   # Top Left
                18, -2, -30,      uv, uv,  # Bottom Right
                18, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_009",
            "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, uv,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                -18, -2, -30,      uv, uv,  # Bottom Right
                -18, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0010",
            "buffer_data": [
                # Position         UV
                6, -2, -42,       0, uv,  # Bottom Left
                6, 6, -42,        0, 0,   # Top Left
                18, -2, -42,      uv, uv,  # Bottom Right
                18, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0011",
            "buffer_data": [
                # Position         UV
                -6, -2, -42,       0, uv,  # Bottom Left
                -6, 6, -42,        0, 0,   # Top Left
                -18, -2, -42,      uv, uv,  # Bottom Right
                -18, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0012",
            "buffer_data": [
                # Position         UV
                6, -2, -42,       0, uv,  # Bottom Left
                6, 6, -42,        0, 0,   # Top Left
                -6, -2, -42,      uv, uv,  # Bottom Right
                -6, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0013",
            "buffer_data": [
                # Position         UV
                30, -2, -42,       0, uv,  # Bottom Left
                30, 6, -42,        0, 0,   # Top Left
                18, -2, -42,      uv, uv,  # Bottom Right
                18, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0014",
            "buffer_data": [
                # Position         UV
                30, -2, -42,       0, uv,  # Bottom Left
                30, 6, -42,        0, 0,   # Top Left
                30, -2, -30,      uv, uv,  # Bottom Right
                30, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0015",
            "buffer_data": [
                # Position         UV
                30, -2, -30,       0, uv,  # Bottom Left
                30, 6, -30,        0, 0,   # Top Left
                42, -2, -30,      uv, uv,  # Bottom Right
                42, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0016",
            "buffer_data": [
                # Position         UV
                42, -2, -30,       0, uv,  # Bottom Left
                42, 6, -30,        0, 0,   # Top Left
                42, -2, -18,      uv, uv,  # Bottom Right
                42, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0017",
            "buffer_data": [
                # Position         UV
                42, -2, -6,       0, uv,  # Bottom Left
                42, 6, -6,        0, 0,   # Top Left
                42, -2, -18,      uv, uv,  # Bottom Right
                42, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0018",
            "buffer_data": [
                # Position         UV
                42, -2, 8,       0, uv,  # Bottom Left
                42, 6, 8,        0, 0,   # Top Left
                42, -2, -6,      uv, uv,  # Bottom Right
                42, 6, -6,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0019",
            "buffer_data": [
                # Position         UV
                18, -2, 8,       0, uv,  # Bottom Left
                18, 6, 8,        0, 0,   # Top Left
                6, -2, 8,        uv, uv,  # Bottom Right
                6, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0020",
            "buffer_data": [
                # Position         UV
                18, -2, 8,       0, uv,  # Bottom Left
                18, 6, 8,        0, 0,   # Top Left
                30, -2, 8,        uv, uv,  # Bottom Right
                30, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0021",
            "buffer_data": [
                # Position         UV
                30, -2, 8,       0, uv,  # Bottom Left
                30, 6, 8,        0, 0,   # Top Left
                42, -2, 8,        uv, uv,  # Bottom Right
                42, 6, 8,         uv, 0,  # Top Right
            ],
        }
    ]
    return walls

def get_doors(program):
    doors = [
        {
            "name": "red_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 4,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -18, -2, -42,       0, 1,  # Bottom Left
                -18, 6, -42,        0, 0,   # Top Left
                -18, -2, -30,       1, 1,  # Bottom Right
                -18, 6, -30,        1, 0,  # Top Right
            ],
        }
    ]
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
            "object": enemy.Enemy(player, get_walls(), get_enemy_walls(), Vec3(18, -2, -6), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_002",
            "object": enemy.Enemy(player, get_walls(), get_enemy_walls(), Vec3(30, -2, -6), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_003",
            "object": enemy.Enemy(player, get_walls(), get_enemy_walls(), Vec3(14, -2, -4), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_004",
            "object": enemy.Enemy(player, get_walls(), get_enemy_walls(), Vec3(34, -2, -4), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        }
    ]
    return enemies

def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(10, 1, 2),
    }
    return exit
