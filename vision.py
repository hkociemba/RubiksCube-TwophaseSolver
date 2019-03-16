# pip install opencv_python-3.2.0-cp36-cp36m-win_amd64.whl


import cv2
import numpy as np
import time

rgb_L = 50  # 30, maximieren

sigma_W = 300  # 10-300
sat_W_max = 60  # 60
val_W_min = 150  # 120

sigma_C = 5  # 5
delta_C = 5   # 5

orange_L = 6  # 10 bei Tag 6,7
orange_H = 23  # 25 bei Tag
yellow_H = 50
green_H = 100  # 110
blue_H = 160

grid_N = 25


def drawgrid(img, n):
    h, w = img.shape[:2]
    sz = h // n
    border = 1 * sz
    for y in range(border, h - border, sz):
        for x in range(border, w - border, sz):
            cv2.rectangle(img, (x, y), (x + sz, y + sz), (0, 0, 0), 1)  # plot small squares in black and white
            cv2.rectangle(img, (x - 1, y - 1), (x + 1 + sz, y + 1 + sz), (255, 255, 255), 1)


def del_duplicates(pts):
    dele = True
    while dele:
        dele = False
        r = range(len(pts))
        for i in r:
            for j in r[i + 1:]:
                if np.linalg.norm(pts[i] - pts[j]) < 20:
                    del pts[j]
                    dele = True
                if dele:
                    break
            if dele:
                break


def medoid(pts):
    res = np.array([0.0, 0.0])
    smin = 100000
    for i in pts:
        s = 0
        for j in pts:
            s += np.linalg.norm(i - j)
        if s < smin:
            smin = s
            res = i

    return res


def facelets(pts, med):
    # pts sind alle erkannten facelets, m der Medoid
    ed = []
    co = []
    if med[0] == 0:
        return co, ed  # no edgefacelets detected
    # find shortest distance
    dmin = 10000
    for p in pts:
        d = np.linalg.norm(p - med)
        if 1 < d < dmin:
            dmin = d
    # edgefacelets should be in a distance not more than dmin*1.3
    for p in pts:
        d = np.linalg.norm(p - med)
        if dmin - 1 < d < dmin * 1.3:
            ed.append(p)
    # now find the corner facelets
    for p in pts:
        d = np.linalg.norm(p - med)
        if dmin * 1.3 < d < dmin * 1.7:
            co.append(p)
    return co, ed


def antifacelets(co, ed, med):
    global width
    aef = []
    acf = []
    for p in ed:
        pa = 2 * med - p
        aef.append(pa)
    for p in co:
        pa = 2 * med - p
        acf.append(pa)

    # delete duplicates
    delta = width / 15
    for k in range(len(aef) - 1, -1, -1):
        for p in ed:
            if np.linalg.norm(aef[k] - p) < delta:
                del aef[k]
                break

    for k in range(len(acf) - 1, -1, -1):
        for p in co:
            if np.linalg.norm(acf[k] - p) < delta:
                del acf[k]
                break

    return acf, aef


