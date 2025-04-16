def get_walls(program):
    uv = 2
    walls = [
        {
            "name": "wall1",
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
            "name": "wall2",
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
            "name": "wall3",
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
            "name": "wall4",
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
            "name": "wall5",
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
            "name": "wall6",
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
            "name": "wall7",
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
            "name": "wall8",
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
            "name": "wall9",
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
            "name": "wall10",
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
            "name": "wall11",
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
            "name": "wall12",
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
            "name": "wall13",
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
            "name": "wall14",
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
            "name": "wall15",
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
            "name": "wall16",
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
            "name": "wall17",
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
            "name": "wall18",
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
            "name": "wall19",
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
            "name": "wall20",
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
            "name": "wall21",
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
            "name": "wall22",
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
            "name": "wall23",
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
            "name": "wall24",
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
            "name": "wall25",
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
            "name": "wall26",
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
            "name": "wall27",
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
            "name": "wall28",
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