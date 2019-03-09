# #################################### Computer vision parameters #####################################################

# The parameters are used by functions in vision2.py and can be changed from the GUI client_gui.py

# default values for the parameters

# black-filter
rgb_L = 50  # threshold for r, g and b values. rgb-pixels with r,g,b< rgb_L are consider to be no facelet-pixel

# white-filter
sat_W = 60  # hsv-pixels with a saturation s > sat_W are considered not to be a white facelet-pixel
val_W = 150  # hsv-pixels with a value v < sat_W are considered not to be a white facelet-pixel

# this parameter cannot be changed by the GUI
sigma_W = 300  # a grid square is considered part of a white facelet if the standard deviation of the hue is <= sigma_W

# color-filter
sigma_C = 5  # a grid square is considered part of a facelet if the standard deviation of the hue is <= sigma_C
delta_C = 5  # pixels within the interval [hue-delta,hue+delta] are considered to belong to the same facelet

# these parameters depend on the actually used cube colors and the lightning conditions
orange_L = 6  # lowest allowed hue for color orange
orange_H = 23  # highest allowed hue for color orange
yellow_H = 50  # highest allowed hue for color yellow
green_H = 100  # highest allowed hue for color green
blue_H = 160  # highest allowed hue for color blue
# hue values > blue_H and < orange_L describe the color red

# the colors of the cube are stored here
face_col = []  # the colors (as text) of a cube face are stored here
face_hsv = []  # the colors (as hsv-values) of a cube face are stored here
cube_col = {}  # the colors (as text) of the 6 faces
cube_hsv = {}  # the colors (as hsv-values) o the 6 faces
