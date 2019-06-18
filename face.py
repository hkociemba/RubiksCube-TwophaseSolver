# ####### The cube on the facelet level is described by positions of the colored stickers. #############################

from defs import cornerFacelet, edgeFacelet, cornerColor, edgeColor
from enums import Color, Corner, Edge
from cubie import CubieCube


class FaceCube:
    """Represent a cube on the facelet level with 54 colored facelets."""
    def __init__(self):
        self.f = []
        for i in range(9):
            self.f.append(Color.U)
        for i in range(9):
            self.f.append(Color.R)
        for i in range(9):
            self.f.append(Color.F)
        for i in range(9):
            self.f.append(Color.D)
        for i in range(9):
            self.f.append(Color.L)
        for i in range(9):
            self.f.append(Color.B)

    def __str__(self):
        return self.to_string()

    def from_string(self, s):
        """Construct a facelet cube from a string. See class Facelet(IntEnum) in enums.py for string format."""
        if len(s) < 54:
            return 'Error: Cube definition string ' + s + ' contains less than 54 facelets.'
        elif len(s) > 54:
            return 'Error: Cube definition string ' + s + ' contains more than 54 facelets.'
        cnt = [0] * 6
        for i in range(54):
            if s[i] == 'U':
                self.f[i] = Color.U
                cnt[Color.U] += 1
            elif s[i] == 'R':
                self.f[i] = Color.R
                cnt[Color.R] += 1
            elif s[i] == 'F':
                self.f[i] = Color.F
                cnt[Color.F] += 1
            elif s[i] == 'D':
                self.f[i] = Color.D
                cnt[Color.D] += 1
            elif s[i] == 'L':
                self.f[i] = Color.L
                cnt[Color.L] += 1
            elif s[i] == 'B':
                self.f[i] = Color.B
                cnt[Color.B] += 1
        if all(x == 9 for x in cnt):
            return True
        else:
            return 'Error: Cube definition string ' + s + ' does not contain exactly 9 facelets of each color.'


    def to_string(self):
        """Give a string representation of the facelet cube."""
        s = ''
        for i in range(54):
            if self.f[i] == Color.U:
                s += 'U'
            elif self.f[i] == Color.R:
                s += 'R'
            elif self.f[i] == Color.F:
                s += 'F'
            elif self.f[i] == Color.D:
                s += 'D'
            elif self.f[i] == Color.L:
                s += 'L'
            elif self.f[i] == Color.B:
                s += 'B'
        return s

    def to_2dstring(self):
        """Give a 2dstring representation of a facelet cube."""
        s = self.to_string()
        r = '   ' + s[0:3] + '\n   ' + s[3:6] + '\n   ' + s[6:9] + '\n'
        r += s[36:39] + s[18:21] + s[9:12] + s[45:48] + '\n' + s[39:42] + s[21:24] + s[12:15] + s[48:51] \
            + '\n' + s[42:45] + s[24:27] + s[15:18] + s[51:54] + '\n'
        r += '   ' + s[27:30] + '\n   ' + s[30:33] + '\n   ' + s[33:36] + '\n'
        return r

    def to_cubie_cube(self):
        """Return a cubie representation of the facelet cube."""
        cc = CubieCube()
        cc.cp = [-1] * 8  # invalidate corner and edge permutation
        cc.ep = [-1] * 12
        for i in Corner:
            fac = cornerFacelet[i]  # facelets of corner  at position i
            for ori in range(3):
                if self.f[fac[ori]] == Color.U or self.f[fac[ori]] == Color.D:
                    break
            col1 = self.f[fac[(ori + 1) % 3]]  # colors which identify the corner at position i
            col2 = self.f[fac[(ori + 2) % 3]]
            for j in Corner:
                col = cornerColor[j]  # colors of corner j
                if col1 == col[1] and col2 == col[2]:
                    cc.cp[i] = j  # we have corner j in corner position i
                    cc.co[i] = ori
                    break

        for i in Edge:
            for j in Edge:
                if self.f[edgeFacelet[i][0]] == edgeColor[j][0] and \
                        self.f[edgeFacelet[i][1]] == edgeColor[j][1]:
                    cc.ep[i] = j
                    cc.eo[i] = 0
                    break
                if self.f[edgeFacelet[i][0]] == edgeColor[j][1] and \
                        self.f[edgeFacelet[i][1]] == edgeColor[j][0]:
                    cc.ep[i] = j
                    cc.eo[i] = 1
                    break
        return cc
