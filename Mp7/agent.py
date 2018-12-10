import utils
import numpy as np
import math
import random





def discretState(state):
    new = np.zeros(len(state))
    new[0] = int(math.floor(state[0] * 12))
    if new[0] > 11:
        new[0] = 11
    new[1] = int(math.floor(state[1] * 12))
    if new[1] > 11:
        new[1] = 11

    if state[2] > 0:
        new[2] = 1
    else:
        new[2] = -1

    if math.abs(state[3]) < 0.015:
        new[3] = 0
    if state[3] > 0:
        new[3] = 1
    else:
        new[3] = -1

    new[4] = int(math.floor(state[4] * 15)) #15 because the range for paddle is [0, 0.8]
    if new[4] > 11:
        new[4] = 11

    return new


def choose_action(self, discret_state):
    qActions = self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]]

    maxQ = max(qActions)

    if random.random() < self.epsilon:
        best = [i for i in range(len(self._actions)) if qActions[i] == maxQ]
        i = random.choice(best)
    else:
        i = qActions.index(maxQ)

    action = self._actions[i]

    return action



class Agent:
    def getReward(self, bounces, done, won):
        if done:
            if won:
                return 1
            else:
                return -1
        if bounces > self.max_bounces:
            self.max_bounces = bounces
            return 1
        return 0
    
    def __init__(self, actions, two_sided = False):
        self.max_bounces = 0
        self.learning_rate = 1 #will need to update
        #rate of decay is C/(C + N(s,a))
        self.discount_rate = 1 #need to update
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


    def act(self, state, bounces, done, won):
         #TODO - fill out this function
        discret_state = discretState(state)

        #Do we only need this for train
        reward = getReward(self, bounces, done, won)

        #if terminal then update q with new r


        if self.train:  #explore and exploit
            #increment N[s, a]
            #Update Q[s,a] <-- Q[s,a] + learning*N[s,a] * (r + discount * max Q[s', a'] - Q[s,a])


            return 0

            #update Q table and return best action
        else:
            #exploit
            return 0

            #return action from Q table
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



