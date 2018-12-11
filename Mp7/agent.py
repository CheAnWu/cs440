import utils
import numpy as np
import math
import random
from random import randint


action = [-1, 0, 1]

LEARNING_CONSTANT = .4
EPSILON = LEARNING_CONSTANT
DISCOUNT_RATE = 0.7

def discretState(state):
    new = np.zeros(len(state), dtype= int)
    new[0] = int(math.floor(state[0] * 12))
    if new[0] > 11:
        new[0] = int(11)
    new[1] = int(math.floor(state[1] * 12))
    if new[1] > 11:
        new[1] = int(11)

    if state[2] > 0:
        new[2] = int(0)
    else:
        new[2] = int(1)

    if np.absolute(state[3]) < 0.015:
        new[3] = int(0)
    elif state[3] > 0:
        new[3] = int(1)
    else:
        new[3] = int(2)

    new[4] = int(math.floor(state[4] * 15)) #15 because the range for paddle is [0, 0.8]
    if new[4] > 11:
        new[4] = int(11)

    return new


def get_reward(self, bounces, done, won):
    if done:
        if won:
            return 1
        else:
            return -1
    if bounces > self.max_bounces:
        self.max_bounces = bounces
        return 1
    return 0




def get_val(matrix, state):
    return matrix[state[0]][state[1]][state[2]][state[3]][state[4]]



class Agent:

    def choose_action(self, discret_state):
        if random.random() < self.learning_rate:
            return randint(0,2)
        else:
            maxVal, idx = self.getMax(discret_state)
            return idx

    def getMax(self, state):
        qVals = self.Q[state[0]][state[1]][state[2]][state[3]][state[4]]
        bigVal = np.argmax(qVals)
        idx = []
        for i in range(3):
            if qVals[i] == bigVal:
                idx.append(i)

        if len(idx) > 0:
            index = random.choice(idx)
            return bigVal, index
        else:
            return qVals[1], 1


    def updateQ(self, state):
        max_newQ, idx = self.getMax(state)

        oldQ = self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][
            self.old_action]


        n = self.N[state[0]][state[1]][state[2]][state[3]][
            state[4]][self.old_action]


        val = self.learning_rate * (1/self.N[state[0]][state[1]][state[2]][state[3]][
            state[4]][self.old_action]) * (self.old_reward + self.discount_rate * max_newQ - oldQ)

        return self

    def updateRates(self):
        n = self.N[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][
            self.old_state[4]][self.old_action]

        self.learning_rate = LEARNING_CONSTANT / (LEARNING_CONSTANT + n)

        self.discount_rate = DISCOUNT_RATE / (DISCOUNT_RATE + n)



    def __init__(self, actions, two_sided = False):
        self.old_state = [-1,-1,-1,-1,-1]
        self.old_reward = 0
        self.old_action = 1
        self.max_bounces = 0
        self.learning_rate = LEARNING_CONSTANT / (LEARNING_CONSTANT + 1)
        self.discount_rate = DISCOUNT_RATE / (DISCOUNT_RATE + 1)
        self.two_sided = two_sided
        self._actions = actions
        self._train = True
        self._x_bins = utils.X_BINS
        self._y_bins = utils.Y_BINS
        self._v_x = utils.V_X
        self._v_y = utils.V_Y
        self._paddle_locations = utils.PADDLE_LOCATIONS
        self._num_actions = utils.NUM_ACTIONS
        # Create the Q Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()


    def act(self, state, bounces, done, won):

        discret_state = discretState(state)

        if not self._train:
            if done:
                return 0
            maxVal, maxidx = self.getMax(discret_state)
            return action[maxidx]

        else:
            reward = 0
            if done:
                if won:
                    reward = 1
                else:
                    reward = -1

                self.max_bounces = 0
                self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][self.old_action] = reward
                self.old_action = 1
                #self.old_state[0] = -1
                self.old_reward = 0
                return action[1]


            if bounces > self.max_bounces:
                self.max_bounces = bounces
                reward = 1

            if self.old_state[0] == -1:
                self.old_action = 1
                self.old_state = discret_state.copy()
                self.old_reward = reward
                return action[1]

            self.N[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][self.old_action] += 1
            self.updateRates()
            new_action_idx = self.choose_action(discret_state)

            self.updateQ(discret_state)

            self.old_state = discret_state
            self.old_reward = reward
            self.old_action = new_action_idx

            return int(action[new_action_idx])

        return self._actions[0]

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    def save_model(self,model_path):
        # At the end of training save the trained model
        utils.save(model_path,self.Q)

    def load_model(self,model_path):
        # Load the trained model for evaluation
        self.Q = utils.load(model_path)



