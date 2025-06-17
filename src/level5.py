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
            "name": "green_door_001",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 3,
            "condition": "room1_dead",  
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, 30,       0, 1,  # Bottom Left
                -6, 6, 30,        0, 0,   # Top Left
                6, -2, 30,        1, 1,  # Bottom Right
                6, 6, 30,         1, 0,  # Top Right
            ],
        },
        {
            "name": "green_door_002",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 3,
            "condition": "room2_dead",
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                30, -2, -6,       0, 1,  # Bottom Left
                30, 6,  -6,        0, 0,   # Top Left
                30, -2, 6,        1, 1,  # Bottom Right
                30, 6, 6,         1, 0,  # Top Right
            ],
        },
        {
            "name": "green_door_003",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 3,
            "condition": "room3_dead",
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -30, -2, -6,       0, 1,  # Bottom Left
                -30, 6,  -6,        0, 0,   # Top Left
                -30, -2, 6,        1, 1,  # Bottom Right
                -30, 6, 6,         1, 0,  # Top Right
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
                -6, -2, -30,       0, 1,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                6, -2, -30,        1, 1,  # Bottom Right
                6, 6, -30,         1, 0,  # Top Right
            ],
        },
        {
            "name": "red_door_002",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 4,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -6, -2, 30,       0, 1,  # Bottom Left
                -6, 6, 30,        0, 0,   # Top Left
                6, -2, 30,        1, 1,  # Bottom Right
                6, 6, 30,         1, 0,  # Top Right
            ],
        },
        {
            "name": "red_door_003",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 4,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                30, -2, -6,       0, 1,  # Bottom Left
                30, 6,  -6,        0, 0,   # Top Left
                30, -2, 6,        1, 1,  # Bottom Right
                30, 6, 6,         1, 0,  # Top Right
            ],
        },
        {
            "name": "red_door_004",
            "lock": True,
            "program": program,  # Use the passed program
            "texture": 4,
            "opacity": .9,
            "buffer_data": [
                # Position         UV
                -30, -2, -6,       0, 1,  # Bottom Left
                -30, 6,  -6,        0, 0,   # Top Left
                -30, -2, 6,        1, 1,  # Bottom Right
                -30, 6, 6,         1, 0,  # Top Right
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
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(12, -2, -24), 100, Vec3(0, 0, 0)),
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
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(12, -2, 24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_004",
            "type": 1,
            "room": 1,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, 24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_001",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(16, -2, -28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_002",
            "type": 2,
            "room": 1,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-16, -2, -28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        # SECOND ROOM ENEMIES
        {
            "name": "enemy1_001",
            "type": 1,
            "room": 2,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(12, -2, -24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_002",
            "type": 1,
            "room": 2,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, -24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_003",
            "type": 1,
            "room": 2,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(12, -2, 24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy1_004",
            "type": 1,
            "room": 2,
            "object": enemy.Enemy1(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, 24), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_001",
            "type": 2,
            "room": 2,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(16, -2, -28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_002",
            "type": 2,
            "room": 2,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-16, -2, -28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_001",
            "type": 3,
            "room": 2,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(16, -2, 28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_002",
            "type": 3,
            "room": 2,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(-16, -2, 28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        # THIRD ROOM ENEMIES
        {
            "name": "enemy2_001",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(16, -2, -28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_002",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-16, -2, -28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_003",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(16, -2, 28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy2_004",
            "type": 2,
            "room": 3,
            "object": enemy.Enemy2(game, get_walls(), get_enemy_walls(), Vec3(-16, -2, 28), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_001",
            "type": 3,
            "room": 3,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(12, -2, 20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_002",
            "type": 3,
            "room": 3,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, 20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_003",
            "type": 3,
            "room": 3,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(12, -2, -20), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
        {
            "name": "enemy3_004",
            "type": 3,
            "room": 3,
            "object": enemy.Enemy3(game, get_walls(), get_enemy_walls(), Vec3(-12, -2, -20), 100, Vec3(0, 0, 0)),
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
            "position": Vec3(0, -2, -12),
            "rotation": Vec3(0, 0, 0),
            "active": True,
            "action": "open_door",
            "target": "red_door_002"
        },
        {
            "name": "button_002",
            "id": 20,
            "program": program,
            "position": Vec3(0, -2, 36),
            "rotation": Vec3(0, 0, 0),
            "active": True,
            "action": "open_door",
            "target": "red_door_003"
        },
        {
            "name": "button_003",
            "id": 20,
            "program": program,
            "position": Vec3(36, -2, 0),
            "rotation": Vec3(0, 0, 0),
            "active": True,
            "action": "open_door",
            "target": "red_door_004"
        },
        {
            "name": "button_004",
            "id": 20,
            "program": program,
            "position": Vec3(-36, -2, 0),
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
                -3, -2, -15,       0, 1,  # Bottom Left
                -3, 6, -15,        0, 0,   # Top Left
                3, -2, -9,        1, 1,  # Bottom Right
                3, 6, -9,         1, 0,  # Top Right
            ],
            "room": 1,
        },
        {
            "name": "room_trigger_002",
            "buffer_data": [
                # Position         UV
                -3, -2, 39,       0, 1,  # Bottom Left
                -3, 6, 39,        0, 0,   # Top Left
                3, -2, 33,        1, 1,  # Bottom Right
                3, 6, 33,         1, 0,  # Top Right
            ],
            "room": 2,
        },
        {
            "name": "room_trigger_003",
            "buffer_data": [
                # Position         UV
                39, -2, -3,       0, 1,  # Bottom Left
                39, 6, -3,        0, 0,   # Top Left
                36, -2, 3,        1, 1,  # Bottom Right
                36, 6, 3,         1, 0,  # Top Right
            ],
            "room": 3,
        },
        {
            "name": "room_trigger_004",
            "buffer_data": [
                # Position         UV
                -39, -2, -3,       0, 1,  # Bottom Left
                -39, 6, -3,        0, 0,   # Top Left
                -36, -2, 3,        1, 1,  # Bottom Right
                -36, 6, 3,         1, 0,  # Top Right
            ],
            "room": 4,
        },
    ]
    return triggers


def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(0, 1, -36),
        "destination": 6,
    }
    return exit
