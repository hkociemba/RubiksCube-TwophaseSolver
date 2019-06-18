# ################### Movetables describe the transformation of the coordinates by cube moves. #########################

from os import path
import array as ar
import cubie as cb
import enums
from defs import N_TWIST, N_FLIP, N_SLICE_SORTED, N_CORNERS, N_UD_EDGES, N_MOVE

a = cb.CubieCube()
# ######################################### Move table for the twists of the corners. ##################################

# The twist coordinate describes the 3^7 = 2187 possible orientations of the 8 corners
# 0 <= twist < 2187 in phase 1, twist = 0 in phase 2
fname = "move_twist"
if not path.isfile(fname):
    print("creating " + fname + " table...")
    twist_move = ar.array('H', [0 for i in range(N_TWIST * N_MOVE)])
    for i in range(N_TWIST):
        a.set_twist(i)
        for j in enums.Color:  # six faces U, R, F, D, L, B
            for k in range(3):  # three moves for each face, for example U, U2, U3 = U'
                a.corner_multiply(cb.basicMoveCube[j])
                twist_move[N_MOVE * i + 3 * j + k] = a.get_twist()
            a.corner_multiply(cb.basicMoveCube[j])  # 4. move restores face
    fh = open(fname, "wb")
    twist_move.tofile(fh)
else:
    print("loading " + fname + " table...")
    fh = open(fname, "rb")
    twist_move = ar.array('H')
    twist_move.fromfile(fh, N_TWIST * N_MOVE)
fh.close()
########################################################################################################################

# ####################################  Move table for the flip of the edges. ##########################################

