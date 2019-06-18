# ######################################## Miscellaneous functions #####################################################

def rotate_right(arr, l, r):
    """"Rotate array arr right between l and r. r is included."""
    temp = arr[r]
    for i in range(r, l, -1):
        arr[i] = arr[i-1]
    arr[l] = temp


def rotate_left(arr, l, r):
    """"Rotate array arr left between l and r. r is included."""
    temp = arr[l]
    for i in range(l, r):
        arr[i] = arr[i+1]
    arr[r] = temp


def c_nk(n, k):
    """Binomial coefficient [n choose k]."""
    if n < k:
        return 0
    if k > n // 2:
        k = n - k
    s, i, j = 1, n, 1
    while i != n - k:
        s *= i
        s //= j
        i -= 1
        j += 1
    return s
