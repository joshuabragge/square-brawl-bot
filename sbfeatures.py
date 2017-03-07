import memory
import addresses as ad
import cooldown as cd
import time

global p1_x
global p1_y
global p2_x
global p2_y

p1_x = 0
p1_y = 0
p2_x = 0
p2_y = 0

class Features(object):

    def __init__(self):
        self.process = memory.Process("Square Brawl")

    def grab_addresses(self):

        self.p1_health_addr = self.process.get_addr(ad.baseaddr['p1_health'],
                                                    ad.offsets['p1_health'])
        self.p2_health_addr = self.process.get_addr(ad.baseaddr['p2_health'],
                                                    ad.offsets['p2_health'])
        self.p1_x_addr = self.process.get_addr(ad.baseaddr['p1_x'],
                                                ad.offsets['p1_x'], handle=True)
        self.p1_y_addr = self.process.get_addr(ad.baseaddr['p1_y'],
                                                ad.offsets['p1_y'], handle=True)
        self.p2_x_addr = self.process.get_addr(ad.baseaddr['p2_x'],
                                                ad.offsets['p2_x'], handle=True)
        self.p2_y_addr = self.process.get_addr(ad.baseaddr['p2_y'],
                                                ad.offsets['p2_y'], handle=True)

    # intiate features
    def grab_features(self):
            p1h = self.process.get_feature(self.p1_health_addr)

            if p1h > 0:
                time.sleep(0.02)
                p1_x = self.process.get_feature(self.p1_x_addr)
                time.sleep(0.02)
                p1_y = self.process.get_feature(self.p1_y_addr)
            else:
                p1_x = 0
                p1_y = 0
            time.sleep(0.02)
            p2h = self.process.get_feature(self.p2_health_addr)

            if p2h > 0:
                time.sleep(0.02)
                p2_x = self.process.get_feature(self.p2_x_addr)
                time.sleep(0.0)
                p2_y = self.process.get_feature(self.p2_y_addr)
            else:
                p2_x = 0
                p2_y = 0

            features = [p1h, p1_x, p1_y,
                        p2h, p2_x, p2_y,
                        cd.gunonetimer, cd.guntwotimer]
            return features

    def testp1(self):
        p1_y = self.process.get_feature(self.p1_y_addr)
        time.sleep(0.02)
        p1_x = self.process.get_feature(self.p1_x_addr)
        time.sleep(0.02)
        return print("(", p1_x, ",", p1_y, ")")

    def testp2(self):
        p2_x = self.process.get_feature(self.p2_x_addr)
        time.sleep(0.02)
        p2_y = self.process.get_feature(self.p2_y_addr)
        time.sleep(0.01)
        return print("(", p2_x, ",", p2_y, ")")
