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
                -6, -2, -6,       0, uv,  # Bottom Left
                -6, 6, -6,        0, 0,   # Top Left
                6, -2, -6,        uv, uv,  # Bottom Right
                6, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_002",
            "buffer_data": [
                # Position         UV
                -6, -2, -6,       0, uv,  # Bottom Left
                -6, 6, -6,        0, 0,   # Top Left
                -18, -2, -6,        uv, uv,  # Bottom Right
                -18, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_003",
            "buffer_data": [
                # Position         UV
                -6, -2, 18,       0, uv,  # Bottom Left
                -6, 6, 18,        0, 0,   # Top Left
                6, -2, 18,        uv, uv,  # Bottom Right
                6, 6, 18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_004",
            "buffer_data": [
                # Position         UV
                -6, -2, 18,       0, uv,  # Bottom Left
                -6, 6, 18,        0, 0,   # Top Left
                -6, -2, 6,        uv, uv,  # Bottom Right
                -6, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_005",
            "buffer_data": [
                # Position         UV
                6, -2, 18,       0, uv,  # Bottom Left
                6, 6, 18,        0, 0,   # Top Left
                6, -2, 6,        uv, uv,  # Bottom Right
                6, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_005",
            "buffer_data": [
                # Position         UV
                -6, -2, 6,       0, uv,  # Bottom Left
                -6, 6, 6,        0, 0,   # Top Left
                -18, -2, 6,        uv, uv,  # Bottom Right
                -18, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_006",
            "buffer_data": [
                # Position         UV
                6, -2, 6,       0, uv,  # Bottom Left
                6, 6, 6,        0, 0,   # Top Left
                18, -2, 6,        uv, uv,  # Bottom Right
                18, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_006",
            "buffer_data": [
                # Position         UV
                6, -2, 6,       0, uv,  # Bottom Left
                6, 6, 6,        0, 0,   # Top Left
                18, -2, 6,        uv, uv,  # Bottom Right
                18, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_007",
            "buffer_data": [
                # Position         UV
                18, -2, 6,       0, uv,  # Bottom Left
                18, 6, 6,        0, 0,   # Top Left
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
                -30, -2, 6,        uv, uv,  # Bottom Right
                -30, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_09",
            "buffer_data": [
                # Position         UV
                -30, -2, 6,       0, uv,  # Bottom Left
                -30, 6, 6,        0, 0,   # Top Left
                -30, -2, -6,        uv, uv,  # Bottom Right
                -30, 6, -6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_010",
            "buffer_data": [
                # Position         UV
                -30, -2, -6,       0, uv,  # Bottom Left
                -30, 6, -6,        0, 0,   # Top Left
                -30, -2, -18,        uv, uv,  # Bottom Right
                -30, 6, -18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_011",
            "buffer_data": [
                # Position         UV
                -30, -2, -18,       0, uv,  # Bottom Left
                -30, 6, -18,        0, 0,   # Top Left
                -18, -2, -18,        uv, uv,  # Bottom Right
                -18, 6, -18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "glass_wall_02",
            "texture": 5,  
            "opacity": 0.5,  # Semi-transparent glass wall
            "buffer_data": [
                # Position         UV
                -6, -2, -6,       0, 1,  # Bottom Left
                -6, 6, -6,        0, 0,   # Top Left
                -6, -2, -18,        1, 1,  # Bottom Right
                -6, 6, -18,         1, 0,  # Top Right
            ],
        },
        {
            "name": "glass_wall_02",
            "texture": 5,  
            "opacity": 0.5,  # Semi-transparent glass wall
            "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, 1,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                -6, -2, -18,        1, 1,  # Bottom Right
                -6, 6, -18,         1, 0,  # Top Right
            ],
        },
        {
            "name": "glass_wall_03",
            "texture": 5,  
            "opacity": 0.5,  # Semi-transparent glass wall
            "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, 1,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                -6, -2, -42,        1, 1,  # Bottom Right
                -6, 6, -42,         1, 0,  # Top Right
            ],
        },
        {
            "name": "wall_012",
            "buffer_data": [
                # Position         UV
                -30, -2, -30,       0, uv,  # Bottom Left
                -30, 6, -30,        0, 0,   # Top Left
                -30, -2, -18,        uv, uv,  # Bottom Right
                -30, 6, -18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_013",
            "buffer_data": [
                # Position         UV
                -30, -2, -30,       0, uv,  # Bottom Left
                -30, 6, -30,        0, 0,   # Top Left
                -30, -2, -42,        uv, uv,  # Bottom Right
                -30, 6, -42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_014",
            "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, uv,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                -18, -2, -30,        uv, uv,  # Bottom Right
                -18, 6, -30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_015",
            "buffer_data": [
                # Position         UV
                0, -2, -24,       0, uv,  # Bottom Left
                0, 6, -24,        0, 0,   # Top Left
                12, -2, -24,        uv, uv,  # Bottom Right
                12, 6, -24,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_016",
            "buffer_data": [
                # Position         UV
                18, -2, -6,       0, uv,  # Bottom Left
                18, 6, -6,        0, 0,   # Top Left
                18, -2, -18,        uv, uv,  # Bottom Right
                18, 6, -18,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_017",
            "buffer_data": [
                # Position         UV
                18, -2, -18,       0, uv,  # Bottom Left
                18, 6, -18,        0, 0,   # Top Left
                18, -2, -30,        uv, uv,  # Bottom Right
                18, 6, -30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_018",
            "buffer_data": [
                # Position         UV
                18, -2, -42,       0, uv,  # Bottom Left
                18, 6, -42,        0, 0,   # Top Left
                18, -2, -30,        uv, uv,  # Bottom Right
                18, 6, -30,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_019",
            "buffer_data": [
                # Position         UV
                6, -2, -42,       0, uv,  # Bottom Left
                6, 6, -42,        0, 0,   # Top Left
                18, -2, -42,        uv, uv,  # Bottom Right
                18, 6, -42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_020",
            "buffer_data": [
                # Position         UV
                -18, -2, -42,       0, uv,  # Bottom Left
                -18, 6, -42,        0, 0,   # Top Left
                -30, -2, -42,        uv, uv,  # Bottom Right
                -30, 6, -42,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_021",
            "buffer_data": [
                # Position         UV
                6, -2, -42,       0, uv,  # Bottom Left
                6, 6, -42,        0, 0,   # Top Left
                6, -2, -54,        uv, uv,  # Bottom Right
                6, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_022",
            "buffer_data": [
                # Position         UV
                -18, -2, -42,       0, uv,  # Bottom Left
                -18, 6, -42,        0, 0,   # Top Left
                -18, -2, -54,        uv, uv,  # Bottom Right
                -18, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_023",
            "buffer_data": [
                # Position         UV
                -6, -2, -54,       0, uv,  # Bottom Left
                -6, 6, -54,        0, 0,   # Top Left
                -18, -2, -54,        uv, uv,  # Bottom Right
                -18, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_024",
            "buffer_data": [
                # Position         UV
                -30, -2, -54,       0, uv,  # Bottom Left
                -30, 6, -54,        0, 0,   # Top Left
                -18, -2, -54,        uv, uv,  # Bottom Right
                -18, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_025",
            "buffer_data": [
                # Position         UV
                6, -2, -54,       0, uv,  # Bottom Left
                6, 6, -54,        0, 0,   # Top Left
                18, -2, -54,        uv, uv,  # Bottom Right
                18, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_026",
            "buffer_data": [
                # Position         UV
                30, -2, -54,       0, uv,  # Bottom Left
                30, 6, -54,        0, 0,   # Top Left
                18, -2, -54,        uv, uv,  # Bottom Right
                18, 6, -54,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_027",
            "buffer_data": [
                # Position         UV
                30, -2, -54,       0, uv,  # Bottom Left
                30, 6, -54,        0, 0,   # Top Left
                30, -2, -66,        uv, uv,  # Bottom Right
                30, 6, -66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_028",
            "buffer_data": [
                # Position         UV
                -30, -2, -54,       0, uv,  # Bottom Left
                -30, 6, -54,        0, 0,   # Top Left
                -30, -2, -66,        uv, uv,  # Bottom Right
                -30, 6, -66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_029",
            "buffer_data": [
                # Position         UV
                -6, -2, -70,       0, uv,  # Bottom Left
                -6, 6, -70,        0, 0,   # Top Left
                -18, -2, -70,        uv, uv,  # Bottom Right
                -18, 6, -70,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_030",
            "buffer_data": [
                # Position         UV
                6, -2, -70,       0, uv,  # Bottom Left
                6, 6, -70,        0, 0,   # Top Left
                18, -2, -70,        uv, uv,  # Bottom Right
                18, 6, -70,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_031",
            "buffer_data": [
                # Position         UV
                30, -2, -78,       0, uv,  # Bottom Left
                30, 6, -78,        0, 0,   # Top Left
                30, -2, -66,        uv, uv,  # Bottom Right
                30, 6, -66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_032",
            "buffer_data": [
                # Position         UV
                -30, -2, -78,       0, uv,  # Bottom Left
                -30, 6, -78,        0, 0,   # Top Left
                -30, -2, -66,        uv, uv,  # Bottom Right
                -30, 6, -66,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_033",
            "buffer_data": [
                # Position         UV
                30, -2, -78,       0, uv,  # Bottom Left
                30, 6, -78,        0, 0,   # Top Left
                30, -2, -80,        uv, uv,  # Bottom Right
                30, 6, -80,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_034",
            "buffer_data": [
                # Position         UV
                -30, -2, -78,       0, uv,  # Bottom Left
                -30, 6, -78,        0, 0,   # Top Left
                -30, -2, -80,        uv, uv,  # Bottom Right
                -30, 6, -80,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_033",
            "buffer_data": [
                # Position         UV
                30, -2, -92,       0, uv,  # Bottom Left
                30, 6, -92,        0, 0,   # Top Left
                30, -2, -80,        uv, uv,  # Bottom Right
                30, 6, -80,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_034",
            "buffer_data": [
                # Position         UV
                -30, -2, -92,       0, uv,  # Bottom Left
                -30, 6, -92,        0, 0,   # Top Left
                -30, -2, -80,        uv, uv,  # Bottom Right
                -30, 6, -80,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_035",
            "buffer_data": [
                # Position         UV
                30, -2, -92,       0, uv,  # Bottom Left
                30, 6, -92,        0, 0,   # Top Left
                18, -2, -92,        uv, uv,  # Bottom Right
                18, 6, -92,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_036",
            "buffer_data": [
                # Position         UV
                -30, -2, -92,       0, uv,  # Bottom Left
                -30, 6, -92,        0, 0,   # Top Left
                -18, -2, -92,        uv, uv,  # Bottom Right
                -18, 6, -92,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_037",
            "buffer_data": [
                # Position         UV
                6, -2, -92,       0, uv,  # Bottom Left
                6, 6, -92,        0, 0,   # Top Left
                18, -2, -92,        uv, uv,  # Bottom Right
                18, 6, -92,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_038",
            "buffer_data": [
                # Position         UV
                -6, -2, -92,       0, uv,  # Bottom Left
                -6, 6, -92,        0, 0,   # Top Left
                -18, -2, -92,        uv, uv,  # Bottom Right
                -18, 6, -92,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_039",
            "buffer_data": [
                # Position         UV
                -6, -2, -92,       0, uv,  # Bottom Left
                -6, 6, -92,        0, 0,   # Top Left
                -6, -2, -104,        uv, uv,  # Bottom Right
                -6, 6, -104,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_040",
            "buffer_data": [
                # Position         UV
                6, -2, -92,       0, uv,  # Bottom Left
                6, 6, -92,        0, 0,   # Top Left
                6, -2, -104,        uv, uv,  # Bottom Right
                6, 6, -104,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_041",
            "buffer_data": [
                # Position         UV
                -6, -2, -104,       0, uv,  # Bottom Left
                -6, 6, -104,        0, 0,   # Top Left
                6, -2, -104,        uv, uv,  # Bottom Right
                6, 6, -104,         uv, 0,  # Top Right
            ],
        }
    ]
    return walls


def get_doors(program):
    doors = [
        {
            "name": "green_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "condition": "room1_dead",  # This door opens when the player completes room 1
            "texture": 3,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, 6,       0, 1,  # Bottom Left
                -6, 6, 6,        0, 0,   # Top Left
                6, -2, 6,        1, 1,  # Bottom Right
                6, 6, 6,         1, 0,  # Top Right
            ],
            
        },
        {
            "name": "red_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 4,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, -54,       0, 1,  # Bottom Left
                -6, 6, -54,        0, 0,   # Top Left
                 6, -2, -54,        1, 1,  # Bottom Right
                 6, 6, -54,         1, 0,  # Top Right
            ],
        },
        {
            "name": "green_door_002",
            "lock": True,
            "program": program,  # Use the passed program
            "condition": "room2_dead",  # This door opens when the player completes room 1
            "texture": 3,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, -92,       0, 1,  # Bottom Left
                -6, 6, -92,        0, 0,   # Top Left
                6, -2, -92,        1, 1,  # Bottom Right
                6, 6, -92,         1, 0,  # Top Right
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
        {
            "name": "enemy1_001",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-24, -2, -24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_002",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, -24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_003",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, -36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_004",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-24, -2, -26), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_001",
            "type": 3,
            "room": 1,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, -18), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        # OTHER SIDE
        {
            "name": "enemy3_002",
            "type": 3,
            "room": 1,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(6, -2, -30), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_001",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(6, -2, -36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),  
        },
        {
            "name": "enemy2_002",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(10, -2, -36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),  
        },
        {
            "name": "enemy2_003",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(2, -2, -36), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),  
        },
        {
            "name": "enemy2_004",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(10, -2, -30), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),  
        },
        {
            "name": "enemy2_005",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(2, -2, -30), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),  
        },
        # ROOM 2 is a MINI BOSS ROOM
        {
            "name": "miniboss1",
            "type": 4,
            "room": 2,
            "object": enemy.Miniboss(game, get_walls(), get_enemy_walls(), Vec3(0, -2, -80), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        }
        
    ]
    return enemies


def get_buttons(program):
    buttons = [
        {
            "name": "button_001",
            "id": 20,
            "program": program,
            "position": Vec3(0, -2, 16),
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
                -30, -2, -6,       0, 1,  # Bottom Left
                -30, 6, -6,        0, 0,   # Top Left
                18, -2, -8,        1, 1,  # Bottom Right
                18, 6, -8,         1, 0,  # Top Right
            ],
            "room": 1,
        },
        {
            "name": "room_trigger_002",
            "buffer_data": [
                # Position         UV
                -8, -2, -58,       0, 1,  # Bottom Left
                -8, 6, -58,        0, 0,   # Top Left
                 8, -2, -57,        1, 1,  # Bottom Right
                 8, 6, -57,         1, 0,  # Top Right
            ],
            "room": 2,
        },
    ]
    return triggers


def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(0, 1, -96),
        "destination": 5,
    }
    return exit
