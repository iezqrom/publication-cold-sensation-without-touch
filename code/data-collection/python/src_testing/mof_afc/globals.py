temp = -1
indx0, indy0 = 1, 1
current_device = "colther"
amount = 10000
centreROI = 1, 2
light = 3

frames = []

grid_heights = {
    "1": 48995 + 2000 + 18373 + 15748,
    "2": 47995 + 2000 + 15748 + 10499,
    "3": 52095 + 2000 + 10499 + 15748 - 5249,
    "4": 35995 + 2000 + 18373 + 15748,
    "5": 42995 + 2000 + 15748,
    "6": 46995 + 2000 + 10499 + 15748 - 5249,
    "7": 31995 + 2000 + 18373 + 15748,
    "8": 37995 + 2000 + 15748,
    "9": 44995 + 3000 + 10499 + 15748 - 5249,
}

positions = {
    "colther": {"x": 281014, "y": 229834 + 10079 + 10079 / 2, "z": 0},
    "camera": {
        "x": 341759 + 52493 + 7874 * 4 + 5249 * 2,
        "y": 331260 - 23622 - 7874 - 7874,
        "z": 0,
    },
    "tactile": {
        "x": 71633 + 52493 + 13123 + 7874 * 3 + 5249 * 2,
        "y": 475761 + 7874 - 7874,
        "z": 0,
    },
}

dry_ice_pos = {"x": 0, "y": 290000, "z": 0}

grid = {"colther": None, "camera": None, "tactile": None}

# For dict of zabers
axes = {
    "colther": ["x", "y", "z"],
    "camera": ["y", "x", "z"],
    "tactile": ["x", "y", "z"],
}

# Order of movement
haxes = {
    "colther": ["z", "x", "y"],
    "camera": ["x", "y", "z"],
    "tactile": ["y", "x", "z"],
}

ROIs = {}

stimulus = 0
timeout = 2
momen = 0

delta = 0

pid_out = 0
pos_zaber = None

step_sizes = {"colther": 0.49609375, "camera": 0.1905, "tactile": 0.1905}

coor_cells = {
    "1": (1, 1),
    "2": (1, 2),
    "3": (1, 3),
    "4": (2, 1),
    "5": (2, 2),
    "6": (2, 3),
    "7": (3, 1),
    "8": (3, 2),
    "9": (3, 3),
}

rules = {
    "colther": {"x": True, "y": True, "z": True},
    "camera": {"x": False, "y": True, "z": True},
    "tactile": {"x": False, "y": True, "z": True},
}

answer = None
answered = None

temp = 32
pid_out = 0
current = 0

dummy = True


pos_init = {"x": 300000 - 18142 - 3024 * 2, "y": 90000, "z": 0}
pos_knuckle = {"x": 300000, "y": 180000, "z": 0}
pos_centre = {"x": 250000, "y": 240472, "z": 0}

hypothesis = None
listened = None
confidence = None

lamp = 0
