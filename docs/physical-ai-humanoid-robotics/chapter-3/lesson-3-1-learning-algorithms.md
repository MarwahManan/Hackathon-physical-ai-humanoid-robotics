---
title: Learning Algorithms
sidebar_label: "Lesson 3.1: Learning Algorithms"
sidebar_position: 1
description: Machine learning techniques for humanoid robot skill acquisition and adaptation
keywords: [robot-learning, reinforcement-learning, imitation-learning, robot-adaptation]
---

# Learning Algorithms

## Introduction

This lesson explores machine learning algorithms that enable humanoid robots to acquire new skills, adapt to environments, and improve performance over time. Learning algorithms are crucial for creating robots that can operate effectively in unstructured environments.

### Learning Objectives

- Understand different types of robot learning algorithms
- Learn about reinforcement learning for robotics
- Explore imitation learning and skill transfer
- Know how to implement basic learning algorithms

### Prerequisites

- Understanding of control systems (from Chapter 2)
- Basic knowledge of machine learning concepts

### Estimated Time

55 minutes

## Core Concepts

Learning algorithms enable humanoid robots to improve their performance through experience. These algorithms allow robots to adapt to new situations, learn from demonstrations, and optimize their behavior based on feedback.

![Learning Algorithm](/img/learning-algorithm.svg)

### Types of Robot Learning

#### Reinforcement Learning (RL)
- **Model-Free RL**: Learn policies directly from interaction
- **Model-Based RL**: Learn environment dynamics first
- **Deep RL**: Combine neural networks with RL algorithms

#### Imitation Learning
- **Behavioral Cloning**: Learn from expert demonstrations
- **Inverse Reinforcement Learning**: Infer reward functions
- **Generative Adversarial Imitation Learning (GAIL)**: Adversarial approach

#### Self-Supervised Learning
- **Autoencoders**: Learn representations from sensor data
- **Predictive models**: Forecast future states
- **Contrastive learning**: Learn representations via comparison

### Learning Challenges in Robotics

Robot learning faces unique challenges:
- **Real-world safety**: Learning must not damage the robot
- **Sample efficiency**: Limited time for real-world interaction
- **Transfer**: Skills learned in simulation to real robots
- **Multi-task learning**: Learning multiple skills simultaneously

## Code Implementation

