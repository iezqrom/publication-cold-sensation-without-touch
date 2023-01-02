dev = "Dev2"
rate_NI = 100

cam = None
ani_boolean = False
hidden = True
current_device = "camera"

shutter = "close"

answer = None
amount = 10000

subj_age = None
n_subj = None

# Thermal camera
vminT = 30
vmaxT = 40
fig = None
temp = 30

baseline_temp = 33

indy0 = None
indx0 = None
pos_zaber = 0

centreROI = {"control": [], "experimental": []}

frames = {
    "fixation_cross": [],
    "age": [],
    "instructions": [],
    "break_point": [],
    "break_point_ready": [],
    "response": [],
    "transition": [],
    "end": [],
    "start": [],
    "n_participant": [],
    "microspots": [],
    "zabering": [],
    "tactile_height": [],
    "intro_big_three": [],
    "intro_training": [],
    "repeat_training": [],
    "intro_trials": [],
    "intro_tactile_height": [],
    "baseline_temp": [],
}

positions = {
    "colther": {"experimental": [None, None, None], "control": [None, None, None]},
    "tactile": {"experimental": [None, None, None], "control": [None, None, None]},
    "non_tactile": {"experimental": [None, None, None], "control": [None, None, None]},
    "camera": {"experimental": [None, None, None], "control": [None, None, None]},
}

conditions = [
    ("non_tactile", "experimental"),
    ("non_tactile", "control"),
    ("tactile", "experimental"),
    ("tactile", "control"),
]

boost = [
    ("non_tactile", "experimental", "boost"),
    ("non_tactile", "control", "boost"),
    ("tactile", "experimental", "boost"),
    ("tactile", "control", "boost"),
]


current_device = "camera"

# Data
RF = None
response = None
pressure = None

training_boolean = "n"
