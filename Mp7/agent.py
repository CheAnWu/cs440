import utils
import numpy as np
import math
import random





def discretState(state):
    new = np.zeros(len(state), dtype= int)
    new[0] = int(math.floor(state[0] * 12))
    if new[0] > 11:
        new[0] = int(11)
    new[1] = int(math.floor(state[1] * 12))
    if new[1] > 11:
        new[1] = int(11)

    if state[2] > 0:
        new[2] = int(1)
    else:
        new[2] = int(2)

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
        print(discret_state)
        print(type(discret_state[0]))
        print(self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][0])
        print(self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][1])
        print(self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][2])

        qActions = self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]].copy()

        maxQ = max(qActions)

      #  if random.random() < self.learning_rate:
       #     best = [i for i in range(len(self._actions)) if qActions[i] == maxQ]
       #     i = random.choice(best)
       # else:
        #    i = random.choice(np.where(qActions == maxQ))

        #action = self._actions[i]
        action = random.randint(0,2)
        print(action)
        return action


    
    def __init__(self, actions, two_sided = False):
        self.old_state = [-1,-1,-1,-1,-1]
        self.old_reward = 0
        self.old_action = 0
        self.max_bounces = 0
        self.learning_rate = .2 #will need to update
        #rate of decay is C/(C + N(s,a))
        self.discount_rate = .2 #need to update
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
        if not self._train:
            if done:
                return 0

        discret_state = discretState(state)

        #Do we only need this for train


        #if terminal then update q with new r



        if self._train:  #explore and exploit
            #increment N[s, a]
            #Update Q[s,a] <-- Q[s,a] + learning*N[s,a] * (r + discount * max Q[s', a'] - Q[s,a])
            #self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]]

            reward = 0
            if done:
                if won:
                    reward = 1
                else:
                    reward = -1
                self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][self.old_action] = reward
                self.old_action = 0
                self.old_state[0] = -1
                self.old_reward = 0
                return 0

            if bounces > self.max_bounces:
                self.max_bounces = bounces
                reward = 1

            new_action = self.choose_action(discret_state)
            if self.old_state[0] == -1:
                self.old_action = new_action
                self.old_state = discret_state.copy()
                self.old_reward = reward
                return new_action

            max = self.Q[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][new_action] - self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][self.old_action]

            self.N[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][self.old_action] += 1
            self.Q[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][self.old_action] += self.learning_rate * self.N[discret_state[0]][discret_state[1]][discret_state[2]][discret_state[3]][discret_state[4]][self.old_action] * (self.old_reward + self.discount_rate * max)

            self.old_state = discret_state
            self.old_reward = reward
            self.old_action = new_action

            #print(type(int(new_action)))
            return int(new_action)


            #update Q table and return best action
        else:
            #exploit
            print("testing")
            return 0

        print(type(self._actions[0]))
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



