import os

local_path = os.getcwd()

default_pantilt = (44, 0, 158)  # [48, 158, 20]
PanTilts = {
    "1": (42, 63, 53),
    "2": (42, 63, 53),
    "3": (42, 63, 53),
    "4": (42, 63, 53),
    "5": (42, 63, 53),
    "6": (42, 63, 53),
    "7": (42, 63, 53),
    "8": (42, 63, 53),
    "9": (42, 63, 53),
}
pre_adjust_camera_pos = {
    "1": {"x": -4.5, "y": 5, "z": 7},
    "2": {"x": -3, "y": 7.5, "z": 8},
}
keydelay = 0.15
weDone = False

camera_up = 209974

lower_bound_delay = 0.1
higher_bound_delay = 0.4

move_platform_camera = 0
move_platform_camera_4 = 0  # 131234

current_device = "tactile"
positions = {
    "colther": {"x": 214000, "y": 108000, "z": 0},
    "camera": {"x": 50000, "y": 362604, "z": 0},
    "tactile": {"x": 369000, "y": 307000, "z": 0},
}

init_grid = {"x": 50000, "y": 800000, "z": 70000}
init_meta = {"x": 110000, "y": 170000, "z": 10000}

touch = 0

amount = 10000
vminT = 29
vmaxT = 36
init_sep = 4

grid = {"colther": None, "camera": None, "tactile": None}

touch_z_offset = 52494
tactile_y_save = 413491
base_touch = 20000
tactile_x_save = 533332

tactilex1 = 51000
tactiley1 = 450000
tactilez1 = 293000

tactilex2 = 486000
tactiley2 = 652000
tactilez2 = 268000

try:

    file_coltherx1 = open(
        f"{local_path}/data/coltherx1",
        "r",
    )
    coltherx1 = int(file_coltherx1.read())
    file_colthery1 = open(
        f"{local_path}/data/colthery1",
        "r",
    )
    colthery1 = int(file_colthery1.read())
    coltherz1 = 206000

    file_coltherx2 = open(
        f"{local_path}/data/coltherx2",
        "r",
    )
    coltherx2 = int(file_coltherx2.read())
    file_colthery2 = open(
        f"{local_path}/data/colthery2",
        "r",
    )
    colthery2 = int(file_colthery2.read())
    coltherz2 = 206000

    slopex_colther = (coltherx1 - coltherx2) / (
        tactilex1 - tactilex2
    )  # (coltherX1 - coltherX2)/(tactileX1 - tactileX2)
    yoriginx_colther = coltherx1 - (
        slopex_colther * tactilex1
    )  # (coltherX1 - (slopex_colther * tactileX1))
    slopey_colther = (colthery1 - colthery2) / (
        tactiley1 - tactiley2
    )  # (coltherY1 - coltherY2)/(tactileY1 - tactileY2)
    yoriginy_colther = colthery1 - (
        slopey_colther * tactiley1
    )  # (coltherY1 - (slopey_colther * tactileY1))

except Exception as e:
    print(e)

# slopex_camera = (300000 - 520000)/(40000 - 260000) #()
# yoriginx_camera = 300000 - (slopex_camera * 40000)
# slopey_camera = (300000 - 480000)/(290000 - 390000)
# yoriginy_camera = 390000 - (slopey_camera * 290000)
# 222245


z_ds = {"colther": 40000, "camera": 0}

diff_colther_touch = 12000

lut_distances = [3.5, 4, 4.5, 5, 5.5, 6]

########################################################
temp = -1
indx0, indy0 = 1, 1

centreROI = 1, 2
light = 3

frames = []

dry_ice_pos = {"x": 0, "y": 290000, "z": 0}

# For dict of zabers
axes = {
    "colther": ["x", "y", "z"],
    "camera": ["y", "x", "z"],
    "tactile": ["x", "y", "z"],
}

# Order of movement
haxes = {
    "colther": ["z", "x", "y"],
    "camera": ["x", "z", "y"],
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

rules = {
    "colther": {"x": True, "y": True, "z": True},
    "camera": {"x": False, "y": True, "z": True},
    "tactile": {"x": False, "y": True, "z": True},
}

temp = 32
pid_out = 0
current = 0

dummy = True

pos_init = {"x": 30000, "y": 750000, "z": 0}
pos_knuckle = {"x": 300000, "y": 180000, "z": 0}
pos_centre = {"x": 250000, "y": 240472, "z": 0}

lamp = 0

# colther default speed
default_speed = 153600
speed = 153600 * 4

modem_port_touch = 41
modem_port_pantilt = 2
modem_port_dimmer = 33
modem_port_syringe = 1

# modem_port_colther
modem_port_camera = 31
modem_port_tactile = 3

usb_port_camera = 1
usb_port_tactile = 9
usb_port_touch = 1
usb_port_pantilt = 1
usb_port_dimmer = 1
usb_port_syringe = 1

zaber_models = {
    "colther": {"x": "end_X-LSQ150B", "y": "end_A-LSQ150B", "z": "end_A-LSQ150B"},
    "camera": {"x": "end_LSM100B-T4", "y": "end_LSM200B-T4", "z": "end_LSM100B-T4"},
    "tactile": {"x": "end_LSM100B-T4", "y": "end_LSM200B-T4", "z": "end_LSM100B-T4"},
}
zaber_models_end = {
    "end_X-LSQ150B": 305381,
    "end_A-LSQ150B": 305381,
    "end_LSM100B-T4": 533333,
    "end_LSM200B-T4": 1066667,
}

length = 7

size_ROI = 15

question_scaling = "\n How much ...? (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)   "
question_staircase = (
    "Was there any temperature change during the tone? 0: NO, 1: YES    "
)

time_out_ex = 2
time_out_tb = 5

initial_staircase_temp = 1.1

delay_data_display = 1

park_touch = {"x": 533332, "z": 330000}
