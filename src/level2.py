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
        },
        {
            "name": "wall_0022",
            "buffer_data": [
                # Position         UV
                -18, -2, -42,       0, uv,  # Bottom Left
                -18, 6, -42,        0, 0,   # Top Left
                -30, -2, -42,      uv, uv,  # Bottom Right
                -30, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0023",
            "buffer_data": [
                # Position         UV
                -42, -2, -30,       0, uv,  # Bottom Left
                -42, 6, -30,        0, 0,   # Top Left
                -42, -2, -42,      uv, uv,  # Bottom Right
                -42, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0024",
            "buffer_data": [
                # Position         UV
                -42, -2, -30,       0, uv,  # Bottom Left
                -42, 6, -30,        0, 0,   # Top Left
                -42, -2, -18,      uv, uv,  # Bottom Right
                -42, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0025",
            "buffer_data": [
                # Position         UV
                -42, -2, -18,       0, uv,  # Bottom Left
                -42, 6, -18,        0, 0,   # Top Left
                -42, -2, -6,      uv, uv,  # Bottom Right
                -42, 6, -6,       uv, 0,  # Top Right
            ],
        },
        {            
            "name": "wall_0027",
            "buffer_data": [
                # Position         UV
                -42, -2, -6,       0, uv,  # Bottom Left
                -42, 6, -6,        0, 0,   # Top Left
                -30, -2, -6,      uv, uv,  # Bottom Right
                -30, 6, -6,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0028",
            "buffer_data": [
                # Position         UV
                -30, -2, -6,       0, uv,  # Bottom Left
                -30, 6, -6,        0, 0,   # Top Left
                -18, -2, -6,      uv, uv,  # Bottom Right
                -18, 6, -6,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_0029",
            "buffer_data": [
                # Position         UV
                -18, -2, -6,       0, uv,  # Bottom Left
                -18, 6, -6,        0, 0,   # Top Left
                -6, -2, -6,      uv, uv,  # Bottom Right
                -6, 6, -6,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0030",
            "buffer_data": [
                # Position         UV
                -42, -2, -42,       0, uv,  # Bottom Left
                -42, 6, -42,        0, 0,   # Top Left
                -42, -2, -54,      uv, uv,  # Bottom Right
                -42, 6, -54,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0031",
            "buffer_data": [
                # Position         UV
                -42, -2, -54,       0, uv,  # Bottom Left
                -42, 6, -54,        0, 0,   # Top Left
                -42, -2, -66,      uv, uv,  # Bottom Right
                -42, 6, -66,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0032",
            "buffer_data": [
                # Position         UV
                -42, -2, -66,       0, uv,  # Bottom Left
                -42, 6, -66,        0, 0,   # Top Left
                -42, -2, -78,      uv, uv,  # Bottom Right
                -42, 6, -78,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0033",
            "buffer_data": [
                # Position         UV
                -42, -2, -78,       0, uv,  # Bottom Left
                -42, 6, -78,        0, 0,   # Top Left
                -30, -2, -78,      uv, uv,  # Bottom Right
                -30, 6, -78,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0034",
            "buffer_data": [
                # Position         UV
                -30, -2, -78,       0, uv,  # Bottom Left
                -30, 6, -78,        0, 0,   # Top Left
                -18, -2, -78,      uv, uv,  # Bottom Right
                -18, 6, -78,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0035",
            "buffer_data": [
                # Position         UV
                -18, -2, -78,       0, uv,  # Bottom Left
                -18, 6, -78,        0, 0,   # Top Left
                -6, -2, -78,      uv, uv,  # Bottom Right
                -6, 6, -78,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0036",
            "buffer_data": [
                # Position         UV
                -6, -2, -78,       0, uv,  # Bottom Left
                -6, 6, -78,        0, 0,   # Top Left
                -6, -2, -66,      uv, uv,  # Bottom Right
                -6, 6, -66,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0037",
            "buffer_data": [
                # Position         UV
                -6, -2, -66,       0, uv,  # Bottom Left
                -6, 6, -66,        0, 0,   # Top Left
                -6, -2, -54,      uv, uv,  # Bottom Right
                -6, 6, -54,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0038",
            "buffer_data": [
                # Position         UV
                -6, -2, -54,       0, uv,  # Bottom Left
                -6, 6, -54,        0, 0,   # Top Left
                6, -2, -54,      uv, uv,  # Bottom Right
                6, 6, -54,       uv, 0   # Top Right
            ],
        },
        {
            "name": "wall_0039",
            "buffer_data": [
                # Position         UV
                6, -2, -54,       0, uv,  # Bottom Left
                6, 6, -54,        0, 0,   # Top Left
                6, -2, -42,      uv, uv,  # Bottom Right
                6, 6, -42,       uv, 0   # Top Right
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
                -6, -2, -42,       0, 1,  # Bottom Left
                -6, 6, -42,        0, 0,   # Top Left
                -6, -2, -30,       1, 1,  # Bottom Right
                -6, 6, -30,        1, 0,  # Top Right
            ],
        },
        {
            "name": "green_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 3,
            "condition": "room2_dead",
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -42, -2, -42,       0, 1,  # Bottom Left
                -42, 6, -42,        0, 0,   # Top Left
                -30, -2, -42,       1, 1,  # Bottom Right
                -30, 6, -42,        1, 0,  # Top Right
            ],
        },
        {
            "name": "green_door_002",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 3,
            "condition": "room3_dead",
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, -54,       0, 1,  # Bottom Left
                -6, 6, -54,        0, 0,   # Top Left
                -6, -2, -42,      1, 1,  # Bottom Right
                -6, 6, -42,       1, 0   # Top Right
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
        {
            "name": "enemy_wall_001",
            "buffer_data": [
                # Position         UV
                -18, -2, -42,       0, 1,  # Bottom Left
                -18, 6, -42,        0, 0,   # Top Left
                -18, -2, -30,       1, 1,  # Bottom Right
                -18, 6, -30,        1, 0,  # Top Right
            ],
        },
        {
            "name": "enemy_wall_002",
            "buffer_data": [
                # Position         UV
                -42, -2, -42,       0, 1,  # Bottom Left
                -42, 6, -42,        0, 0,   # Top Left
                -30, -2, -42,       1, 1,  # Bottom Right
                -30, 6, -42,        1, 0,  # Top Right
            ],
        }
        
    ]
    return []


def get_Enemies(game, program):
    enemies = [
        # FIRST ROOM ENEMIES
        {
            "name": "enemy1_001",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(18, -2, -6), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_002",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(30, -2, -6), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_003",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(14, -2, -4), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_004",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(34, -2, -4), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        # SECOND ROOM ENEMIES
        {
            "name": "enemy2_001",
            "type": 2,
            "room": 2,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-40, -2, -12), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_002",
            "type": 2,
            "room": 2,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, -18), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_005",
            "type": 1,
            "room": 2,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-24, -2, -20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_006",
            "type": 1,
            "room": 2,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-30, -2, -20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_007",
            "type": 1,
            "room": 2,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-36, -2, -20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        # THIRD ROOM ENEMIES
        {
            "name": "enemy1_008",
            "type": 1,
            "room": 3,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-20, -2, -60), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_009",
            "type": 1,
            "room": 3,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-20, -2, -54), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_010",
            "type": 1,
            "room": 3,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-20, -2, -72), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_003",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-15, -2, -68), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_004",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, -52), 100, Vec3(0, 0, 0)),
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
            "position": Vec3(24, -2, 0),
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
    return triggers
    

def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(0, 1, -48),
        "destination": 3,
    }
    return exit


