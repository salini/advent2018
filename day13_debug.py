
from day13 import _load_track

import pylab as pl
import png
import numpy as np


def draw_track(track, outfile):
    symbol = {
ord(" "): np.zeros((5,5)),
ord("-"): np.array([[0,0,0,0,0],[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [0,0,0,0,0]]),
ord("|"): np.array([[0,1,1,1,0],[0,1,1,1,0], [0,1,1,1,0], [0,1,1,1,0], [0,1,1,1,0]]),
ord("+"): np.array([[0,1,1,1,0],[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [0,1,1,1,0]]),
"-/": np.array([[0,1,1,1,0],[1,1,1,1,0], [1,1,1,0,0], [1,1,0,0,0], [0,0,0,0,0]]),
"/-": np.array([[0,0,0,0,0],[0,0,0,1,1], [0,0,1,1,1], [0,1,1,1,1], [0,1,1,1,0]]),
"-\\": np.array([[0,0,0,0,0],[1,1,0,0,0], [1,1,1,0,0], [1,1,1,1,0], [0,1,1,1,0]]),
"\\-": np.array([[0,1,1,1,0],[0,1,1,1,1], [0,0,1,1,1], [0,0,0,1,1], [0,0,0,0,0]]),
    }

    N = 5
    m = track.map
    Nrow, Ncol = m.shape
    img = np.zeros((N*Nrow, N*Ncol))
    for row in range(Nrow):
        for col in range(Ncol):
            subimg = img[N*row:N*row+N, N*col:N*col+N]
            if m[row,col] in [ord(" "), ord("-"), ord("|"), ord("+")]:
                img[N*row:N*row+N, N*col:N*col+N] = symbol[m[row,col]]
            elif m[row, col] == ord("/"):
                if col>0 and m[row, col-1] == ord("-"):
                    img[N*row:N*row+N, N*col:N*col+N] = symbol["-/"]
                elif  col>0 and m[row, col-1] == ord("+"):
                    if row>0 and m[row-1, col] in [ord("+"), ord("|")]:
                        img[N*row:N*row+N, N*col:N*col+N] = symbol["-/"]
                    else:
                        img[N*row:N*row+N, N*col:N*col+N] = symbol["/-"]
                else:
                    img[N*row:N*row+N, N*col:N*col+N] = symbol["/-"]
            elif m[row, col] == ord("\\"):
                if col>0 and m[row, col-1] == ord("-"):
                    img[N*row:N*row+N, N*col:N*col+N] = symbol["-\\"]
                elif  col>0 and m[row, col-1] == ord("+"):
                    if row<Nrow-1 and m[row+1, col] in [ord("+"), ord("|")]:
                        img[N*row:N*row+N, N*col:N*col+N] = symbol["-\\"]
                    else:
                        img[N*row:N*row+N, N*col:N*col+N] = symbol["\\-"]
                else:
                    img[N*row:N*row+N, N*col:N*col+N] = symbol["\\-"]

    img = np.array([(255,255,255,255) if x==1 else (0,0,0,0) for x in img.flatten()], dtype=np.uint8).reshape((N*Nrow, N*Ncol, 4))
    png.from_array(img, 'RGBA').save(outfile)



def draw_kart_traj(kart, dim, c, outfile):
    symbol = {
"S": np.array([[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1]]),
"X": np.array([[1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1]]),
">": np.array([[0,0,0,0,0], [1,1,1,0,0], [1,1,1,1,0], [1,1,1,0,0], [0,0,0,0,0]]),
"<": np.array([[0,0,0,0,0], [0,0,1,1,1], [0,1,1,1,1], [0,0,1,1,1], [0,0,0,0,0]]),
"v": np.array([[0,1,1,1,0], [0,1,1,1,0], [0,1,1,1,0], [0,0,1,0,0], [0,0,0,0,0]]),
"^": np.array([[0,0,0,0,0], [0,0,1,0,0], [0,1,1,1,0], [0,1,1,1,0], [0,1,1,1,0]]),
    }

    N = 5
    Nrow, Ncol = dim
    img = np.zeros((N*Nrow, N*Ncol))
    coord = kart.trajectory[0][1]
    row, col = coord
    img[N*row:N*row+N, N*col:N*col+N] += symbol["S"]
    for state, coord in kart.trajectory:
        row, col = coord
        img[N*row:N*row+N, N*col:N*col+N] += symbol[state]
    img = np.array([(c[0]*255,c[1]*255,c[2]*255,255) if x>=1 else (0,0,0,0) for x in img.flatten()], dtype=np.uint8).reshape((N*Nrow, N*Ncol, 4))
    png.from_array(img, 'RGBA').save(outfile)


def get_last_kart_coordinate_with_images():
    #track = _load_track_example2()
    track = _load_track()
    print track
    print "%d karts remaining" % len(track.karts)
    draw_track(track, "day13_00_track.png")

    N = 10000
    NKart = len(track.karts)
    KK = 0
    cmap = pl.cm.get_cmap('hsv')
    for i in range(N):
        print "================",i
        #print "%d karts remaining" % len(track.karts)
        res = track.do_tick()
        #print track

        collisions = track.clean_crashed_karts()
        if collisions:
            for c in collisions:
                draw_kart_traj(c, track.map.shape, cmap(KK/float(NKart)), "day13_coll_{0}.png".format(KK))
                KK += 1
            print "Collision(s) occured"
            print "%d karts remaining" % len(track.karts)

        if len(track.karts) == 1:
            print track
            c = track.karts[0].coordinate()
            print c.trajectory
            return (c[1], c[0]) #inverted

        elif len(track.karts) == 0:
            print "no more karts!"
            return None

    return None


if __name__ == '__main__':
    get_last_kart_coordinate_with_images()