stimulus = 0
current_device = "camera"

positions1 = {
    "colther": [None, None, None],
    "tactile": [None, None, None],
    "non_tactile": [None, None, None],
    "camera": [None, None, None],
}


positions2 = {
    "colther": {"experimental": [None, None, None], "control": [None, None, None]},
    "tactile": {"experimental": [None, None, None], "control": [None, None, None]},
    "non_tactile": {"experimental": [None, None, None], "control": [None, None, None]},
    "camera": {"experimental": [None, None, None], "control": [None, None, None]},
}

conditions = None

temp = 33
amount = 10000

thres_temp = None
stimulus = 0

indx0, indy0 = None, None
rt = None

centreROI = None, None
