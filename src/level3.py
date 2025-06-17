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
                6, -2, -18,       0, uv,  # Bottom Left
                6, 6, -18,        0, 0,   # Top Left
                18, -2, -18,        uv, uv,  # Bottom Right
                18, 6, -18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_005",
            "buffer_data": [
                # Position         UV
                -6, -2, -18,       0, uv,  # Bottom Left
                -6, 6, -18,        0, 0,   # Top Left
                -18, -2, -18,        uv, uv,  # Bottom Right
                -18, 6, -18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_006",
            "buffer_data": [
                # Position         UV
                -18, -2, -18,       0, uv,  # Bottom Left
                -18, 6, -18,        0, 0,   # Top Left
                -18, -2, -6,        uv, uv,  # Bottom Right
                -18, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_007",
            "buffer_data": [
                # Position         UV
                18, -2, -18,       0, uv,  # Bottom Left
                18, 6, -18,        0, 0,   # Top Left
                18, -2, -6,        uv, uv,  # Bottom Right
                18, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_008",
            "buffer_data": [
                # Position         UV
                -18, -2, 6,       0, uv,  # Bottom Left
                -18, 6, 6,        0, 0,   # Top Left
                -18, -2, -6,        uv, uv,  # Bottom Right
                -18, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_009",
            "buffer_data": [
                # Position         UV
                18, -2, 6,       0, uv,  # Bottom Left
                18, 6,  6,        0, 0,   # Top Left
                18, -2, -6,        uv, uv,  # Bottom Right
                18, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_010",
            "buffer_data": [
                # Position         UV
                -18, -2, 6,       0, uv,  # Bottom Left
                -18, 6, 6,        0, 0,   # Top Left
                -18, -2, 18,        uv, uv,  # Bottom Right
                -18, 6, 18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_011",
            "buffer_data": [
                # Position         UV
                18, -2, 6,       0, uv,  # Bottom Left
                18, 6,  6,        0, 0,   # Top Left
                18, -2, 18,        uv, uv,  # Bottom Right
                18, 6, 18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_012",
            "buffer_data": [
                # Position         UV
                -18, -2, 18,       0, uv,  # Bottom Left
                -18, 6, 18,        0, 0,   # Top Left
                -18, -2, 30,        uv, uv,  # Bottom Right
                -18, 6, 30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_013",
            "buffer_data": [
                # Position         UV
                18, -2, 18,       0, uv,  # Bottom Left
                18, 6,  18,        0, 0,   # Top Left
                18, -2, 30,        uv, uv,  # Bottom Right
                18, 6, 30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_014",
            "buffer_data": [
                # Position         UV
                -18, -2, 30,       0, uv,  # Bottom Left
                -18, 6, 30,        0, 0,   # Top Left
                -18, -2, 42,        uv, uv,  # Bottom Right
                -18, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_015",
            "buffer_data": [
                # Position         UV
                18, -2, 30,       0, uv,  # Bottom Left
                18, 6,  30,        0, 0,   # Top Left
                18, -2, 42,        uv, uv,  # Bottom Right
                18, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_016",
            "buffer_data": [
                # Position         UV
                -18, -2, 54,       0, uv,  # Bottom Left
                -18, 6, 54,        0, 0,   # Top Left
                -18, -2, 42,        uv, uv,  # Bottom Right
                -18, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_017",
            "buffer_data": [
                # Position         UV
                18, -2, 54,       0, uv,  # Bottom Left
                18, 6,  54,        0, 0,   # Top Left
                18, -2, 42,        uv, uv,  # Bottom Right
                18, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_018",
            "buffer_data": [
                # Position         UV
                -18, -2, 54,       0, uv,  # Bottom Left
                -18, 6, 54,        0, 0,   # Top Left
                -18, -2, 66,        uv, uv,  # Bottom Right
                -18, 6, 66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_019",
            "buffer_data": [
                # Position         UV
                18, -2, 54,       0, uv,  # Bottom Left
                18, 6,  54,        0, 0,   # Top Left
                18, -2, 66,        uv, uv,  # Bottom Right
                18, 6, 66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_020",
            "buffer_data": [
                # Position         UV
                -4, -2, 30,       0, uv,  # Bottom Left
                -4, 6, 30,        0, 0,   # Top Left
                4, -2, 30,        uv, uv,  # Bottom Right
                4, 6, 30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_021",
            "buffer_data": [
                # Position         UV
                4, -2, 42,       0, uv,  # Bottom Left
                4, 6, 42,        0, 0,   # Top Left
                12, -2, 42,        uv, uv,  # Bottom Right
                12, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_022",
            "buffer_data": [
                # Position         UV
                -4, -2, 42,       0, uv,  # Bottom Left
                -4, 6, 42,        0, 0,   # Top Left
                -12, -2, 42,        uv, uv,  # Bottom Right
                -12, 6, 42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_023",
            "buffer_data": [
                # Position         UV
                -4, -2, 54,       0, uv,  # Bottom Left
                -4, 6, 54,        0, 0,   # Top Left
                4, -2, 54,        uv, uv,  # Bottom Right
                4, 6, 54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_024",
            "buffer_data": [
                # Position         UV
                6, -2, 66,       0, uv,  # Bottom Left
                6, 6, 66,        0, 0,   # Top Left
                18, -2, 66,        uv, uv,  # Bottom Right
                18, 6, 66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_025",
            "buffer_data": [
                # Position         UV
                -6, -2, 66,       0, uv,  # Bottom Left
                -6, 6, 66,        0, 0,   # Top Left
                -18, -2, 66,        uv, uv,  # Bottom Right
                -18, 6, 66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_026",
            "buffer_data": [
                # Position         UV
                18, -2, 66,       0, uv,  # Bottom Left
                18, 6, 66,        0, 0,   # Top Left
                18, -2, 78,        uv, uv,  # Bottom Right
                18, 6, 78,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_027",
            "buffer_data": [
                # Position         UV
                -18, -2, 66,       0, uv,  # Bottom Left
                -18, 6, 66,        0, 0,   # Top Left
                -18, -2, 78,        uv, uv,  # Bottom Right
                -18, 6, 78,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_028",
            "buffer_data": [
                # Position         UV
                6, -2, 78,       0, uv,  # Bottom Left
                6, 6, 78,        0, 0,   # Top Left
                18, -2, 78,        uv, uv,  # Bottom Right
                18, 6, 78,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_029",
            "buffer_data": [
                # Position         UV
                -6, -2, 78,       0, uv,  # Bottom Left
                -6, 6, 78,        0, 0,   # Top Left
                -18, -2, 78,        uv, uv,  # Bottom Right
                -18, 6, 78,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_030",
            "buffer_data": [
                # Position         UV
                6, -2, 78,       0, uv,  # Bottom Left
                6, 6, 78,        0, 0,   # Top Left
                -6, -2, 78,        uv, uv,  # Bottom Right
                -6, 6, 78,         uv, 0,  # Top Right
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
                -6, -2, -18,       0, 1,  # Bottom Left
                -6, 6, -18,        0, 0,   # Top Left
                6, -2, -18,        1, 1,  # Bottom Right
                6, 6, -18,         1, 0,  # Top Right
            ],
        },
        {
            "name": "green_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "condition": "room1_dead",  # This door opens when the player completes room 1
            "texture": 3,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, 66,       0, 1,  # Bottom Left
                -6, 6, 66,        0, 0,   # Top Left
                 6, -2, 66,        1, 1,  # Bottom Right
                 6, 6, 66,         1, 0,  # Top Right
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
        
    ]
    return []


def get_Enemies(game, program):
    enemies = [
        
        
    ]
    return enemies

def get_buttons(program):
    buttons = [
        {
            "name": "button_001",
            "id": 20,
            "program": program,
            "position": Vec3(24, -2, 0),
            "rotation": Vec3(0, 0, 0),
            "active": True,
            "action": "open_door",
            "target": "red_door_001"
        }
    ]
    return []

def room_triggers():
    """Get the room triggers for the level.
    These are used to change the room when the player enters a specific area.
    """
    triggers = [
        {
            "name": "room_trigger_001",
            "buffer_data": [
                # Position         UV
                -6, -2, -18,       0, 1,  # Bottom Left
                -6, 6, -18,        0, 0,   # Top Left
                6, -2, -18,        1, 1,  # Bottom Right
                6, 6, -18,         1, 0,  # Top Right
            ],
            "room": 1,
        },
        {
            "name": "room_trigger_002",
            "buffer_data": [
                # Position         UV
                -16, -2, -42,       0, 1,  # Bottom Left
                -16, 6, -42,        0, 0,   # Top Left
                -14, -2, -30,       1, 1,  # Bottom Right
                -14, 6, -30,        1, 0,  # Top Right
            ],
            "room": 2,
        },
        {
            "name": "room_trigger_003",
            "buffer_data": [
                # Position         UV
                -42, -2, -45,       0, 1,  # Bottom Left
                -42, 6, -45,        0, 0,   # Top Left
                -30, -2, -45,       1, 1,  # Bottom Right
                -30, 6, -45,        1, 0,  # Top Right
            ],
            "room": 3,
        }
    ]
    return []
    

def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(0, 1, -48),
        "destination": 3,
    }
    return exit


