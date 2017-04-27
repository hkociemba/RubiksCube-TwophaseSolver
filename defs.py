# ###################################### some definitions and constants ################################################

from enums import Facelet as Fc, Color as Cl

# Map the corner positions to facelet positions.
cornerFacelet = [[Fc.U9, Fc.R1, Fc.F3], [Fc.U7, Fc.F1, Fc.L3], [Fc.U1, Fc.L1, Fc.B3], [Fc.U3, Fc.B1, Fc.R3],
                 [Fc.D3, Fc.F9, Fc.R7], [Fc.D1, Fc.L9, Fc.F7], [Fc.D7, Fc.B9, Fc.L7], [Fc.D9, Fc.R9, Fc.B7]
                 ]

# Map the edge positions to facelet positions.
edgeFacelet = [[Fc.U6, Fc.R2], [Fc.U8, Fc.F2], [Fc.U4, Fc.L2], [Fc.U2, Fc.B2], [Fc.D6, Fc.R8], [Fc.D2, Fc.F8],
               [Fc.D4, Fc.L8], [Fc.D8, Fc.B8], [Fc.F6, Fc.R4], [Fc.F4, Fc.L6], [Fc.B6, Fc.L4], [Fc.B4, Fc.R6]
               ]

# Map the corner positions to facelet colors.
cornerColor = [[Cl.U, Cl.R, Cl.F], [Cl.U, Cl.F, Cl.L], [Cl.U, Cl.L, Cl.B], [Cl.U, Cl.B, Cl.R],
               [Cl.D, Cl.F, Cl.R], [Cl.D, Cl.L, Cl.F], [Cl.D, Cl.B, Cl.L], [Cl.D, Cl.R, Cl.B]
               ]

# Map the edge positions to facelet colors.
edgeColor = [[Cl.U, Cl.R], [Cl.U, Cl.F], [Cl.U, Cl.L], [Cl.U, Cl.B], [Cl.D, Cl.R], [Cl.D, Cl.F],
             [Cl.D, Cl.L], [Cl.D, Cl.B], [Cl.F, Cl.R], [Cl.F, Cl.L], [Cl.B, Cl.L], [Cl.B, Cl.R]
             ]

# ###################################### some "constants" ##############################################################
N_PERM_4 = 24
N_CHOOSE_8_4 = 70
N_MOVE = 18  # number of possible face moves

N_TWIST = 2187  # 3^7 possible corner orientations in phase 1
N_FLIP = 2048  # 2^11 possible edge orientations in phase 1
N_SLICE_SORTED = 11880  # 12*11*10*9 possible positions of the FR, FL, BL, BR edges in phase 1
N_SLICE = N_SLICE_SORTED // N_PERM_4  # we ignore the permutation of FR, FL, BL, BR in phase 1
N_FLIPSLICE_CLASS = 64430  # number of equivalence classes for combined flip+slice concerning symmetry group D4h

N_U_EDGES_PHASE2 = 1680  # number of different positions of the edges UR, UF, UL and UB in phase 2
# N_D_EDGES_PHASE2 = 1680  # number of different positions of the edges DR, DF, DL and DB in phase 2
N_CORNERS = 40320  # 8! corner permutations in phase 2
N_CORNERS_CLASS = 2768  # number of equivalence classes concerning symmetry group D4h
N_UD_EDGES = 40320  # 8! permutations of the edges in the U-face and D-face in phase 2

N_SYM = 48  # number of cube symmetries of full group Oh
N_SYM_D4h = 16  # Number of symmetries of subgroup D4h
########################################################################################################################
