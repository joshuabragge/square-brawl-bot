import time
import numpy as np
import buttonmap as bm
import vjoy


# initialize
vj = vjoy.vJoy()
vj.open()


def random_actions(array):
    xmove = array[:3]
    ymove = array[3:6]
    push = array[6:]
    xmove_index = np.where(array == max(xmove))[0]
    ymove_index = np.where(array == max(ymove))[0]
    push_index = np.where(array == max(push))[0]
    if xmove_index == 0:
        mvx = bm.xmax
    if xmove_index == 1:
        mvx = bm.xcent
    if xmove_index == 2:
        mvx = bm.xmin
    if ymove_index == 3:
        mvy = bm.ymax
    if ymove_index == 4:
        mvy = bm.ycent
    if ymove_index == 5:
        mvy = bm.ymin
    if push_index == 6:
        pb = bm.firergun
    if push_index == 7:
        pb = bm.firelgun
    if push_index == 8:
        pb = bm.none
    if push_index == 9:
        pb = bm.jump
    return mvx, mvy, pb


while True:
    rand = np.random.uniform(low=0, high=1, size=(10,))
    xmv, ymv, pb = random_actions(rand)
    print(xmv, ymv, pb)
    vj.aim(x=xmv, y=ymv, button=pb)
    time.sleep(0.3)
