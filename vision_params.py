# ############################ Computer vision parameters #####################################################

rgb_L = 50  #

sigma_W = 300  # This parameter cannot be changed in the GUI

# default values for parameters
sat_W = 60  # maximum allowed saturation for white
val_W = 150  # minimum allowed value for white

sigma_C = 5  # maximum allowed hue standard deviation for a grid square to be considered as part of a facelet
delta_C = 5  # pixels within the interval [hue-delta,hue+delta] are considered to belong to the same facelet

orange_L = 6  # lowest allowed hue for color orange
orange_H = 23  # highest allowed hue for color orange
yellow_H = 50  # highest allowed hue for color yellow
green_H = 100  # highest allowed hue for color green
blue_H = 160  # highest allowed hue for color blue
# hue values > blue_H and < orange_L describe the color red


fc = [['red', 'red', 'red'], ['red', 'red', 'red'], ['red', 'red', 'red']]

