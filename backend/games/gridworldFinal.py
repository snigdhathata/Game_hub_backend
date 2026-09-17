import numpy as np
import random
import time

# ---------------------------
# GRID WORLD SETUP
# ---------------------------
GRID_SIZE = 4

grid = [
    ["S", ".", ".", "."],
    [".", "H", ".", "H"],
    [".", ".", ".", "."],
    ["H", ".", ".", "G"]
]

actions = {
    0: (-1, 0),  # Up
    1: (1, 0),   # Down
    2: (0, -1),  # Left
    3: (0, 1)    # Right
}

REWARD_GOAL = 10
REWARD_HOLE = -10
REWARD_STEP = -1

# ---------------------------
# HELPERS
# ---------------------------
def reset_agent():
    return [0, 0]

def get_state(pos):
    return pos[0] * GRID_SIZE + pos[1]

def step(pos, action):
    dr, dc = actions[action]
    r, c = pos[0] + dr, pos[1] + dc

    if r < 0 or r >= GRID_SIZE or c < 0 or c >= GRID_SIZE:
        return pos, REWARD_STEP, False

    pos = [r, c]
    cell = grid[r][c]

    if cell == "G":
        return pos, REWARD_GOAL, True
    elif cell == "H":
        return pos, REWARD_HOLE, True
    else:
        return pos, REWARD_STEP, False

def print_grid(pos):
    for r in range(GRID_SIZE):
        row = ""
        for c in range(GRID_SIZE):
            if [r, c] == pos:
                row += "A  "
            else:
                row += grid[r][c] + "  "
        print(row)
    print()

# ---------------------------
# TRAINING (HEADLESS)
# ---------------------------
def train_headless(episodes=500):
    state_size = GRID_SIZE * GRID_SIZE
    action_size = len(actions)
    q_table = np.zeros((state_size, action_size))

    lr = 0.1
    gamma = 0.95
    epsilon = 1.0
    epsilon_decay = 0.01
    min_epsilon = 0.1

    successes = 0

    for _ in range(episodes):
        agent_pos = reset_agent()
        state = get_state(agent_pos)
        done = False

        while not done:
            action = (
                random.choice(list(actions))
                if random.random() < epsilon
                else np.argmax(q_table[state])
            )

            new_pos, reward, done = step(agent_pos, action)
            new_state = get_state(new_pos)

            q_table[state, action] += lr * (
                reward + gamma * np.max(q_table[new_state]) - q_table[state, action]
            )

            agent_pos = new_pos
            state = new_state

            if reward == REWARD_GOAL:
                successes += 1

        epsilon = max(min_epsilon, epsilon - epsilon_decay)

    stats = {
        "episodes": episodes,
        "success_rate": round((successes / episodes) * 100, 2),
        "grid_size": GRID_SIZE
    }

    return q_table, stats

# ---------------------------
# TERMINAL DEMO + RETURN STATS
# ---------------------------
def run():
    q_table, stats = train_headless()

    print("\n🎮 GRID WORLD DEMO\n")
    agent_pos = reset_agent()
    done = False

    while not done:
        print_grid(agent_pos)
        state = get_state(agent_pos)
        action = np.argmax(q_table[state])
        agent_pos, _, done = step(agent_pos, action)
        time.sleep(0.6)

    print_grid(agent_pos)
    print("🎉 Agent reached the goal!")

    return stats
