import gym
import numpy as np
from shobu import *  # Assuming SHOBU class is implemented in a module called shobu

class SHOBUEnv(gym.Env):
    def __init__(self):
        super(SHOBUEnv, self).__init__()
        self.game = ShobuGame()  # Instantiate the SHOBU game
        self.state = self.game.initial  # Initial state
        self.action_space = gym.spaces.Discrete(len(self.game.actions(self.state)))  # Dynamic action space
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(32,), dtype=np.float32)  # Define observation space
        
    def reset(self):
        # Reset the environment to its initial state
        self.game = ShobuGame()  # Re-instantiate the SHOBU game
        return self.game.initial  # Return initial state

    def step(self, action):
        # Take a step in the environment based on the given action
        reward = 0
        done = False
        # Execute action in the game
        self.game.execute_action(action)
        # Compute reward based on game outcome
        if self.game.has_won():
            reward = 1
            done = True
        elif self.game.has_lost():
            reward = -1
            done = True
        # Get next state and available actions
        next_state = self.game.result(self.state, action)
        available_actions = self.game.actions(next_state)
        return next_state, reward, done, {'available_actions': available_actions}

class QLearningAgent:
    def __init__(self, observation_space, action_space):
        self.observation_space = observation_space
        self.action_space = action_space
        self.q_table = np.zeros((self.observation_space.shape[0], self.action_space.n))  # Adjust Q-table size accordingly

    def choose_action(self, state, available_actions, epsilon=0.1):
        print(state)
        state_index = hash(state)  # Convert state to integer index (adjust as needed)
        if np.random.uniform(0, 1) < epsilon:
            return self.action_space.sample()  # Explore: choose a random action
        else:
            # Exploit: choose the action with highest Q-value among available actions
            available_actions_mask = np.zeros_like(self.q_table[state_index], dtype=bool)
            available_actions_mask[available_actions] = True
            q_values_masked = np.where(available_actions_mask, self.q_table[state_index], -np.inf)
            return np.argmax(q_values_masked)

    def update_q_table(self, state, action, reward, next_state, alpha=0.1, gamma=0.9):
        # Update Q-value based on the Q-learning formula
        self.q_table[state, action] += alpha * (reward + gamma * np.max(self.q_table[next_state]) - self.q_table[state, action])

env = SHOBUEnv()

# Wrap the environment to enable visualization (optional)
# env = gym.wrappers.Monitor(env, './videos', force=True)

agent = QLearningAgent(env.observation_space, env.action_space)

num_episodes = 1000

for episode in range(num_episodes):
    state = env.reset()
    done = False

    while not done:
        available_actions = env.game.actions(state)
        action = agent.choose_action(state, available_actions)
        next_state, reward, done, step_info = env.step(action)
        agent.update_q_table(state, action, reward, next_state)
        state = next_state
