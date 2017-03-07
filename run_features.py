import gamemangement as gm
import buttonmap as bm
import locations
import cooldown as cd
import sbfeatures
import vjoy
import time

cdt = cd.Tread()

sbf = sbfeatures.Features()
sbf.grab_addresses()



for i in range(100000):
    time.sleep(0.1)
    try:
        sbf.grab_addresses()
    except:
        sbf.grab_features()
    print(sbf.grab_features())
    # print(sbf.testp1())
    time.sleep(0.2)
