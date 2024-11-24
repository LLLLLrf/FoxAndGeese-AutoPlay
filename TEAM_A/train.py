import gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
import matplotlib.pyplot as plt
from train_RL.fox_and_geese_env import FoxAndGeeseEnv

# Custom callback for logging rewards
class RewardLogger(BaseCallback):
    def __init__(self, verbose=0):
        super(RewardLogger, self).__init__(verbose)
        self.episode_rewards = []
        self.episode_lengths = []

    def _on_step(self) -> bool:
        if self.locals.get("done", False):  # At the end of each episode
            self.episode_rewards.append(self.locals["infos"][0].get("episode", {}).get("r", 0))
            self.episode_lengths.append(self.locals["infos"][0].get("episode", {}).get("l", 0))
        return True

# Create the environment
env = FoxAndGeeseEnv()

# Initialize PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train with logging
reward_logger = RewardLogger()
model.learn(total_timesteps=10000, callback=reward_logger)

# Save the trained model
model.save("fox_model")

# Evaluate the agent
obs = env.reset()[0]
done = False
total_rewards = 0
steps = 0

while not done:
    action, _ = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)  # Correct unpacking
    total_rewards += reward
    steps += 1
    env.render()

print(f"Evaluation completed in {steps} steps with total reward {total_rewards}")

# Plot training rewards
plt.plot(reward_logger.episode_rewards)
plt.title("Training Rewards")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.show()
