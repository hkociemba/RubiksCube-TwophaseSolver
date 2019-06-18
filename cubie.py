# ####### The cube on the cubie level is described by the permutation and orientations of corners and edges ############

from defs import cornerFacelet, edgeFacelet, cornerColor, edgeColor, N_SYM
from enums import Color, Corner as Co, Edge as Ed
import face
from misc import c_nk, rotate_left, rotate_right
from random import randrange


# ################## The basic six cube moves described by permutations and changes in orientation #####################

# Up-move
cpU = [Co.UBR, Co.URF, Co.UFL, Co.ULB, Co.DFR, Co.DLF, Co.DBL, Co.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Ed.UB, Ed.UR, Ed.UF, Ed.UL, Ed.DR, Ed.DF, Ed.DL, Ed.DB, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Right-move
cpR = [Co.DFR, Co.UFL, Co.ULB, Co.URF, Co.DRB, Co.DLF, Co.DBL, Co.UBR]  # permutation of the corners
coR = [2, 0, 0, 1, 1, 0, 0, 2]  # changes of the orientations of the corners
epR = [Ed.FR, Ed.UF, Ed.UL, Ed.UB, Ed.BR, Ed.DF, Ed.DL, Ed.DB, Ed.DR, Ed.FL, Ed.BL, Ed.UR]  # permutation of the edges
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # changes of the permutations of the edges

# Front-move
cpF = [Co.UFL, Co.DLF, Co.ULB, Co.UBR, Co.URF, Co.DFR, Co.DBL, Co.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Ed.UR, Ed.FL, Ed.UL, Ed.UB, Ed.DR, Ed.FR, Ed.DL, Ed.DB, Ed.UF, Ed.DF, Ed.BL, Ed.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# Down-move
cpD = [Co.URF, Co.UFL, Co.ULB, Co.UBR, Co.DLF, Co.DBL, Co.DRB, Co.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DF, Ed.DL, Ed.DB, Ed.DR, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Left-move
cpL = [Co.URF, Co.ULB, Co.DBL, Co.UBR, Co.DFR, Co.UFL, Co.DLF, Co.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Ed.UR, Ed.UF, Ed.BL, Ed.UB, Ed.DR, Ed.DF, Ed.FL, Ed.DB, Ed.FR, Ed.UL, Ed.DL, Ed.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Back-move
cpB = [Co.URF, Co.UFL, Co.UBR, Co.DRB, Co.DFR, Co.DLF, Co.ULB, Co.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Ed.UR, Ed.UF, Ed.UL, Ed.BR, Ed.DR, Ed.DF, Ed.DL, Ed.BL, Ed.FR, Ed.FL, Ed.UB, Ed.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
########################################################################################################################

CUBE_OK = True


class CubieCube:
    """Represent a cube on the cubie level with 8 corner cubies, 12 edge cubies and the cubie orientations.
    
    Is also used to represent:
    1. the 18 cube moves
    2. the 48 symmetries of the cube.
    """
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        """
        Initializes corners and edges.
        :param cp: corner permutation
        :param co: corner orientation
        :param ep: edge permutation
        :param eo: edge orientation
        """
        if cp is None:
            self.cp = [Co(i) for i in range(8)]  # You may not put this as the default two lines above!
        else:
            self.cp = cp[:]
        if co is None:
            self.co = [0]*8
        else:
            self.co = co[:]
        if ep is None:
            self.ep = [Ed(i) for i in range(12)]
        else:
            self.ep = ep[:]
        if eo is None:
            self.eo = [0] * 12
        else:
            self.eo = eo[:]

    def __str__(self):
        """Print string for a cubie cube."""
        s = ''
        for i in Co:
            s = s + '(' + str(self.cp[i]) + ',' + str(self.co[i]) + ')'
        s += '\n'
        for i in Ed:
            s = s + '(' + str(self.ep[i]) + ',' + str(self.eo[i]) + ')'
        return s

    def __eq__(self, other):
        """Define equality of two cubie cubes."""
        if self.cp == other.cp and self.co == other.co and self.ep == other.ep and self.eo == other.eo:
            return True
        else:
            return False

    def to_facelet_cube(self):
        """Return a facelet representation of the cube."""
        fc = face.FaceCube()
        for i in Co:
            j = self.cp[i]  # corner j is at corner position i
            ori = self.co[i]  # orientation of C j at position i
            for k in range(3):
                fc.f[cornerFacelet[i][(k+ori) % 3]] = cornerColor[j][k]
        for i in Ed:
            j = self.ep[i]  # similar for Es
            ori = self.eo[i]
            for k in range(2):
                fc.f[edgeFacelet[i][(k+ori) % 2]] = edgeColor[j][k]
        return fc

    def corner_multiply(self, b):
        """Multiply this cubie cube with another cubie cube b, restricted to the corners. Does not change b."""
        c_perm = [0]*8
        c_ori = [0]*8
        ori = 0
        for c in Co:
            c_perm[c] = self.cp[b.cp[c]]
            ori_a = self.co[b.cp[c]]
            ori_b = b.co[c]
            if ori_a < 3 and ori_b < 3:  # two regular cubes
                ori = ori_a + ori_b
                if ori >= 3:
                    ori -= 3
            elif ori_a < 3 <= ori_b:  # cube b is in a mirrored state
                ori = ori_a + ori_b
                if ori >= 6:
                    ori -= 3  # the composition also is in a mirrored state
            elif ori_a >= 3 > ori_b:  # cube a is in a mirrored state
                ori = ori_a - ori_b
                if ori < 3:
                    ori += 3  # the composition is a mirrored cube
            elif ori_a >= 3 and ori_b >= 3:  # if both cubes are in mirrored states
                ori = ori_a - ori_b
                if ori < 0:
                    ori += 3  # the composition is a regular cube
            c_ori[c] = ori
        for c in Co:
            self.cp[c] = c_perm[c]
            self.co[c] = c_ori[c]

    def edge_multiply(self, b):
        """ Multiply this cubie cube with another cubiecube b, restricted to the edges. Does not change b."""
        e_perm = [0]*12
        e_ori = [0]*12
        for e in Ed:
            e_perm[e] = self.ep[b.ep[e]]
            e_ori[e] = (b.eo[e] + self.eo[b.ep[e]]) % 2
        for e in Ed:
            self.ep[e] = e_perm[e]
            self.eo[e] = e_ori[e]

    def multiply(self, b):
        self.corner_multiply(b)
        self.edge_multiply(b)

    def inv_cubie_cube(self, d):
        """Store the inverse of this cubie cube in d."""
        for e in Ed:
            d.ep[self.ep[e]] = e
        for e in Ed:
            d.eo[e] = self.eo[d.ep[e]]

        for c in Co:
            d.cp[self.cp[c]] = c
        for c in Co:
            ori = self.co[d.cp[c]]
            if ori >= 3:
                d.co[c] = ori
            else:
                d.co[c] = -ori
                if d.co[c] < 0:
                    d.co[c] += 3

    def corner_parity(self):
        """Give the parity of the corner permutation."""
        s = 0
        for i in range(Co.DRB, Co.URF, -1):
            for j in range(i - 1, Co.URF - 1, -1):
                if self.cp[j] > self.cp[i]:
                    s += 1
        return s % 2

    def edge_parity(self):
        """Give the parity of the edge permutation. A solvable cube has the same corner and edge parity."""
        s = 0
        for i in range(Ed.BR, Ed.UR, -1):
            for j in range(i - 1, Ed.UR - 1, -1):
                if self.ep[j] > self.ep[i]:
                    s += 1
        return s % 2

    def symmetries(self):
        """Generate a list of the symmetries and antisymmetries of the cubie cube."""
        from symmetries import symCube, inv_idx  # not nice here but else we have circular imports
        s = []
        d = CubieCube()
        for j in range(N_SYM):
            c = CubieCube(symCube[j].cp, symCube[j].co, symCube[j].ep, symCube[j].eo)
            c.multiply(self)
            c.multiply(symCube[inv_idx[j]])
            if self == c:
                s.append(j)
            c.inv_cubie_cube(d)
            if self == d:  # then we have antisymmetry
                s.append(j + N_SYM)
        return s

# ###################################### coordinates for phase 1 and 2 #################################################
    def get_twist(self):
        """Get the twist of the 8 corners. 0 <= twist < 2187 in phase 1, twist = 0 in phase 2."""
        ret = 0
        for i in range(Co.URF, Co.DRB):
            ret = 3 * ret + self.co[i]
        return ret

    def set_twist(self, twist):
        twistparity = 0
        for i in range(Co.DRB - 1, Co.URF - 1, -1):
            self.co[i] = twist % 3
            twistparity += self.co[i]
            twist //= 3
        self.co[Co.DRB] = ((3 - twistparity % 3) % 3)

    def get_flip(self):
        """Get the flip of the 12 edges. 0 <= flip < 2048 in phase 1, flip = 0 in phase 2."""
        ret = 0
        for i in range(Ed.UR, Ed.BR):
            ret = 2 * ret + self.eo[i]
        return ret

    def set_flip(self, flip):
        flipparity = 0
        for i in range(Ed.BR - 1, Ed.UR - 1, -1):
            self.eo[i] = flip % 2
            flipparity += self.eo[i]
            flip //= 2
        self.eo[Ed.BR] = ((2 - flipparity % 2) % 2)

    def get_slice(self):
        """Get the location of the UD-slice edges FR,FL,BL and BR ignoring their permutation.
            0<= slice < 495 in phase 1, slice = 0 in phase 2."""
        a = x = 0
        # Compute the index a < (12 choose 4)
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.FR <= self.ep[j] <= Ed.BR:
                a += c_nk(11 - j, x + 1)
                x += 1
        return a

    def set_slice(self, idx):
        slice_edge = list(range(Ed.FR, Ed.BR + 1))
        other_edge = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        a = idx  # Location
        for e in Ed:
            self.ep[e] = -1  # Invalidate all edge positions

        x = 4  # set slice edges
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0  # set the remaining edges UR..DB
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1

    def get_slice_sorted(self):
        """Get the permutation and location of the UD-slice edges FR,FL,BL and BR.
            0 <= slice_sorted < 11880 in phase 1, 0 <= slice_sorted < 24 in phase 2, slice_sorted = 0 for solved cube."""
        a = x = 0
        edge4 = [0]*4
        # First compute the index a < (12 choose 4) and the permutation array perm.
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.FR <= self.ep[j] <= Ed.BR:
                a += c_nk(11 - j, x + 1)
                edge4[3 - x] = self.ep[j]
                x += 1
        # Then compute the index b < 4! for the permutation in edge4
        b = 0
        for j in range(3, 0, -1):
            k = 0
            while edge4[j] != j + 8:
                rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1)*b + k
        return 24*a + b

    def set_slice_sorted(self, idx):
        slice_edge = [Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        other_edge = [Ed.UR, Ed.UF, Ed.UL, Ed.UB, Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        b = idx % 24  # Permutation
        a = idx // 24  # Location
        for e in Ed:
            self.ep[e] = -1  # Invalidate all edge positions

        j = 1  # generate permutation from index b
        while j < 4:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                rotate_right(slice_edge, 0, j)
                k -= 1
            j += 1

        x = 4  # set slice edges
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0  # set the remaining edges UR..DB
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1

    def get_u_edges(self):
        """Get the permutation and location of edges UR, UF, UL and UB.
            0 <= u_edges < 11880 in phase 1, 0 <= u_edges < 1680 in phase 2, u_edges = 1656 for solved cube."""
        a = x = 0
        edge4 = [0]*4
        ep_mod = self.ep[:]
        for j in range(4):
            rotate_right(ep_mod, 0, 11)
        # First compute the index a < (12 choose 4) and the permutation array perm.
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.UR <= ep_mod[j] <= Ed.UB:
                a += c_nk(11 - j, x + 1)
                edge4[3 - x] = ep_mod[j]
                x += 1
        # Then compute the index b < 4! for the permutation in edge4
        b = 0
        for j in range(3, 0, -1):
            k = 0
            while edge4[j] != j:
                rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1)*b + k
        return 24*a + b

    def set_u_edges(self, idx):
        slice_edge = [Ed.UR, Ed.UF, Ed.UL, Ed.UB]
        other_edge = [Ed.DR, Ed.DF, Ed.DL, Ed.DB, Ed.FR, Ed.FL, Ed.BL, Ed.BR]
        b = idx % 24  # Permutation
        a = idx // 24  # Location
        for e in Ed:
            self.ep[e] = -1  # Invalidate all edge positions

        j = 1  # generate permutation from index b
        while j < 4:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                rotate_right(slice_edge, 0, j)
                k -= 1
            j += 1

        x = 4  # set slice edges
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0  # set the remaining edges UR..DB
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1
        for j in range(4):
            rotate_left(self.ep, 0, 11)

    def get_d_edges(self):
        """Get the permutation and location of the edges DR, DF, DL and DB.
            0 <= d_edges < 11880 in phase 1, 0 <= d_edges < 1680 in phase 2, d_edges = 0 for solved cube."""
        a = x = 0
        edge4 = [0] * 4
        ep_mod = self.ep[:]
        for j in range(4):
            rotate_right(ep_mod, 0, 11)
        # First compute the index a < (12 choose 4) and the permutation array perm.
        for j in range(Ed.BR, Ed.UR - 1, -1):
            if Ed.DR <= ep_mod[j] <= Ed.DB:
                a += c_nk(11 - j, x + 1)
                edge4[3 - x] = ep_mod[j]
                x += 1
        # Then compute the index b < 4! for the permutation in edge4
        b = 0
        for j in range(3, 0, -1):
            k = 0
            while edge4[j] != j + 4:
                rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1) * b + k
        return 24 * a + b

    def set_d_edges(self, idx):
        slice_edge = [Ed.DR, Ed.DF, Ed.DL, Ed.DB]
        other_edge = [Ed.FR, Ed.FL, Ed.BL, Ed.BR, Ed.UR, Ed.UF, Ed.UL, Ed.UB]
        b = idx % 24  # Permutation
        a = idx // 24  # Location
        for e in Ed:
            self.ep[e] = -1  # Invalidate all edge positions

        j = 1  # generate permutation from index b
        while j < 4:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                rotate_right(slice_edge, 0, j)
                k -= 1
            j += 1

        x = 4  # set slice edges
        for j in Ed:
            if a - c_nk(11 - j, x) >= 0:
                self.ep[j] = slice_edge[4 - x]
                a -= c_nk(11 - j, x)
                x -= 1

        x = 0  # set the remaining edges UR..DB
        for j in Ed:
            if self.ep[j] == -1:
                self.ep[j] = other_edge[x]
                x += 1
        for j in range(4):
            rotate_left(self.ep, 0, 11)

    def get_corners(self):
        """Get the permutation of the 8 corners.
            0 <= corners < 40320 defined but unused in phase 1, 0 <= corners < 40320 in phase 2,
            corners = 0 for solved cube"""
        perm = list(self.cp)  # duplicate cp
        b = 0
        for j in range(Co.DRB, Co.URF, -1):
            k = 0
            while perm[j] != j:
                rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
        return b

    def set_corners(self, idx):
        self.cp = [i for i in Co]
        for j in Co:
            k = idx % (j + 1)
            idx //= j + 1
            while k > 0:
                rotate_right(self.cp, 0, j)
                k -= 1

    def get_ud_edges(self):
        """Get the permutation of the 8 U and D edges.
            ud_edges undefined in phase 1, 0 <= ud_edges < 40320 in phase 2, ud_edges = 0 for solved cube."""
        perm = self.ep[0:8]  # duplicate first 8 elements of ep
        b = 0
        for j in range(Ed.DB, Ed.UR, -1):
            k = 0
            while perm[j] != j:
                rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
        return b

    def set_ud_edges(self, idx):
        # positions of FR FL BL BR edges are not affected
        for i in list(Ed)[0:8]:
            self.ep[i] = i
        for j in list(Ed)[0:8]:
            k = idx % (j + 1)
            idx //= j + 1
            while k > 0:
                rotate_right(self.ep, 0, j)
                k -= 1
# ###################################### end coordinates for phase 1 and 2 #############################################

# ############################################ other usefull functions #################################################
    def randomize(self):
        """Generate a random cube. The probability is the same for all possible states."""
        def set_edges(idx):
            """The permutation of the 12 edges. 0 <= idx < 12!."""
            self.ep = [i for i in Ed]
            for j in Ed:
                k = idx % (j + 1)
                idx //= j + 1
                while k > 0:
                    rotate_right(self.ep, 0, j)
                    k -= 1
        set_edges(randrange(479001600))  # 12!
        p = self.edge_parity()
        while True:
            self.set_corners(randrange(40320))  # 8!
            if p == self.corner_parity():  # parities of edge and corner permutations must be the same
                break
        self.set_flip(randrange(2048))  # 2^11
        self.set_twist(randrange(2187))  # 3^7

    def verify(self):
        """Check if cubiecube is valid."""
        edge_count = [0]*12
        for i in Ed:
            edge_count[self.ep[i]] += 1
        for i in Ed:
            if edge_count[i] != 1:
                return 'Error: Some edges are undefined.'

        s = 0
        for i in Ed:
            s += self.eo[i]
        if s % 2 != 0:
            return 'Error: Total edge flip is wrong.'

        corner_count = [0] * 8
        for i in Co:
            corner_count[self.cp[i]] += 1
        for i in Co:
            if corner_count[i] != 1:
                return 'Error: Some corners are undefined.'

        s = 0
        for i in Co:
            s += self.co[i]
        if s % 3 != 0:
            return 'Error: Total corner twist is wrong.'

        if self.edge_parity() != self.corner_parity():
            return 'Error: Wrong edge and corner parity'

        return CUBE_OK
########################################################################################################################

# ################################## these cubes represent the basic cube moves ########################################
basicMoveCube = [0] * 6
basicMoveCube[Color.U] = CubieCube(cpU, coU, epU, eoU)
basicMoveCube[Color.R] = CubieCube(cpR, coR, epR, eoR)
basicMoveCube[Color.F] = CubieCube(cpF, coF, epF, eoF)
basicMoveCube[Color.D] = CubieCube(cpD, coD, epD, eoD)
basicMoveCube[Color.L] = CubieCube(cpL, coL, epL, eoL)
basicMoveCube[Color.B] = CubieCube(cpB, coB, epB, eoB)
########################################################################################################################

# ################################# these cubes represent the all 18 cube moves ########################################

moveCube = [0] * 18
for c1 in Color:
    cc = CubieCube()
    for k1 in range(3):
        cc.multiply(basicMoveCube[c1])
        moveCube[3 * c1 + k1] = CubieCube(cc.cp, cc.co, cc.ep, cc.eo)
########################################################################################################################
