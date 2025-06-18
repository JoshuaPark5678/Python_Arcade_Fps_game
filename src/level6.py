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
                -6, -2, 6,       0, uv,  # Bottom Left
                -6, 6, 6,        0, 0,   # Top Left
                6, -2, 6,        uv, uv,  # Bottom Right
                6, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_002",
            "buffer_data": [
                # Position         UV
                -6, -2, -6,       0, uv,  # Bottom Left
                -6, 6, -6,        0, 0,   # Top Left
                -6, -2, 6,        uv, uv,  # Bottom Right
                -6, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_003",
            "buffer_data": [
                # Position         UV
                6, -2, -6,       0, uv,  # Bottom Left
                6, 6, -6,        0, 0,   # Top Left
                6, -2, 6,        uv, uv,  # Bottom Right
                6, 6, 6,         uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_004",
            "buffer_data": [
                # Position         UV
                -6, -2, -6,       0, uv,  # Bottom Left
                -6, 6, -6,        0, 0,   # Top Left
                -18, -2, -6,      uv, uv,  # Bottom Right
                -18, 6, -6,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_005",
            "buffer_data": [
                # Position         UV
                6, -2, -6,       0, uv,  # Bottom Left
                6, 6, -6,        0, 0,   # Top Left
                18, -2, -6,      uv, uv,  # Bottom Right
                18, 6, -6,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_006",
            "buffer_data": [
                # Position         UV
                -18, -2, -6,       0, uv,  # Bottom Left
                -18, 6, -6,        0, 0,   # Top Left
                -18, -2, -18,      uv, uv,  # Bottom Right
                -18, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_007",
            "buffer_data": [
                # Position         UV
                -18, -2, -18,      0, uv,  # Bottom Left
                -18, 6, -18,       0, 0,   # Top Left
                -18, -2, -30,      uv, uv,  # Bottom Right
                -18, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_008",
            "buffer_data": [
                # Position         UV
                18, -2, -6,        0, uv,  # Bottom Left
                18, 6, -6,         0, 0,   # Top Left
                18, -2, -18,       uv, uv,  # Bottom Right
                18, 6, -18,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_009",
            "buffer_data": [
                # Position         UV
                18, -2, -18,       0, uv,  # Bottom Left
                18, 6, -18,        0, 0,   # Top Left
                18, -2, -30,       uv, uv,  # Bottom Right
                18, 6, -30,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_010",
            "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, uv,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                -18, -2, -30,      uv, uv,  # Bottom Right
                -18, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_011",
            "buffer_data": [
                # Position         UV
                6, -2, -30,       0, uv,  # Bottom Left
                6, 6, -30,        0, 0,   # Top Left
                18, -2, -30,      uv, uv,  # Bottom Right
                18, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_012",
            "buffer_data": [
                # Position         UV
                -6, -2, -30,       0, uv,  # Bottom Left
                -6, 6, -30,        0, 0,   # Top Left
                -6, -2, -42,       uv, uv,  # Bottom Right
                -6, 6, -42,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_013",
            "buffer_data": [
                # Position         UV
                -6, -2, -42,       0, uv,  # Bottom Left
                -6, 6, -42,        0, 0,   # Top Left
                -6, -2, -54,       uv, uv,  # Bottom Right
                -6, 6, -54,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_014",
            "buffer_data": [
                # Position         UV
                -6, -2, -54,       0, uv,  # Bottom Left
                -6, 6, -54,        0, 0,   # Top Left
                -6, -2, -66,       uv, uv,  # Bottom Right
                -6, 6, -66,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_015",
            "buffer_data": [
                # Position         UV
                -6, -2, -66,       0, uv,  # Bottom Left
                -6, 6, -66,        0, 0,   # Top Left
                6, -2, -66,       uv, uv,  # Bottom Right
                6, 6, -66,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_016",
            "buffer_data": [
                # Position         UV
                6, -2, -66,       0, uv,  # Bottom Left
                6, 6, -66,        0, 0,   # Top Left
                18, -2, -66,       uv, uv,  # Bottom Right
                18, 6, -66,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_017",
            "buffer_data": [
                # Position         UV
                30, -2, -30,       0, uv,  # Bottom Left
                30, 6, -30,        0, 0,   # Top Left
                18, -2, -30,      uv, uv,  # Bottom Right
                18, 6, -30,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_018",
            "buffer_data": [
                # Position         UV
                42, -2, -30,       0, uv,  # Bottom Left
                42, 6, -30,        0, 0,   # Top Left
                42, -2, -18,      uv, uv,  # Bottom Right
                42, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_019",
            "buffer_data": [
                # Position         UV
                42, -2, -30,       0, uv,  # Bottom Left
                42, 6, -30,        0, 0,   # Top Left
                42, -2, -42,      uv, uv,  # Bottom Right
                42, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_020",
            "buffer_data": [
                # Position         UV
                18, -2, -6,        0, uv,  # Bottom Left
                18, 6, -6,         0, 0,   # Top Left
                18, -2, 6,       uv, uv,  # Bottom Right
                18, 6, 6,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_021",
            "buffer_data": [
                # Position         UV
                18, -2, 6,        0, uv,  # Bottom Left
                18, 6, 6,         0, 0,   # Top Left
                30, -2, 6,       uv, uv,  # Bottom Right
                30, 6, 6,        uv, 0,  # Top Right
            ],
        },
        {
        
            "name": "wall_022",
            "buffer_data": [
                # Position         UV
                42, -2, 6,        0, uv,  # Bottom Left
                42, 6, 6,         0, 0,   # Top Left
                30, -2, 6,       uv, uv,  # Bottom Right
                30, 6, 6,        uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_023",
            "buffer_data": [
                # Position         UV
                42, -2, -6,       0, uv,  # Bottom Left
                42, 6, -6,        0, 0,   # Top Left
                42, -2, -18,      uv, uv,  # Bottom Right
                42, 6, -18,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_024",
            "buffer_data": [
                # Position         UV
                42, -2, -6,       0, uv,  # Bottom Left
                42, 6, -6,        0, 0,   # Top Left
                42, -2, 6,      uv, uv,  # Bottom Right
                42, 6, 6,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_025",
            "buffer_data": [
                # Position         UV
                42, -2, -54,       0, uv,  # Bottom Left
                42, 6, -54,        0, 0,   # Top Left
                42, -2, -66,      uv, uv,  # Bottom Right
                42, 6, -66,       uv, 0,  # Top Right
            ],
        },
         {
            "name": "wall_025",
            "buffer_data": [
                # Position         UV
                42, -2, -54,       0, uv,  # Bottom Left
                42, 6, -54,        0, 0,   # Top Left
                42, -2, -42,      uv, uv,  # Bottom Right
                42, 6, -42,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_026",
            "buffer_data": [
                # Position         UV
                42, -2, -78,       0, uv,  # Bottom Left
                42, 6, -78,        0, 0,   # Top Left
                42, -2, -66,      uv, uv,  # Bottom Right
                42, 6, -66,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_027",
            "buffer_data": [
                # Position         UV
                30, -2, -66,       0, uv,  # Bottom Left
                30, 6, -66,        0, 0,   # Top Left
                18, -2, -66,       uv, uv,  # Bottom Right
                18, 6, -66,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_028",
            "buffer_data": [
                # Position         UV
                42, -2, -78,       0, uv,  # Bottom Left
                42, 6, -78,        0, 0,   # Top Left
                42, -2, -90,      uv, uv,  # Bottom Right
                42, 6, -90,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_029",
            "buffer_data": [
                # Position         UV
                42, -2, -102,       0, uv,  # Bottom Left
                42, 6, -102,        0, 0,   # Top Left
                42, -2, -90,      uv, uv,  # Bottom Right
                42, 6, -90,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_030",
            "buffer_data": [
                # Position         UV
                42, -2, -102,       0, uv,  # Bottom Left
                42, 6, -102,        0, 0,   # Top Left
                30, -2, -102,      uv, uv,  # Bottom Right
                30, 6, -102,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_031",
            "buffer_data": [
                # Position         UV
                18, -2, -102,       0, uv,  # Bottom Left
                18, 6, -102,        0, 0,   # Top Left
                30, -2, -102,      uv, uv,  # Bottom Right
                30, 6, -102,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_032",
            "buffer_data": [
                # Position         UV
                18, -2, -102,       0, uv,  # Bottom Left
                18, 6, -102,        0, 0,   # Top Left
                6, -2, -102,      uv, uv,  # Bottom Right
                6, 6, -102,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_033",
            "buffer_data": [
                # Position         UV
                -6, -2, -102,       0, uv,  # Bottom Left
                -6, 6, -102,        0, 0,   # Top Left
                6, -2, -102,      uv, uv,  # Bottom Right
                6, 6, -102,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_034",
            "buffer_data": [
                # Position         UV
                -6, -2, -102,       0, uv,  # Bottom Left
                -6, 6, -102,        0, 0,   # Top Left
                -6, -2, -90,      uv, uv,  # Bottom Right
                -6, 6, -90,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_035",
            "buffer_data": [
                # Position         UV
                -6, -2, -78,       0, uv,  # Bottom Left
                -6, 6, -78,        0, 0,   # Top Left
                -6, -2, -90,      uv, uv,  # Bottom Right
                -6, 6, -90,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_035",
            "buffer_data": [
                # Position         UV
                -6, -2, -66,       0, uv,  # Bottom Left
                -6, 6, -66,        0, 0,   # Top Left
                -6, -2, -78,      uv, uv,  # Bottom Right
                -6, 6, -78,       uv, 0,  # Top Right
            ],
        },
        {
            "name": "wall_036",
            "buffer_data": [
                # Position         UV
                -6, -2, -66,       0, uv,  # Bottom Left
                -6, 6, -66,        0, 0,   # Top Left
                -6, -2, -54,      uv, uv,  # Bottom Right
                -6, 6, -54,       uv, 0,  # Top Right
            ],
        },
    ]
        
    return walls


def get_doors(program):
    doors = [
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
        # FINAL BOSS
        {
            "name": "final_boss",
            "phase": 1,
            "type": 5,
            "room": 1,
            "object": enemy.FinalBoss(game, get_walls(), get_enemy_walls(), Vec3(32, -2, -48), 100, Vec3(0, 0, 0)),
            "program": program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
        },
    ]
    return enemies


def get_buttons(program):
    buttons = [
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
                6, -2, -30,       0, 1,  # Bottom Left
                6, 6, -30,        0, 0,   # Top Left
                8, -2, -64,        1, 1,  # Bottom Right
                8, 6, -64,         1, 0,  # Top Right
            ],
            "room": 1,
        },
    ]
    return triggers


def get_exit():
    exit = {
        "name": "exit_001",
        "model": Vec3(60, 1, -60),
        "destination": 6,
    }
    return exit
