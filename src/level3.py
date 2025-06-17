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
                18, -2, 78,       0, uv,  # Bottom Left
                18, 6, 78,        0, 0,   # Top Left
                18, -2, 90,        uv, uv,  # Bottom Right
                18, 6, 90,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_029",
            "buffer_data": [
                # Position         UV
                -18, -2, 78,       0, uv,  # Bottom Left
                -18, 6, 78,        0, 0,   # Top Left
                -18, -2, 90,        uv, uv,  # Bottom Right
                -18, 6, 90,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_030",
            "buffer_data": [
                # Position         UV
                6, -2, 90,       0, uv,  # Bottom Left
                6, 6, 90,        0, 0,   # Top Left
                18, -2, 90,        uv, uv,  # Bottom Right
                18, 6, 90,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_031",
            "buffer_data": [
                # Position         UV
                -6, -2, 90,       0, uv,  # Bottom Left
                -6, 6, 90,        0, 0,   # Top Left
                -18, -2, 90,        uv, uv,  # Bottom Right
                -18, 6, 90,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_032",
            "buffer_data": [
                # Position         UV
                6, -2, 90,       0, uv,  # Bottom Left
                6, 6, 90,        0, 0,   # Top Left
                -6, -2, 90,        uv, uv,  # Bottom Right
                -6, 6, 90,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_033",
            "buffer_data": [
                # Position         UV
                -18, -2, -18,       0, uv,  # Bottom Left
                -18, 6, -18,        0, 0,   # Top Left
                -18, -2, -30,        uv, uv,  # Bottom Right
                -18, 6, -30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_034",
            "buffer_data": [
                # Position         UV
                18, -2, -18,       0, uv,  # Bottom Left
                18, 6, -18,        0, 0,   # Top Left
                18, -2, -30,        uv, uv,  # Bottom Right
                18, 6, -30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_035",
            "buffer_data": [
                # Position         UV
                -18, -2, -42,       0, uv,  # Bottom Left
                -18, 6, -42,        0, 0,   # Top Left
                -18, -2, -30,        uv, uv,  # Bottom Right
                -18, 6, -30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_036",
            "buffer_data": [
                # Position         UV
                18, -2, -18,       0, uv,  # Bottom Left
                18, 6, -18,        0, 0,   # Top Left
                18, -2, -42,        uv, uv,  # Bottom Right
                18, 6, -42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_037",
            "buffer_data": [
                # Position         UV
                6, -2, -42,       0, uv,  # Bottom Left
                6, 6, -42,        0, 0,   # Top Left
                18, -2, -42,        uv, uv,  # Bottom Right
                18, 6, -42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_038",
            "buffer_data": [
                # Position         UV
                -6, -2, -42,       0, uv,  # Bottom Left
                -6, 6, -42,        0, 0,   # Top Left
                -18, -2, -42,        uv, uv,  # Bottom Right
                -18, 6, -42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_039",
            "buffer_data": [
                # Position         UV
                -6, -2, -42,       0, uv,  # Bottom Left
                -6, 6, -42,        0, 0,   # Top Left
                -6, -2, -54,        uv, uv,  # Bottom Right
                -6, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_040",
            "buffer_data": [
                # Position         UV
                6, -2, -42,       0, uv,  # Bottom Left
                6, 6, -42,        0, 0,   # Top Left
                6, -2, -54,        uv, uv,  # Bottom Right
                6, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_041",
            "buffer_data": [
                # Position         UV
                -6, -2, -54,       0, uv,  # Bottom Left
                -6, 6, -54,        0, 0,   # Top Left
                6, -2, -54,        uv, uv,  # Bottom Right
                6, 6, -54,         uv, 0,  # Top Right
            ],
        },


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
        },
        {
            "name": "green_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "condition": "room3_dead",  # This door opens when the player completes room 3
            "texture": 3,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, -42,       0, 1,  # Bottom Left
                -6, 6, -42,        0, 0,   # Top Left
                6, -2, -42,        1, 1,  # Bottom Right
                6, 6, -42,         1, 0,  # Top Right
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
        # FIRST ROOM ENEMIES
        {
            "name": "enemy1_001",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(0, -2, 24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_002",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(0, -2, 36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_003",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(9, -2, 36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_004",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-9, -2, 36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_005",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(0, -2, 48), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_001",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(9, -2, 48), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_002",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-9, -2, 48), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_003",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, 60), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_003",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(12, -2, 60), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        # SECOND ROOM ENEMIES
        {
            "name": "enemy3_001",
            "type": 3,
            "room": 2,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(0, -2, 82), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        # THIRD ROOM ENEMIES
        {
            "name": "enemy1_006",
            "type": 1,
            "room": 3,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(0, -2, -34), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_007",
            "type": 1,
            "room": 3,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(8, -2, -36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_008",
            "type": 1,
            "room": 3,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-8, -2, -36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_004",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(8, -2, -38), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_005",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-8, -2, -38), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_002",
            "type": 3,
            "room": 3,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(10, -2, -38), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_002",
            "type": 3,
            "room": 3,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(-10, -2, -38), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        

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
                -18, -2, 8,       0, 1,  # Bottom Left
                -18, 6, 8,        0, 0,   # Top Left
                18, -2, 8,        1, 1,  # Bottom Right
                18, 6, 8,         1, 0,  # Top Right
            ],
            "room": 1,
        },
        {
            "name": "room_trigger_002",
            "buffer_data": [
                # Position         UV
                -6, -2, 68,       0, 1,  # Bottom Left
                -6, 6, 68,        0, 0,   # Top Left
                6, -2, 68,        1, 1,  # Bottom Right
                6, 6, 68,         1, 0,  # Top Right
            ],
            "room": 2,
        },
        {
            "name": "room_trigger_003",
            "buffer_data": [
                # Position         UV
                -6, -2, -20,       0, 1,  # Bottom Left
                -6, 6, -20,        0, 0,   # Top Left
                6, -2, -20,        1, 1,  # Bottom Right
                6, 6, -20,         1, 0,  # Top Right
            ],
            "room": 3,
        }
    ]
    return triggers


def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(0, 1, -48),
        "destination": 3,
    }
    return exit
