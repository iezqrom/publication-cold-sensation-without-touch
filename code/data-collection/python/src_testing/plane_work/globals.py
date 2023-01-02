dev = "Dev1"
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

vminT = 30
vmaxT = 40

fig = None

# frames = {'fixation_cross': [], 'age': [], 'instructions': [], 'break_point': [],
#             'break_point_ready': [], 'transition': [], 'end': [], 'start': [], 'n_participant': [],
#             'microspots': [], 'zabering': [], 'tactile_height': [],
#             'intro_big_three':[], 'response': []}

frames = {"fixation_cross": [], "response": []}

positions = {
    "colther": {"experimental": [None, None, None], "control": [None, None, None]},
    "tactile": {"experimental": [None, None, None], "control": [None, None, None]},
    "camera": {"experimental": [None, None, None], "control": [None, None, None]},
}

# Data
array_RFS = []
RF = None

response = None
