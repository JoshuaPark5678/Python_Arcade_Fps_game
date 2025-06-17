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
        },
        {
            "name": "wall_005",
            "buffer_data": [
                # Position         UV
                4, -2, -4,       0, uv,  # Bottom Left
                4, 6, -4,        0, 0,   # Top Left
                16, -2, -4,      uv, uv,  # Bottom Right
                16, 6, -4,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_006",
            "buffer_data": [
                # Position         UV
                -16, -2, -4,       0, uv,  # Bottom Left
                -16, 6, -4,        0, 0,   # Top Left
                -16, -2, -16,      uv, uv,  # Bottom Right
                -16, 6, -16,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_007",
            "buffer_data": [
                # Position         UV
                -16, -2, -16,      0, uv,  # Bottom Left
                -16, 6, -16,       0, 0,   # Top Left
                -16, -2, -28,      uv, uv,  # Bottom Right
                -16, 6, -28,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_008",
            "buffer_data": [
                # Position         UV
                16, -2, -4,        0, uv,  # Bottom Left
                16, 6, -4,         0, 0,   # Top Left
                16, -2, -16,       uv, uv,  # Bottom Right
                16, 6, -16,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_009",
            "buffer_data": [
                # Position         UV
                16, -2, -16,       0, uv,  # Bottom Left
                16, 6, -16,        0, 0,   # Top Left
                16, -2, -28,       uv, uv,  # Bottom Right
                16, 6, -28,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_010",
            "buffer_data": [
                # Position         UV
                -4, -2, -28,       0, uv,  # Bottom Left
                -4, 6, -28,        0, 0,   # Top Left
                -16, -2, -28,      uv, uv,  # Bottom Right
                -16, 6, -28,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_011",
            "buffer_data": [
                # Position         UV
                4, -2, -28,       0, uv,  # Bottom Left
                4, 6, -28,        0, 0,   # Top Left
                16, -2, -28,      uv, uv,  # Bottom Right
                16, 6, -28,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_012",
            "buffer_data": [
                # Position         UV
                -4, -2, -28,       0, uv,  # Bottom Left
                -4, 6, -28,        0, 0,   # Top Left
                -4, -2, -40,       uv, uv,  # Bottom Right
                -4, 6, -40,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_013",
            "buffer_data": [
                # Position         UV
                4, -2, -28,       0, uv,  # Bottom Left
                4, 6, -28,        0, 0,   # Top Left
                4, -2, -40,       uv, uv,  # Bottom Right
                4, 6, -40,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_014",
            "buffer_data": [
                # Position         UV
                -4, -2, -40,       0, uv,  # Bottom Left
                -4, 6, -40,        0, 0,   # Top Left
                -4, -2, -52,       uv, uv,  # Bottom Right
                -4, 6, -52,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_015",
            "buffer_data": [
                # Position         UV
                4, -2, -40,       0, uv,  # Bottom Left
                4, 6, -40,        0, 0,   # Top Left
                16, -2, -40,      uv, uv,  # Bottom Right
                16, 6, -40,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_016",
            "buffer_data": [
                # Position         UV
                -4, -2, -52,       0, uv,  # Bottom Left
                -4, 6, -52,        0, 0,   # Top Left
                4, -2, -52,      uv, uv,  # Bottom Right
                4, 6, -52,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_017",
            "buffer_data": [
                # Position         UV
                4, -2, -52,       0, uv,  # Bottom Left
                4, 6, -52,        0, 0,   # Top Left
                16, -2, -52,      uv, uv,  # Bottom Right
                16, 6, -52,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_018",
            "buffer_data": [
                # slightly shorter wall
                # Position         UV
                4, 0.5, -40,       0, 1,  # Bottom Left
                4, -2, -40,        0, 0,   # Top Left
                4, 0.5, -52,      1, 1,  # Bottom Right
                4, -2, -52,       1, 0,  # Top Right
            ],
        },
        {
            "name": "wall_019",
            "buffer_data": [
                # slightly shorter wall
                # Position         UV
                16, 0.5, -40,       0, 1,  # Bottom Left
                16, -2, -40,        0, 0,   # Top Left
                16, 0.5, -52,      1, 1,  # Bottom Right
                16, -2, -52,       1, 0,  # Top Right
            ],
        },
        {
            "name": "wall_020",
            "buffer_data": [
                # slightly shorter wall
                # Position         UV
                16, -0.5, -40,       0, 1,  # Bottom Left
                16, 6, -40,        0, 0,   # Top Left
                28, -0.5, -40,      1, 1,  # Bottom Right
                28, 6, -40,       1, 0,  # Top Right
            ],
        },
        {
            "name": "wall_021",
            "buffer_data": [
                # Position         UV
                16, -2, -52,       0, uv,  # Bottom Left
                16, 6, -52,        0, 0,   # Top Left
                28, -2, -52,      uv, uv,  # Bottom Right
                28, 6, -52,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_022",
            "buffer_data": [
                # Position         UV
                28, -2, -40,       0, uv,  # Bottom Left
                28, 6, -40,        0, 0,   # Top Left
                28, -2, -52,       uv, uv,  # Bottom Right
                28, 6, -52,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_023",
            "buffer_data": [
                # Position         UV
                16, -2, -40,       0, uv,  # Bottom Left
                16, 6, -40,        0, 0,   # Top Left
                16, -2, -28,       uv, uv,  # Bottom Right
                16, 6, -28,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_024",
            "buffer_data": [
                # Position         UV
                28, -2, -40,       0, uv,  # Bottom Left
                28, 6, -40,        0, 0,   # Top Left
                40, -2, -40,       uv, uv,  # Bottom Right
                40, 6, -40,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_025",
            "buffer_data": [
                # Position         UV
                40, -2, -40,       0, uv,  # Bottom Left
                40, 6, -40,        0, 0,   # Top Left
                40, -2, -28,       uv, uv,  # Bottom Right
                40, 6, -28,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_026",
            "buffer_data": [
                # Position         UV
                40, -2, -28,       0, uv,  # Bottom Left
                40, 6, -28,        0, 0,   # Top Left
                40, -2, -16,       uv, uv,  # Bottom Right
                40, 6, -16,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_027",
            "buffer_data": [
                # Position         UV
                40, -2, -16,       0, uv,  # Bottom Left
                40, 6, -16,        0, 0,   # Top Left
                40, -2, -4,       uv, uv,  # Bottom Right
                40, 6, -4,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_028",
            "buffer_data": [
                # Position         UV
                28, -2, -4,       0, uv,  # Bottom Left
                28, 6, -4,        0, 0,   # Top Left
                40, -2, -4,       uv, uv,  # Bottom Right
                40, 6, -4,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_029",
            "buffer_data": [
                # Position         UV
                28, -2, -4,       0, uv,  # Bottom Left
                28, 6, -4,        0, 0,   # Top Left
                28, -2, 8,        uv, uv,  # Bottom Right
                28, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_030",
            "buffer_data": [
                # Position         UV
                28, -2, 8,        0, uv,  # Bottom Left
                28, 6, 8,         0, 0,   # Top Left
                16, -2, 8,        uv, uv,  # Bottom Right
                16, 6, 8,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_031",
            "buffer_data": [
                # Position         UV
                16, -2, 8,        0, uv,  # Bottom Left
                16, 6, 8,         0, 0,   # Top Left
                4, -2, 8,        uv, uv,  # Bottom Right
                4, 6, 8,         uv, 0,  # Top Right
            ],
        },
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
            "condition": "room1_dead",
            "buffer_data": [
                # Position         UV
                16, -2, -4,       0, 1,  # Bottom Left
                16, 6, -4,        0, 0,   # Top Left
                28, -2, -4,       1, 1,  # Bottom Right
                28, 6, -4,        1, 0,   # Top Right
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
    return walls


def get_Enemies(game, program):
    enemies = [
        {
            "name": "enemy1_001",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(35, -2, -30), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_002",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(35, -2, -20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        }
    ]
    return enemies

def room_triggers():
    """Get the room triggers for the level.
    These are used to change the room when the player enters a specific area.
    """
    triggers = [
        {
            "name": "room_trigger_001",
            "buffer_data": [
                # Position         UV
                -6, -2, -35,       0, 1,  # Bottom Left
                -6, 6, -35,        0, 0,   # Top Left
                6, -2, -35,        1, 1,  # Bottom Right
                6, 6, -35,         1, 0,  # Top Right
            ],
            "room": 1,
        },
    ]
    return triggers

def get_buttons(program):
    buttons = [
    ]
    return buttons

def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(10, 1, 2),
        "destination": 2,
    }
    return exit
