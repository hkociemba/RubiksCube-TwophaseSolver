import solver as sv
import cubie
import face


def test(n, t):
    """
    :param n: The number of generated random cubes
    :param t: The time in seconds to
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

# test(1000,10): { 14: 0, 15: 1, 16: 8, 17: 51, 18: 242, 19: 532, 20: 166, 21: 0}, average 18.794 moves
# test(1000,1): { 14: 0, 15: 2, 16: 4, 17: 28, 18: 127, 19: 401, 20: 405, 21: 33, 22: 0}, average 19.268 moves
# test(1000,0.1): { 15: 0, 16: 2, 17: 6, 18: 46, 19: 186, 20: 451, 21: 293, 22: 16, 23: 0}, average 20.021 moves
# test(1000,0.01): { 15: 0, 16: 1, 17: 2, 18: 10, 19: 95, 20: 350, 21: 512, 22: 30, 23: 0}, average 20.447 moves