# The flip coordinate describes the 2^11 = 2048 possible orientations of the 12 edges
# 0 <= flip < 2048 in phase 1, flip = 0 in phase 2
fname = "move_flip"
if not path.isfile(fname):
    print("creating " + fname + " table...")
    flip_move = ar.array('H', [0 for i in range(N_FLIP * N_MOVE)])
    for i in range(N_FLIP):
        a.set_flip(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                flip_move[N_MOVE * i + 3 * j + k] = a.get_flip()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(fname, "wb")
    flip_move.tofile(fh)
else:
    print("loading " + fname + " table...")
    fh = open(fname, "rb")
    flip_move = ar.array('H')
    flip_move.fromfile(fh, N_FLIP * N_MOVE)
fh.close()
########################################################################################################################

# ###################### Move table for the four UD-slice edges FR, FL, Bl and BR. #####################################

# The slice_sorted coordinate describes the 12!/8! = 11880 possible positions of the FR, FL, BL and BR edges.
# Though for phase 1 only the "unsorted" slice coordinate with Binomial(12,4) = 495 positions is relevant, using the
# slice_sorted coordinate gives us the permutation of the FR, FL, BL and BR edges at the beginning of phase 2 for free.
# 0 <= slice_sorted < 11880 in phase 1, 0 <= slice_sorted < 24 in phase 2, slice_sorted = 0 for solved cube
fname = "move_slice_sorted"
if not path.isfile(fname):
    print("creating " + fname + " table...")
    slice_sorted_move = ar.array('H', [0 for i in range(N_SLICE_SORTED * N_MOVE)])
    for i in range(N_SLICE_SORTED):
        if i % 200 == 0:
            print('.', end='', flush=True)
        a.set_slice_sorted(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                slice_sorted_move[N_MOVE * i + 3 * j + k] = a.get_slice_sorted()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(fname, "wb")
    slice_sorted_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(fname, "rb")
    slice_sorted_move = ar.array('H')
    slice_sorted_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()
########################################################################################################################

# ################# Move table for the u_edges coordinate for transition phase 1 -> phase 2 ############################

# The u_edges coordinate describes the 12!/8! = 11880 possible positions of the UR, UF, UL and UB edges. It is needed at
# the end of phase 1 to set up the coordinates of phase 2
# 0 <= u_edges < 11880 in phase 1, 0 <= u_edges < 1680 in phase 2, u_edges = 1656 for solved cube."""
fname = "move_u_edges"
if not path.isfile(fname):
    print("creating " + fname + " table...")
    u_edges_move = ar.array('H', [0 for i in range(N_SLICE_SORTED * N_MOVE)])
    for i in range(N_SLICE_SORTED):
        if i % 200 == 0:
            print('.', end='', flush=True)
        a.set_u_edges(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                u_edges_move[N_MOVE * i + 3 * j + k] = a.get_u_edges()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(fname, "wb")
    u_edges_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(fname, "rb")
    u_edges_move = ar.array('H')
    u_edges_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()
########################################################################################################################

# ################# Move table for the d_edges coordinate for transition phase 1 -> phase 2 ############################

# The d_edges coordinate describes the 12!/8! = 11880 possible positions of the DR, DF, DL and DB edges. It is needed at
# the end of phase 1 to set up the coordinates of phase 2
#  0 <= d_edges < 11880 in phase 1, 0 <= d_edges < 1680 in phase 2, d_edges = 0 for solved cube.
fname = "move_d_edges"
if not path.isfile(fname):
    print("creating " + fname + " table...")
    d_edges_move = ar.array('H', [0 for i in range(N_SLICE_SORTED * N_MOVE)])
    for i in range(N_SLICE_SORTED):
        if i % 200 == 0:
            print('.', end='', flush=True)
        a.set_d_edges(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                d_edges_move[N_MOVE * i + 3 * j + k] = a.get_d_edges()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(fname, "wb")
    d_edges_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(fname, "rb")
    d_edges_move = ar.array('H')
    d_edges_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()
########################################################################################################################

# ######################### # Move table for the edges in the U-face and D-face. #######################################

# The ud_edges coordinate describes the 40320 permutations of the edges UR, UF, UL, UB, DR, DF, DL and DB in phase 2
# ud_edges undefined in phase 1, 0 <= ud_edges < 40320 in phase 2, ud_edges = 0 for solved cube.
fname = "move_ud_edges"
if not path.isfile(fname):
    print("creating " + fname + " table...")
    ud_edges_move = ar.array('H', [0 for i in range(N_UD_EDGES * N_MOVE)])
    for i in range(N_UD_EDGES):
        if (i+1) % 600 == 0:
            print('.', end='', flush=True)
        if (i+1) % 48000 == 0:
            print('')
        a.set_ud_edges(i)
        for j in enums.Color:
            for k in range(3):
                a.edge_multiply(cb.basicMoveCube[j])
                # only R2, F2, L2 and B2 in phase 2
                if j in [enums.Color.R, enums.Color.F, enums.Color.L, enums.Color.B] and k != 1:
                    continue
                ud_edges_move[N_MOVE * i + 3 * j + k] = a.get_ud_edges()
            a.edge_multiply(cb.basicMoveCube[j])
    fh = open(fname, "wb")
    ud_edges_move.tofile(fh)
    print()
else:
    print("loading " + fname + " table...")
    fh = open(fname, "rb")
    ud_edges_move = ar.array('H')
    ud_edges_move.fromfile(fh, N_UD_EDGES * N_MOVE)
fh.close()
########################################################################################################################

# ############################ Move table for the corners coordinate in phase 2 ########################################

# The corners coordinate describes the 8! = 40320 permutations of the corners.
# 0 <= corners < 40320 defined but unused in phase 1, 0 <= corners < 40320 in phase 2, corners = 0 for solved cube
fname = "move_corners"
if not path.isfile(fname):
    print("creating " + fname + " table...")
    corners_move = ar.array('H', [0 for i in range(N_CORNERS * N_MOVE)])
    for i in range(N_CORNERS):
        if (i+1) % 200 == 0:
            print('.', end='', flush=True)
        if(i+1) % 16000 == 0:
            print('')
        a.set_corners(i)
        for j in enums.Color:
            for k in range(3):
                a.corner_multiply(cb.basicMoveCube[j])
                corners_move[N_MOVE * i + 3 * j + k] = a.get_corners()
            a.corner_multiply(cb.basicMoveCube[j])
    fh = open(fname, "wb")
    corners_move.tofile(fh)
    fh.close()
    print()
else:
    print("loading " + fname + " table...")
    fh = open(fname, "rb")
    corners_move = ar.array('H')
    corners_move.fromfile(fh, N_CORNERS * N_MOVE)
fh.close()
########################################################################################################################
