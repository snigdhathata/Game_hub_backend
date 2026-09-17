import gymnasium as gym
import torch
import torch.nn as nn
import torch.nn.functional as F

# ---------------------------
# Policy Network
# ---------------------------
class PolicyNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 16)
        self.fc2 = nn.Linear(16, 2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

# ---------------------------
# Compute discounted returns
# ---------------------------
def compute_returns(rewards, gamma=0.99):
    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)
    return returns

# ---------------------------
# MAIN FUNCTION (WITH RENDER)
# ---------------------------
def run(episodes=50):
    # 👇 THIS LINE MAKES THE GAME VISIBLE
    env = gym.make("CartPole-v1", render_mode="human")

    policy = PolicyNetwork()
    optimizer = torch.optim.Adam(policy.parameters(), lr=0.01)

    rewards_per_episode = []

    for episode in range(episodes):
        state, _ = env.reset()
        done = False

        log_probs = []
        rewards = []

        while not done:
            state_tensor = torch.tensor([state], dtype=torch.float32)
            probs = policy(state_tensor)

            dist = torch.distributions.Categorical(probs)
            action = dist.sample()

            log_probs.append(dist.log_prob(action))

            state, reward, done, _, _ = env.step(action.item())
            rewards.append(reward)

        returns = compute_returns(rewards)
        returns = torch.tensor(returns, dtype=torch.float32)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)

        loss = 0
        for log_prob, G in zip(log_probs, returns):
            loss += -log_prob * G

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        episode_reward = sum(rewards)
        rewards_per_episode.append(episode_reward)

        print(f"Episode {episode + 1}: Reward = {episode_reward}")

    env.close()

    # 🎯 Return summary (used by backend / frontend)
    return {
        "episodes": episodes,
        "rewards": rewards_per_episode,
        "average_reward": sum(rewards_per_episode) / len(rewards_per_episode),
        "max_reward": max(rewards_per_episode)
    }