```python
# Example code demonstrating learning algorithms for humanoid robots
import numpy as np
import random
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim

class ExperienceReplay:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """Add experience to the buffer"""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """Sample a batch of experiences"""
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = map(np.stack, zip(*batch))
        return state, action, reward, next_state, done

    def __len__(self):
        return len(self.buffer)

class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(QNetwork, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def forward(self, state):
        return self.network(state)

class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        # Neural networks
        self.q_network = QNetwork(state_dim, action_dim)
        self.target_network = QNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)

        # Experience replay
        self.memory = ExperienceReplay()

    def act(self, state):
        """Select action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)

        state = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.q_network(state)
        return q_values.max(1)[1].item()

    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.push(state, action, reward, next_state, done)

    def replay(self, batch_size=32):
        """Train the network on a batch of experiences"""
        if len(self.memory) < batch_size:
            return

        state, action, reward, next_state, done = self.memory.sample(batch_size)

        state = torch.FloatTensor(state)
        action = torch.LongTensor(action)
        reward = torch.FloatTensor(reward)
        next_state = torch.FloatTensor(next_state)
        done = torch.BoolTensor(done)

        current_q_values = self.q_network(state).gather(1, action.unsqueeze(1))
        next_q_values = self.target_network(next_state).max(1)[0].detach()
        target_q_values = reward + (self.gamma * next_q_values * ~done)

        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_network(self):
        """Update target network with current network weights"""
        self.target_network.load_state_dict(self.q_network.state_dict())

class ImitationLearningAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3):
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Network for behavioral cloning
        self.network = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
            nn.Tanh()  # Output actions in [-1, 1]
        )

        self.optimizer = optim.Adam(self.network.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

        # Store expert demonstrations
        self.expert_states = []
        self.expert_actions = []

    def add_demonstration(self, state, action):
        """Add expert demonstration to the dataset"""
        self.expert_states.append(state)
        self.expert_actions.append(action)

    def train_behavioral_cloning(self, epochs=100):
        """Train the network using behavioral cloning"""
        if len(self.expert_states) == 0:
            return

        states = torch.FloatTensor(self.expert_states)
        actions = torch.FloatTensor(self.expert_actions)

        for epoch in range(epochs):
            self.optimizer.zero_grad()
            predicted_actions = self.network(states)
            loss = self.criterion(predicted_actions, actions)
            loss.backward()
            self.optimizer.step()

            if epoch % 50 == 0:
                print(f"BC Epoch {epoch}, Loss: {loss.item():.4f}")

    def predict_action(self, state):
        """Predict action for a given state"""
        state = torch.FloatTensor(state).unsqueeze(0)
        action = self.network(state)
        return action.squeeze(0).detach().numpy()

class PolicyGradientAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3):
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Policy network (outputs action probabilities)
        self.policy_network = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
            nn.Softmax(dim=-1)
        )

        self.optimizer = optim.Adam(self.policy_network.parameters(), lr=lr)

    def select_action(self, state):
        """Select action based on current policy"""
        state = torch.FloatTensor(state).unsqueeze(0)
        action_probs = self.policy_network(state).squeeze(0)
        action = torch.multinomial(action_probs, 1).item()
        return action, action_probs[action].item()

    def update_policy(self, log_probs, rewards, gamma=0.99):
        """Update policy using policy gradient"""
        # Calculate discounted rewards
        discounted_rewards = []
        R = 0
        for r in rewards[::-1]:
            R = r + gamma * R
            discounted_rewards.insert(0, R)

        # Normalize rewards
        discounted_rewards = torch.FloatTensor(discounted_rewards)
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9)

        # Calculate loss
        policy_loss = []
        for log_prob, reward in zip(log_probs, discounted_rewards):
            policy_loss.append(-log_prob * reward)

        policy_loss = torch.cat(policy_loss).sum()

        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

class RobotEnvironment:
    def __init__(self):
        # Simplified humanoid environment
        self.state_dim = 12  # 6 joint angles + 6 joint velocities
        self.action_dim = 6  # 6 joint torques

        # Initialize robot state
        self.state = np.random.uniform(-0.1, 0.1, size=self.state_dim)
        self.target_position = np.array([1.0, 0.0, 0.8])  # Target position (x, y, z)
        self.max_steps = 100
        self.current_step = 0

    def reset(self):
        """Reset environment to initial state"""
        self.state = np.random.uniform(-0.1, 0.1, size=self.state_dim)
        self.current_step = 0
        return self.state

    def step(self, action):
        """Execute action and return new state, reward, done"""
        # Apply action to the robot (simplified dynamics)
        action = np.clip(action, -1, 1)  # Clip action to reasonable range

        # Update state (simplified integration)
        self.state[:6] += self.state[6:] * 0.01  # Update positions based on velocities
        self.state[6:] += action * 0.01  # Update velocities based on torques

        # Calculate reward (distance to target + stability)
        current_pos = self.state[:3]  # First 3 elements are position
        distance_to_target = np.linalg.norm(current_pos - self.target_position)

        # Reward for getting closer to target
        reward = -distance_to_target

        # Additional reward for maintaining balance (z > 0.5)
        if self.state[2] > 0.5:
            reward += 0.1

        # Penalty for joint limits
        joint_limit_penalty = np.sum(np.abs(self.state[:6]) > 1.5) * -0.5
        reward += joint_limit_penalty

        self.current_step += 1
        done = self.current_step >= self.max_steps

        return self.state.copy(), reward, done

    def get_state(self):
        """Get current state of the environment"""
        return self.state

# Example usage
if __name__ == "__main__":
    # Create environment
    env = RobotEnvironment()

    # Initialize DQN agent
    dqn_agent = DQNAgent(env.state_dim, env.action_dim)

    print("Starting DQN training...")

    # Training parameters
    num_episodes = 500
    target_update_freq = 10

    # Training loop
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            # Select action
            action = dqn_agent.act(state)

            # Execute action
            next_state, reward, done = env.step(np.random.randn(env.action_dim) * 0.1)  # Random action for demo

            # Store experience
            dqn_agent.remember(state, action, reward, next_state, done)

            # Update state
            state = next_state
            total_reward += reward

        # Train on experiences
        dqn_agent.replay()

        # Update target network periodically
        if episode % target_update_freq == 0:
            dqn_agent.update_target_network()

        # Print progress
        if episode % 50 == 0:
            print(f"Episode {episode}, Total Reward: {total_reward:.2f}, Epsilon: {dqn_agent.epsilon:.3f}")

    print("Training completed!")

    # Example of imitation learning
    print("\nSetting up imitation learning...")

    # Create some expert demonstrations (simplified)
    imitation_agent = ImitationLearningAgent(env.state_dim, env.action_dim)

    # Add some random demonstrations
    for _ in range(100):
        state = np.random.uniform(-0.5, 0.5, size=env.state_dim)
        action = np.random.uniform(-1, 1, size=env.action_dim)
        imitation_agent.add_demonstration(state, action)

    print(f"Added {len(imitation_agent.expert_states)} demonstrations")

    # Train the imitation learning agent
    imitation_agent.train_behavioral_cloning(epochs=200)

    # Test the trained agent
    test_state = np.random.uniform(-0.1, 0.1, size=env.state_dim)
    predicted_action = imitation_agent.predict_action(test_state)
    print(f"Test state: {test_state[:3]}..., Predicted action: {predicted_action[:3]}...")