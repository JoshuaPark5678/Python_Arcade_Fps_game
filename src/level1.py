import arcade
from pyglet.math import Mat4, Vec3
def get_Enemies(program):
    enemies = [
        {
            "name": "enemy1_001",
            "program": program,
            "id": 10,
            "buffer_data": Vec3(0, -2, -20),
            "rotation": Vec3(0, 0, 0),
        }
    ]
    return enemies
def get_walls(program):
    uv = 2
    walls = [
        {
            "name": "wall_001",
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
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
            "program": program,  # Use the passed program
            "texture": 1,
            "buffer_data": [
                # Position         UV
                28, -2, -4,       0, uv,  # Bottom Left
                28, 6, -4,        0, 0,   # Top Left
                40, -2, -4,       uv, uv,  # Bottom Right
                40, 6, -4,        uv, 0,  # Top Right
            ],
        },
    ]
    return walls