temp = -1
indx0, indy0 = 1, 1
current_device = "colther"
amount = 10000
centreROI = 1, 2
light = 3

positions = {
    "colther": {"x": 250000, "y": 240472, "z": 0},
    "camera": {"x": 430000, "y": 240000, "z": 0},
    "tactile": {"x": 0, "y": 0, "z": 0},
}

dry_ice_pos = {"x": 0, "y": 290000, "z": 0}

grid = {"colther": None, "camera": None, "tactile": None}

# For dict of zabers
axes = {
    "colther": ["x", "y", "z"],
    "camera": ["y", "x", "z"],
    "tactile": ["y", "x", "z"],
}

# Order of movement
haxes = {
    "colther": ["z", "x", "y"],
    "tactile": ["y", "x", "z"],
    "camera": ["x", "y", "z"],
}

ROIs = {}

stimulus = 0
timeout = 2
momen = 0

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


pos_init = {"x": 300000, "y": 90000, "z": 0}
pos_knuckle = {"x": 300000, "y": 180000, "z": 0}
pos_centre = {"x": 250000, "y": 240472, "z": 0}
