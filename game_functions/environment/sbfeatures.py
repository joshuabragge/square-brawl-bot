import time
import random

from game_functions.memory import memory_reader as memory
from game_functions.memory import game_addresses as ad

#from game_functions.environment import gun_cooldown_timer as cooldown

from game_functions.game_navigation import menu_navigation as gm

from game_functions.controller import button_mappings as bm
from game_functions.controller import vjoy_controller as vjoy

vj = vjoy.vJoy()
cd = cooldown.Tread()

'''
TODO:
Seperate out feature reading logic to new file
'''


class Environment(object):

    def __init__(self):
        self.environment = 0
        self.read_p1 = False
        self.read_p2 = False
        self.switch = False
        self.p1_score_prev = -25000
        self.p2_score_prev = -25000
        self.p1_x = 0
        self.p1_y = 0
        self.p2_x = 0
        self.p2_y = 0
        self.__last_move_direction__ = 0
        self.direction = [0, 0, 0, 0]
        self.prev_coordinates = [0, 0, 0, 0]
        self.check_p2 = True
        self.check_p1 = True
        print('init')

    def make(self, delay=1):
        gm.launch_game(delay)
        print('launching game...')

    def controller(self, initialize=True, opens=False, close=False):
        if initialize:
            vj = vjoy.vJoy()
        if opens:
            vj.open()
        if close:
            vj.close()

    def start_game(self, vj_mselect=vj.mselect, botsOn=False, mode='easy'):
        gm.start_game(vj_mselect, botsOn, mode='easy')

    def initalize_memory(self):
        self.process = memory.Process("Square Brawl")

    def __grab_addresses__(self):
        '''
        Collects current address of features
        based on base address and pointers
        '''
        self.p1_health_addr = self.process.get_addr(ad.baseaddr['p1_health'],
                                                    ad.offsets['p1_health'])
        self.p2_health_addr = self.process.get_addr(ad.baseaddr['p2_health'],
                                                    ad.offsets['p2_health'])
        self.p1_x_addr = self.process.get_addr(ad.baseaddr['p1_x'],
                                               ad.offsets['p1_x'],
                                               handle=True)
        self.p1_y_addr = self.process.get_addr(ad.baseaddr['p1_y'],
                                               ad.offsets['p1_y'],
                                               handle=True)
        self.p2_x_addr = self.process.get_addr(ad.baseaddr['p2_x'],
                                               ad.offsets['p2_x'],
                                               handle=True)
        self.p2_y_addr = self.process.get_addr(ad.baseaddr['p2_y'],
                                               ad.offsets['p2_y'],
                                               handle=True)
        self.p1_score_addr = self.process.get_addr(ad.baseaddr['p1_score'],
                                                  ad.offsets['p1_score'],
                                                  handle=True)
        self.p2_score_addr = self.process.get_addr(ad.baseaddr['p2_score'],
                                                  ad.offsets['p2_score'],
                                                  handle=True)

    def __update_score__(self):
        '''
        updates the internal scoreboard
        mainly used for ensuring the features
        are not switching in memory
        '''
        self.p1_score = self.process.get_score(self.p1_score_addr)
        self.p2_score = self.process.get_score(self.p2_score_addr)

    def __grab_coordinates__(self, p1h, p1_x_addr, p1_y_addr):
        '''
        if the health is less than 0 player
        is dead and x&y coordinates increase
        randomly to large numbers
        '''
        if p1h > 0:
            time.sleep(0.01)
            p1_x = self.process.get_feature(p1_x_addr)
            time.sleep(0.01)
            p1_y = self.process.get_feature(p1_y_addr)
            self.read_p1 = False
            p1_x = float('%.1f' % (p1_x))
            p1_y = float('%.1f' % (p1_y))
            p1_dead = False
            self.check_p1 = True
        else:
            p1_x = 0
            p1_y = 0
            p1_dead = True
        return p1_x, p1_y, p1_dead

    def __features_switching_killswitch__(self, p2_dead):
        '''
        FML based on the player score
        and which character is currently
        dead, we check and make sure the
        features haven't switched places
        in memory i.e. p1 in column 1
        becomes p2 in column 1
        '''
        if self.check_p2 is True:
            # prevents the system from spamming switch
            # back and for when agent is dead
            if p2_dead is True:
                self.check_p2 = False
                if self.p1_score > self.p1_score_prev:
                    self.switch = False
                else:
                    # we know the features swapped since
                    # p1's score should have increased
                    if self.switch is True:
                        # incase switch is reversed busted
                        self.switch = False
                    else:
                        self.switch = True
                        self.check_p1 = False
                self.p2_score_prev = self.p2_score

    def __grab_features__(self):
        '''
        function to grabs the raw features from
        memory or calls functions that create
        extrapolated features
        '''
        p2h = self.process.get_feature(self.p1_health_addr)
        time.sleep(0.01)
        p1h = self.process.get_feature(self.p2_health_addr)

        if self.switch is True:
            p1h_t = p1h
            p2h_t = p2h
            p1h = p2h_t
            p2h = p1h_t

        self.__update_score__()

        p1_x, p1_y, p1_dead = self.__grab_coordinates__(p1h, self.p1_x_addr, self.p1_y_addr)
        p2_x, p2_y, p2_dead = self.__grab_coordinates__(p2h, self.p2_x_addr, self.p2_y_addr)

        self.__features_switching_killswitch__(p2_dead)
        self.__features_switching_killswitch__(p1_dead)

        locations = self.__location_features__(p1_x, p2_x, p1_y, p2_y, self.switch)
        current_direction = self.__update_current_direction__(self.__last_move_direction__)
        delta_movement = self.__movement_deltas__(p1_x, p2_x, p1_y, p2_y, self.switch)

        if self.switch is False:
            # don't change health because changed earlier
            self.features = [p1h, p1_x, p1_y,
                             p2h, p2_x, p2_y]
        else:
            self.features = [p1h, p2_x, p2_y,
                             p2h, p1_x, p1_y]

        self.features.extend(locations)
        self.features.extend([cd.gunonetimer, cd.guntwotimer])
        self.features.extend(current_direction)
        self.features.extend(delta_movement)

        # delete unnecessary features
        del self.features[-1]
        del self.features[-1]
        del self.features[-1]
        del self.features[-1]
        del self.features[3]
        del self.features[0]

        return self.features

    def __movement_deltas__(self, p1_x, p2_x, p1_y, p2_y, switch):
        if switch is False:
            p1_x_move = p1_x - self.prev_coordinates[0]
            p2_x_move = p2_x - self.prev_coordinates[1]
            p1_y_move = p1_y - self.prev_coordinates[2]
            p2_y_move = p2_y - self.prev_coordinates[3]
            self.prev_coordinates = [p1_x, p2_x, p1_y, p2_y]
        else:
            p1_x_move = p2_x - self.prev_coordinates[1]
            p2_x_move = p1_x - self.prev_coordinates[0]
            p1_y_move = p2_y - self.prev_coordinates[3]
            p2_y_move = p1_y - self.prev_coordinates[2]
            self.prev_coordinates = [p2_x, p1_x, p2_y, p1_y]
        delta_movement = [p1_x_move, p2_x_move, p1_y_move, p2_y_move]
        return delta_movement

    # features
    def __update_current_direction__(self, last_move):
        if last_move == 1:
            self.direction = [1, 0, 0, 0]
        elif last_move == 2:
            self.direction = [0, 1, 0, 0]
        elif last_move == 3:
            self.direction = [0, 0, 1, 0]
        elif last_move == 0:
            self.direction = [0, 0, 0, 1]
        elif last_move == 4:
            self.direction = self.direction
        return self.direction

    # features
    def __location_features__(self, p1_x, p2_x, p1_y, p2_y, switch):
        '''
        creates a list of dummy variables
        indicating where p2 is in relation
        to p1.
        '''
        logic for if cpu player is right, left,
        # above or below current location
        if switch is False:
            if p1_x > p2_x:
                right_of = 0
                left_of = 1
            elif p1_x < p2_x:
                right_of = 1
                left_of = 0
            else:
                right_of = 0
                left_of = 0

            if p1_y > p2_y:
                above = 1
                below = 0
            elif p1_y < p2_y:
                above = 0
                below = 1
            else:
                above = 0
                below = 0

            if abs(p1_x - p2_x) < 1:
                x_clear = 1
            else:
                x_clear = 0
            if abs(p1_y - p2_y) < 1:
                y_clear = 1
            else:
                y_clear = 0

        else:
            if p2_x > p1_x:
                right_of = 0
                left_of = 1
            elif p2_x < p1_x:
                right_of = 1
                left_of = 0
            else:
                right_of = 0
                left_of = 0

            if p2_y > p1_y:
                above = 1
                below = 0
            elif p2_y < p1_y:
                above = 0
                below = 1
            else:
                above = 0
                below = 0

            if abs(p2_x - p1_x) < 1:
                x_clear = 1
            else:
                x_clear = 0
            if abs(p2_y - p1_y) < 1:
                y_clear = 1
            else:
                y_clear = 0

        return [right_of, left_of, above, below, x_clear, y_clear]

    def observation(self):
        '''
        PRODUCTION STRENGTH
        Pulls the Square Brawl features
        and returns them as a list
        '''
        try:
            try:
                self.__grab_addresses__()
            except:
                pass
            feat = self.__grab_features__()
            return feat
        except AttributeError:
            print('Not attached to game memory. Run initialize_memory() first')

    def create_predictions(self, observation):
        '''
        For RL model that takes 1 observation
        and returns one prediction. Duplicates
        the input by the number of actions the
        agent can take in the environment. Returns
        a list of list for model prediction
        '''
        actions = [0, 1, 2, 3, 4, 5, 6, 7]
        predictions = []
        for num in actions:
            obs = observation[:]
            obs.append(num)
            predictions.append(obs)
        return predictions

    def action(self, move, delay=0.05):
        '''
        Controller has to input multiple
        variables at once. This function
        simplies the controller inputs
        by selecting actions from 0 to 7
        '''
        self._actions = 8
        if move < 5:
            self.__last_move_direction__ = move
        self.move = move
        if move == 0:
            mvx = bm.xmax
            mvy = bm.ycent
            pb = bm.none
            delay = delay
        elif move == 1:
            mvx = bm.xcent
            mvy = bm.ymin
            pb = bm.none
            delay = delay
        elif move == 2:
            mvx = bm.xmin
            mvy = bm.ycent
            pb = bm.none
            delay = delay
        elif move == 3:
            mvx = bm.xcent
            mvy = bm.ymax
            pb = bm.none
            delay = delay
        elif move == 4:
            mvx = bm.xcent
            mvy = bm.ycent
            pb = bm.none
            delay = delay
        elif move == 5:
            mvx = bm.xcent
            mvy = bm.ycent
            pb = bm.jump
            delay = delay
        elif move == 6:
            mvx = bm.xcent
            mvy = bm.ycent
            delay = delay
            pb = bm.firergun
            if cd.gunonetimer == 0:
                cd.guncounterone()
        elif move == 7:
            mvx = bm.xcent
            mvy = bm.ycent
            delay = delay
            pb = bm.firelgun
            if cd.guntwotimer == 0:
                cd.guncountertwo()
        else:
            mvx = bm.xcent
            mvy = bm.ycent
            pb = bm.none
            delay = delay
        vj.aim(x=mvx, y=mvy, button=pb, delay=delay)
        return move

    def reward_structure(self, p1_death, p2_death, p1_damage, p2_damage):
        '''
        Sets the values used in the reward
        structure for our agent
        '''
        self.p1_death = p1_death
        self.p2_death = p2_death
        self.p1_damage = p1_damage
        self.p2_damage = p2_damage
        return print('Reward structure defined!')

    def action_checker(self, action, reward, cooldownstates):
        '''
        Depreciated - if opponent dies,
        agent could only get rewards
        when weapons were on cooldown
        '''
        if reward <= 0:
            return action
        else:
            if cooldownstates[0] > cooldownstates[1]:
                return 6
            else:
                return 7

    def reward(self, stale_observation, new_observation):
        '''
        Calculates the amount of reward our
        agent is set to recieve based on the
        reward structure and the difference
        between last state and current.
        '''
        rewards = []
        p1h_old = stale_observation[0]
        p1h_new = new_observation[0]
        p2h_old = stale_observation[3]
        p2h_new = new_observation[3]
        # Death Management
        try:
            if p1h_new < p1h_old:
                if p1h_new <= 0:
                    ph1_delta = (p1h_old - 0)*self.p1_damage
                    rewards.append(self.p1_death + ph1_delta)
                else:
                    ph1_delta = (p1h_old - p1h_new)*self.p1_damage
                    rewards.append(ph1_delta)
            else:
                rewards.append(0)

            if p2h_new < p2h_old:
                if p2h_new <= 0:
                    ph2_delta = (p2h_old - 0)*self.p2_damage
                    rewards.append(self.p2_death + ph2_delta)
                else:
                    ph2_delta = (p2h_old - p2h_new)*self.p2_damage
                    rewards.append(ph2_delta)
            else:
                rewards.append(0)

            rewards.append(0)
            return sum(rewards)
        except AttributeError:
            print('Define the reward structure with reward_structure')

    def action_decay(self, last_action, move_list,
                     decay_rate=0.11, fire_decay=True):
        '''
        Depreciated - used to devalue the
        predicted value for each move when
        based on how recently it was performed
        '''
        del move_list[0]
        move_list.append(last_action)
        decay = [(decay_rate**(i+2)) for i in range(len(move_list), -1, -1)]
        d = dict(zip(move_list, decay))
        all_moves = [0, 1, 2, 3, 4, 5, 6, 7]

        for move in all_moves:
            if move not in list(d.keys()):
                d[move] = 0
        if fire_decay:
            fire_decay = [0, 1, 2, 3, 4, 5]
            for move in fire_decay:
                d[move] = 0
        return d