def getcolor(p):
    global hsv
    sz = 10
    p = p.astype(np.uint16)
    rect = hsv[p[1] - sz:p[1] + sz, p[0] - sz:p[0] + sz]
    median = np.sum(rect, axis=(0, 1)) / sz / sz / 4
    mh, ms, mv = median
    if ms < sat_W_max and mv > val_W_min:
        cv2.putText(
            bgrcap, 'white', tuple(p-(15,-3)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    elif orange_L <= mh < orange_H:
        cv2.putText(
            bgrcap, 'orange', tuple(p - (20, -3)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    elif orange_H <= mh < yellow_H:
        cv2.putText(
            bgrcap, 'yellow', tuple(p - (18, -3)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0  ), 1)
    elif yellow_H <= mh < green_H:
        cv2.putText(
            bgrcap, 'green', tuple(p - (18, -3)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    elif green_H <= mh < blue_H:
        cv2.putText(
            bgrcap, 'blue', tuple(p - (18, -3)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    else:
        cv2.putText(
            bgrcap, 'red', tuple(p - (15, -3)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)


def find_squares(n):
    global hsv, r_mask, color_mask, white_mask, black_filter

    h, s, v = cv2.split(hsv)
    h_sqr = np.square(h)

    sz = height // n
    border = 1 * sz

    varmax_edges = 20  # wichtig
    for y in range(border, height - border, sz):
        for x in range(border, width - border, sz):

            # rect_h = h[y:y + sz, x:x + sz]
            rect_h = h[y:y + sz, x:x + sz]
            rect_h_sqr = h_sqr[y:y + sz, x:x + sz]

            median_h = np.sum(rect_h) / sz / sz

            sqr_median_hf = median_h * median_h
            median_hf_sqr = np.sum(rect_h_sqr) / sz / sz
            var = median_hf_sqr - sqr_median_hf

            sigma = np.sqrt(var)

            delta = delta_C

            if sigma < sigma_W:  # sigma liegt für weiß höher, 10-100

                ex_rect = hsv[y - 1 * sz:y + 2 * sz, x - 1 * sz:x + 2 * sz].copy()  # warum copy?
                r_mask = cv2.inRange(ex_rect, (0, 0, val_W_min),
                                     (255, sat_W_max, 255))  # saturation high 30, value low 180
                r_mask = cv2.bitwise_or(r_mask, white_filter[y - 1 * sz:y + 2 * sz, x - 1 * sz:x + 2 * sz])
                white_filter[y - 1 * sz:y + 2 * sz, x - 1 * sz:x + 2 * sz] = r_mask

            if sigma < sigma_C:  # übrigen echten Farben  1-3
                ex_rect = h[y - 1 * sz:y + 2 * sz, x - 1 * sz:x + 2 * sz].copy()  # warum copy?
                if median_h + delta >= 180:
                    r_mask = cv2.inRange(ex_rect, 0, median_h + delta - 180)
                    r_mask = cv2.bitwise_or(r_mask, cv2.inRange(ex_rect, median_h - delta, 180))
                elif median_h - delta < 0:
                    r_mask = cv2.inRange(ex_rect, median_h - delta + 180, 180)
                    r_mask = cv2.bitwise_or(r_mask, cv2.inRange(ex_rect, 0, median_h + delta))
                else:
                    r_mask = cv2.inRange(ex_rect, median_h - delta, median_h + delta)

                r_mask = cv2.bitwise_or(r_mask, color_filter[y - 1 * sz:y + 2 * sz, x - 1 * sz:x + 2 * sz])
                color_filter[y - 1 * sz:y + 2 * sz, x - 1 * sz:x + 2 * sz] = r_mask

    black_filter = cv2.inRange(bgrcap, (0, 0, 0), (rgb_L, rgb_L, rgb_L))  # wichtiger parameter 30-50
    black_filter = cv2.bitwise_not(black_filter)

    color_filter = cv2.bitwise_and(color_filter, black_filter)
    color_filter = cv2.blur(color_filter, (20, 20))
    color_filter = cv2.inRange(color_filter, 240, 255)

    white_filter = cv2.bitwise_and(white_filter, black_filter)
    white_filter = cv2.blur(white_filter, (20, 20))
    white_filter = cv2.inRange(white_filter, 240, 255)

    itr = iter([color_filter, white_filter])

    for j in itr:
        im2, contours, hierarchy = cv2.findContours(j, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for n in range(len(contours)):
            approx = cv2.approxPolyDP(contours[n], sz // 2, True)
            if approx.shape[0] < 4 or approx.shape[0] > 4:
                continue
            corners = approx[:, 0]

            edges = np.array(
                [cv2.norm(corners[0] - corners[1], cv2.NORM_L2), cv2.norm(corners[1] - corners[2], cv2.NORM_L2),
                 cv2.norm(corners[2] - corners[3], cv2.NORM_L2),
                 cv2.norm(corners[3] - corners[0], cv2.NORM_L2)])
            edges_mean_sq = (np.sum(edges) / 4) ** 2
            edges_sq_mean = np.sum(np.square(edges)) / 4
            if edges_sq_mean - edges_mean_sq > varmax_edges:
                continue
            # cv2.drawContours(bgrcap, [approx], -1, (0, 0, 255), 8)
            middle = np.sum(corners, axis=0) / 4
            cent.append(np.asarray(middle))


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('cube.avi')

while 1:

    # Take each frame
    _, bgrcap = cap.read()  #

    height, width = bgrcap.shape[:2]
    bgrcap = cv2.blur(bgrcap, (5, 5))
    hsv = cv2.cvtColor(bgrcap, cv2.COLOR_BGR2HSV).astype(float)
    color_mask = cv2.inRange(bgrcap, np.array([1, 1, 1]), np.array([0, 0, 0]))  # mask for colors
    white_mask = cv2.inRange(bgrcap, np.array([1, 1, 1]), np.array([0, 0, 0]))  # special mask for white

    cent = []
    find_squares(grid_N)
    del_duplicates(cent)
    # for i in cent:
    #     cv2.circle(bgrcap, txple(i.astype(np.uint16)), 5, (128, 128, 128), -1)
    m = medoid(cent)

    ef, cf = facelets(cent, m)
    acf, aef = antifacelets(cf, ef, m)

    getcolor(m)
    for i in ef:
        getcolor(i)
    for i in cf:
        getcolor(i)
    for i in aef:
        getcolor(i)
    for i in acf:
        getcolor(i)

    # drawgrid(bgrcap, grid_N)
    cv2.imshow('mask', cv2.resize(color_mask, (width // 2, height // 2)))
    cv2.imshow('white_filter', cv2.resize(white_mask, (width // 2, height // 2)))
    cv2.imshow('black_filter', cv2.resize(black_filter, (width // 2, height // 2)))
    cv2.imshow('bgr', bgrcap)

    k = cv2.waitKey(5) & 0xFF
    if k == 120:  # x
        break

cv2.destroyAllWindows()
