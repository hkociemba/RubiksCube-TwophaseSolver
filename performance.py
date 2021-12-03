import solver as sv
import cubie
import face


def test(n, t):
    """
    :param n: The number of generated random cubes
    :param t: The time in seconds to spend on each cube
    :return: A dictioneary with the solving statistics
    """
    cc = cubie.CubieCube()
    fc = face.FaceCube()
    cnt = [0] * 31
    for i in range(n):
        cc.randomize()
        fc = cc.to_facelet_cube()
        s = fc.to_string()
        print(s)
        s = sv.solve(s, 0, t)
        print(s)
        print()
        cnt[int(s.split('(')[1].split('f')[0])] += 1
    avr = 0
    for i in range(31):
        avr += i*cnt[i]
    avr /= n
    return 'average ' + '%.2f' % avr + ' moves', dict(zip(range(31), cnt))

# test results on AMD Ryzen 7 3700X 3.59 GHz

# test(1000,30): {14: 0, 15: 2, 16: 12, 17: 74, 18: 279, 19: 534, 20: 99, 21: 0}, average 18.63 moves
# test(1000,10): { 14: 0, 15: 1, 16: 8, 17: 51, 18: 242, 19: 532, 20: 166, 21: 0}, average 18.79 moves
# test(1000,1): { 14: 0, 15: 2, 16: 4, 17: 28, 18: 127, 19: 401, 20: 405, 21: 33, 22: 0}, average 19.27 moves
# test(10000,1): { 13: 0, 14: 1, 15: 2, 16: 54, 17: 251, 18: 1295, 19: 4047, 20: 4004, 21: 346, 22: 0}, average 19.27 moves
# test(1000,0.1): { 15: 0, 16: 2, 17: 6, 18: 46, 19: 186, 20: 451, 21: 293, 22: 16, 23: 0}, average 20.02 moves
# test(1000,0.01): { 15: 0, 16: 1, 17: 2, 18: 10, 19: 95, 20: 350, 21: 512, 22: 30, 23: 0}, average 20.44 moves

# For comparison: Tomas Rokicki 2010 solved 1.000.000 random cubes *optimally* on a machine with 256 GB of RAM
# {11: 0, 12: 1, 13: 14, 14: 172, 15: 2063, 16: 26448, 17: 267027, 18: 670407, 19: 33868, 20: 0}, average 17.71 moves
