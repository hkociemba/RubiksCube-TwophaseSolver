# ##### The cube on the coordinate level. It is described by a 3-tuple of natural numbers in phase 1 and phase 2. ######

from os import path
import array as ar

import cubie as cb
import enums
import moves as mv
import pruning as pr
import symmetries as sy
from defs import N_U_EDGES_PHASE2, N_PERM_4, N_CHOOSE_8_4, N_FLIP, N_TWIST, N_UD_EDGES, N_MOVE
from enums import Edge as Ed

SOLVED = 0  # 0 is index of solved state (except for u_edges coordinate)
u_edges_plus_d_edges_to_ud_edges = None  # global variable


class CoordCube:
    """Represent a cube on the coordinate level.
    
    In phase 1 a state is uniquely determined by the three coordinates flip, twist and slice.
    In phase 2 a state is uniquely determined by the three coordinates corners, ud_edges and slice_sorted.
    """

    def __init__(self, cc=None):
        if cc is None:
            self.twist = SOLVED  # twist of corners
            self.flip = SOLVED  # flip of edges
            self.slice_sorted = SOLVED  # Position of FR, FL, BL, BR edges. Valid in phase 1 (<11880) and phase 2 (<24)
            # The phase 1 slice coordinate is given by slice_sorted // 24

            self.u_edges = 1656  # Valid in phase 1 (<11880) and phase 2 (<1680). 1656 is the index of solved u_edges.
            self.d_edges = SOLVED  # Valid in phase 1 (<11880) and phase 2 (<1680)
            self.corners = SOLVED  # corner permutation. Valid in phase1 and phase2
            self.ud_edges = SOLVED  # permutation of the ud-edges. Valid only in phase 2
        else:
            self.twist = cc.get_twist()
            self.flip = cc.get_flip()
            self.slice_sorted = cc.get_slice_sorted()
            self.u_edges = cc.get_u_edges()
            self.d_edges = cc.get_d_edges()
            self.corners = cc.get_corners()
            if self.slice_sorted < N_PERM_4:  # phase 2 cube
                self.ud_edges = cc.get_ud_edges()
            else:
                self.ud_edges = -1  # invalid

            # symmetry reduced flipslice coordinate used in phase 1
            self.flipslice_classidx = sy.flipslice_classidx[N_FLIP * (self.slice_sorted // N_PERM_4) + self.flip]
            self.flipslice_sym = sy.flipslice_sym[N_FLIP * (self.slice_sorted // N_PERM_4) + self.flip]
            self.flipslice_rep = sy.flipslice_rep[self.flipslice_classidx]
            # symmetry reduced corner permutation coordinate used in phase 2
            self.corner_classidx = sy.corner_classidx[self.corners]
            self.corner_sym = sy.corner_sym[self.corners]
            self.corner_rep = sy.corner_rep[self.corner_classidx]

    def __str__(self):
        s = '(twist: ' + str(self.twist) + ', flip: ' + str(self.flip) + ', slice: ' + str(self.slice_sorted // 24) + \
            ', U-edges: ' + str(self.u_edges) + ', D-edges: ' + str(self.d_edges) + ', E-edges: ' \
            + str(self.slice_sorted) + ', Corners: ' + str(self.corners) + ', UD-Edges : ' + str(self.ud_edges) + ')'
        s = s + '\n' + str(self.flipslice_classidx) + ' ' + str(self.flipslice_sym) + ' ' + str(self.flipslice_rep)
        s = s + '\n' + str(self.corner_classidx) + ' ' + str(self.corner_sym) + ' ' + str(self.corner_rep)
        return s

    def phase1_move(self, m):
        self.twist = mv.twist_move[N_MOVE * self.twist + m]
        self.flip = mv.flip_move[N_MOVE * self.flip + m]
        self.slice_sorted = mv.slice_sorted_move[N_MOVE * self.slice_sorted + m]
        # optional:
        self.u_edges = mv.u_edges_move[N_MOVE * self.u_edges + m]  # u_edges and d_edges retrieve ud_edges easily
        self.d_edges = mv.d_edges_move[N_MOVE * self.d_edges + m]  # if phase 1 is finished and phase 2 starts
        self.corners = mv.corners_move[N_MOVE * self.corners + m]  # Is needed only in phase 2

        self.flipslice_classidx = sy.flipslice_classidx[N_FLIP * (self.slice_sorted // N_PERM_4) + self.flip]
        self.flipslice_sym = sy.flipslice_sym[N_FLIP * (self.slice_sorted // N_PERM_4) + self.flip]
        self.flipslice_rep = sy.flipslice_rep[self.flipslice_classidx]

        self.corner_classidx = self.corner_classidx = sy.corner_classidx[self.corners]
        self.corner_sym = sy.corner_sym[self.corners]
        self.corner_rep = sy.corner_rep[self.corner_classidx]

    def phase2_move(self, m):
        self.slice_sorted = mv.slice_sorted_move[N_MOVE * self.slice_sorted + m]
        self.corners = mv.corners_move[N_MOVE * self.corners + m]
        self.ud_edges = mv.ud_edges_move[N_MOVE * self.ud_edges + m]

    def get_depth_phase1(self):
        slice_ = self.slice_sorted // N_PERM_4
        flip = self.flip
        twist = self.twist
        flipslice = N_FLIP * slice_ + flip
        classidx = sy.flipslice_classidx[flipslice]
        sym = sy.flipslice_sym[flipslice]
        depth_mod3 = pr.get_flipslice_twist_depth3(N_TWIST * classidx + sy.twist_conj[(twist << 4) + sym])

        depth = 0
        while flip != SOLVED or slice_ != SOLVED or twist != SOLVED:
            if depth_mod3 == 0:
                depth_mod3 = 3
            for m in enums.Move:
                twist1 = mv.twist_move[N_MOVE * twist + m]
                flip1 = mv.flip_move[N_MOVE * flip + m]
                slice1 = mv.slice_sorted_move[N_MOVE * slice_ * N_PERM_4 + m] // N_PERM_4
                flipslice1 = N_FLIP * slice1 + flip1
                classidx1 = sy.flipslice_classidx[flipslice1]
                sym = sy.flipslice_sym[flipslice1]
                if pr.get_flipslice_twist_depth3(
                        N_TWIST * classidx1 + sy.twist_conj[(twist1 << 4) + sym]) == depth_mod3 - 1:
                    depth += 1
                    twist = twist1
                    flip = flip1
                    slice_ = slice1
                    depth_mod3 -= 1
                    break
        return depth

    @staticmethod
    def get_depth_phase2(corners, ud_edges):
        # the slice coordinate is not included
        classidx = sy.corner_classidx[corners]
        sym = sy.corner_sym[corners]
        depth_mod3 = pr.get_corners_ud_edges_depth3(N_UD_EDGES * classidx + sy.ud_edges_conj[(ud_edges << 4) + sym])
        if depth_mod3 == 3:  # unfilled entry, depth >= 11
            return 11
        depth = 0
        while corners != SOLVED or ud_edges != SOLVED:
            if depth_mod3 == 0:
                depth_mod3 = 3
            # only iterate phase 2 moves
            for m in (enums.Move.U1, enums.Move.U2, enums.Move.U3, enums.Move.R2, enums.Move.F2, enums.Move.D1,
                      enums.Move.D2, enums.Move.D3, enums.Move.L2, enums.Move.B2):
                corners1 = mv.corners_move[N_MOVE * corners + m]
                ud_edges1 = mv.ud_edges_move[N_MOVE * ud_edges + m]
                classidx1 = sy.corner_classidx[corners1]
                sym = sy.corner_sym[corners1]
                if pr.get_corners_ud_edges_depth3(N_UD_EDGES * classidx1 + sy.ud_edges_conj[(ud_edges1 << 4) + sym]) == \
                        depth_mod3 - 1:
                    depth += 1
                    corners = corners1
                    ud_edges = ud_edges1
                    depth_mod3 -= 1
                    break
        return depth


def create_phase2_edgemerge_table():
    """phase2_edgemerge retrieves the initial phase 2 ud_edges coordinate from the u_edges and d_edges coordinates."""
    fname = "phase2_edgemerge"
    global u_edges_plus_d_edges_to_ud_edges
    c_u = cb.CubieCube()
    c_d = cb.CubieCube()
    c_ud = cb.CubieCube()
    edge_u = [Ed.UR, Ed.UF, Ed.UL, Ed.UB]
    edge_d = [Ed.DR, Ed.DF, Ed.DL, Ed.DB]
    edge_ud = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]

    if not path.isfile(fname):
        cnt = 0
        print("creating " + fname + " table...")
        u_edges_plus_d_edges_to_ud_edges = ar.array('H', [0 for i in range(N_U_EDGES_PHASE2 * N_PERM_4)])
        for i in range(N_U_EDGES_PHASE2):
            c_u.set_u_edges(i)
            for j in range(N_CHOOSE_8_4):
                c_d.set_d_edges(j * N_PERM_4)
                invalid = False
                for e in edge_ud:
                    c_ud.ep[e] = -1  # invalidate edges
                    if c_u.ep[e] in edge_u:
                        c_ud.ep[e] = c_u.ep[e]
                    if c_d.ep[e] in edge_d:
                        c_ud.ep[e] = c_d.ep[e]
                    if c_ud.ep[e] == -1:
                        invalid = True  # edge collision
                        break
                if not invalid:
                    for k in range(N_PERM_4):
                        c_d.set_d_edges(j * N_PERM_4 + k)
                        for e in edge_ud:
                            if c_u.ep[e] in edge_u:
                                c_ud.ep[e] = c_u.ep[e]
                            if c_d.ep[e] in edge_d:
                                c_ud.ep[e] = c_d.ep[e]
                        u_edges_plus_d_edges_to_ud_edges[N_PERM_4 * i + k] = c_ud.get_ud_edges()
                        cnt += 1
                        if cnt % 2000 == 0:
                            print('.', end='', flush=True)
        print()
        fh = open(fname, "wb")
        u_edges_plus_d_edges_to_ud_edges.tofile(fh)
        fh.close()
        print()
    else:
        fh = open(fname, "rb")
        u_edges_plus_d_edges_to_ud_edges = ar.array('H')
        u_edges_plus_d_edges_to_ud_edges.fromfile(fh, N_U_EDGES_PHASE2 * N_PERM_4)


########################################################################################################################


create_phase2_edgemerge_table()
