import utils
import numpy as np
import math
import random

action = [-1, 0, 1]

LEARNING_CONSTANT = 0.55
EPSILON = .1
DISCOUNT_RATE = 0.4

def discretize_state(state):
    new = np.zeros(len(state), dtype= int)

    if new[0] < 0:
        new[0] = int(0)
    else:
        new[0] = int(math.floor(state[0] * 12))
        if new[0] > 11:
            new[0] = int(11)

    if new[1] < 0:
        new[1] = int(0)
    else:
        new[1] = int(math.floor(state[1] * 12))
        if new[1] > 11:
            new[1] = int(11)

    if state[2] < 0:
        new[2] = int(0)
    else:
        new[2] = int(1)

    if np.absolute(state[3]) < 0.015:
        new[3] = int(1)
    elif state[3] > 0:
        new[3] = int(2)
    else:
        new[3] = int(0)

    if new[4] < 0:
        new[4] = int(0)
    else:
        new[4] = int(math.floor(state[4] * 15)) #15 because the range for paddle is [0, 0.8]
        if new[4] > 11:
            new[4] = int(11)

    return new

#returns the smallest idx and val from the array. Randomly choose if there are equals
def choose_smallest(array):
    results = []
    smallestVal = np.amin(array)
    for count, val in enumerate(array):
        if val == smallestVal:
            results.append(count)
    if(len(results) == 0):
        print("no min found")
    return random.choice(results), smallestVal

def choose_largest(array):
    results = []
    largestVal = np.amax(array)
    for count, val in enumerate(array):
        if val == largestVal:
            results.append(count)
    if(len(results) == 0):
        print("no max found")
    return random.choice(results), largestVal


class Agent:
    def __init__(self, actions, two_sided = False):
        self.old_state = [-1,-1,-1,-1,-1]
        self.old_reward = 0
        self.old_action = 1
        self.max_bounces = 0
        self.learning_rate = LEARNING_CONSTANT / (LEARNING_CONSTANT + 1)
        self.discount_rate = DISCOUNT_RATE / (DISCOUNT_RATE + 1)
        self.epsilon = EPSILON / (EPSILON + 1)
        self.two_sided = two_sided
        self.N = utils.create_q_table()

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


    def act(self, state, bounces, done, won):
        new_state = discretize_state(state)
        new_QVals = self.Q[new_state[0]][new_state[1]][new_state[2]][new_state[3]][new_state[4]]
        old_QVals = self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]]

        if not self._train:
            if done:
                return action[1]
            else:
                qidx, maxVal = choose_largest(new_QVals)
                return action[qidx]


        new_reward = self.get_reward(bounces, done, won)
        if new_reward != 0:
            print(old_QVals)
            print("new reward")

        #Terminal
        if done:
            #May increase this so rewards for winning more influential than rewards for bouncing
            self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][self.old_action] = new_reward
            temp = self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]]
            self.max_bounces = 0
            self.old_state[0] = -1
            return action[1]

        if self.old_state[0] == -1:
            self.old_action = 0
            self.old_reward = new_reward
            self.old_state = new_state
            return 0


        self.N[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][self.old_action] += 1
        old_NVal = self.N[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]]
        self.updateRates()

        qidx, max_QVal = choose_largest(old_QVals)
        #if max_QVal != 0:
        #   print("we got a winner")
        updateVal = self.discount_rate * max_QVal - old_QVals[self.old_action]


        val = self.learning_rate * (new_reward + updateVal)
        self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][self.old_action] += val
        temp2 = self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]]


        new_action = self.choose_action(new_state)
        self.old_action = new_action
        self.old_reward = new_reward
        self.old_state = new_state

        #print(np.count_nonzero(self.Q))

        return new_action

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


    def choose_action(self, state):
        # random chance for exploration - explore the one with smallest n
        # epsilon should decraese (decreasing exploration) as the algorithm progresses
        if random.random() < EPSILON:
            nOptions = self.N[state[0]][state[1]][state[2]][state[3]][state[4]]
            n_idx, minN = choose_smallest(nOptions)
            return n_idx

        # if exploitation, simply return action with the highest Q value
        else:
            qOptions = self.N[state[0]][state[1]][state[2]][state[3]][state[4]]
            q_idx, maxQ = choose_largest(qOptions)
            return q_idx


    def updateRates(self):
        n = self.N[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][
            self.old_state[4]][self.old_action]

        self.learning_rate = LEARNING_CONSTANT / (LEARNING_CONSTANT + n)

        self.discount_rate = DISCOUNT_RATE

        self.epsilon = EPSILON


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



