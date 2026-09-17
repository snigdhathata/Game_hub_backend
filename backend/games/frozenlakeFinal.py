import gymnasium as gym
import numpy as np
import time

# ---------------------------
# TRAIN + TEST
# ---------------------------
def train_and_test(
    train_episodes=5000,
    test_episodes=100
):
    env = gym.make("FrozenLake-v1", is_slippery=True)

    state_size = env.observation_space.n
    action_size = env.action_space.n
    q_table = np.zeros((state_size, action_size))

    epsilon = 1.0
    min_epsilon = 0.01
    epsilon_decay = 0.001
    lr = 0.1
    gamma = 0.99

    # ---- TRAIN ----
    for _ in range(train_episodes):
        state, _ = env.reset()
        done = False

        while not done:
            action = (
                env.action_space.sample()
                if np.random.rand() < epsilon
                else np.argmax(q_table[state])
            )

            new_state, reward, done, _, _ = env.step(action)

            q_table[state, action] += lr * (
                reward + gamma * np.max(q_table[new_state]) - q_table[state, action]
            )

            state = new_state

        epsilon = max(min_epsilon, epsilon - epsilon_decay)

    # ---- TEST ----
    success = 0
    for _ in range(test_episodes):
        state, _ = env.reset()
        done = False

        while not done:
            action = np.argmax(q_table[state])
            state, reward, done, _, _ = env.step(action)
            if reward == 1:
                success += 1

    env.close()

    stats = {
        "train_episodes": train_episodes,
        "test_episodes": test_episodes,
        "success_rate": round((success / test_episodes) * 100, 2),
    }

    return q_table, stats


# ---------------------------
# GUI DEMO
# ---------------------------
def run():
    q_table, stats = train_and_test()

    # 👇 GUI DEMO
    env = gym.make("FrozenLake-v1", render_mode="human")
    state, _ = env.reset()
    done = False

    while not done:
        action = np.argmax(q_table[state])
        state, _, done, _, _ = env.step(action)
        time.sleep(0.5)

    env.close()

    return stats
