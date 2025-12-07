---
title: Motion Planning
sidebar_label: "Lesson 2.2: Motion Planning"
sidebar_position: 2
description: Algorithms and techniques for planning robot movements in complex environments
keywords: [motion-planning, path-planning, robotics-algorithms, navigation]
---

# Motion Planning

## Introduction

This lesson covers motion planning algorithms that enable humanoid robots to navigate through complex environments while avoiding obstacles. Motion planning is a critical component that bridges perception and action in Physical AI systems.

### Learning Objectives

- Understand fundamental motion planning algorithms
- Learn about configuration space and collision detection
- Explore sampling-based and optimization-based planning
- Know how to implement basic path planning techniques

### Prerequisites

- Understanding of perception systems (from Lesson 2.1)
- Basic knowledge of geometry and coordinate systems

### Estimated Time

50 minutes

## Core Concepts

Motion planning involves finding a valid path from a start configuration to a goal configuration while avoiding obstacles. For humanoid robots, this becomes complex due to their multiple degrees of freedom and balance requirements.

![Motion Planning](/img/motion-planning.svg)

### Configuration Space

The configuration space (C-space) represents all possible configurations of a robot. For a humanoid robot, this includes:

1. **Joint space**: All possible joint angle combinations
2. **Operational space**: End-effector positions and orientations
3. **Task space**: Task-specific coordinate systems

### Path Planning Algorithms

#### Sampling-Based Methods
- **RRT (Rapidly-exploring Random Trees)**: Efficient for high-dimensional spaces
- **PRM (Probabilistic Roadmap)**: Pre-computes roadmap for multiple queries
- **RRT***: Optimal variant of RRT that converges to optimal solution

#### Optimization-Based Methods
- **CHOMP (Covariant Hamiltonian Optimization for Motion Planning)**: Smooths trajectories
- **STOMP (Stochastic Trajectory Optimization)**: Optimizes over entire trajectory
- **TrajOpt**: Trajectory optimization with collision constraints

### Humanoid-Specific Considerations

Humanoid robots have unique challenges in motion planning:
- **Balance maintenance**: Keeping center of mass within support polygon
- **Kinematic constraints**: Joint limits and reachability
- **Dynamic stability**: Maintaining stability during motion execution

## Code Implementation

```python
# Example code demonstrating motion planning for humanoid robots
import numpy as np
from scipy.spatial.distance import euclidean
import random

class MotionPlanner:
    def __init__(self, robot_model):
        self.robot = robot_model
        self.obstacles = []
        self.workspace_bounds = {
            'min': np.array([-5, -5, 0]),
            'max': np.array([5, 5, 2])
        }

    def add_obstacle(self, center, dimensions):
        """Add an obstacle to the environment"""
        obstacle = {
            'center': np.array(center),
            'dimensions': np.array(dimensions)
        }
        self.obstacles.append(obstacle)

    def is_collision_free(self, configuration):
        """Check if a configuration is collision-free"""
        # Transform robot to this configuration
        robot_points = self.robot.get_robot_points(configuration)

        for point in robot_points:
            for obstacle in self.obstacles:
                if self._point_in_obstacle(point, obstacle):
                    return False
        return True

    def _point_in_obstacle(self, point, obstacle):
        """Check if a point is inside an obstacle"""
        half_dims = obstacle['dimensions'] / 2
        diff = np.abs(point - obstacle['center'])

        return np.all(diff <= half_dims)

    def sample_free_space(self):
        """Sample a random configuration in free space"""
        while True:
            # Sample random configuration within bounds
            config = np.random.uniform(
                low=self.workspace_bounds['min'],
                high=self.workspace_bounds['max']
            )

            # For humanoid, also sample joint angles
            joint_angles = np.random.uniform(
                low=self.robot.joint_limits['min'],
                high=self.robot.joint_limits['max'],
                size=len(self.robot.joint_limits['min'])
            )

            full_config = np.concatenate([config, joint_angles])

            if self.is_collision_free(full_config):
                return full_config

    def plan_path_rrt(self, start_config, goal_config, max_iterations=1000):
        """Plan path using RRT algorithm"""
        tree = [start_config]
        parent_map = {0: None}  # Track parent of each node

        for i in range(max_iterations):
            # Sample random configuration with bias toward goal
            if random.random() < 0.1:  # 10% chance to sample goal
                random_config = goal_config
            else:
                random_config = self.sample_free_space()

            # Find nearest node in tree
            nearest_idx = self._find_nearest(tree, random_config)
            nearest_config = tree[nearest_idx]

            # Extend toward random configuration
            new_config = self._extend_toward(nearest_config, random_config)

            if self.is_collision_free(new_config):
                tree.append(new_config)
                new_idx = len(tree) - 1
                parent_map[new_idx] = nearest_idx

                # Check if we're close to goal
                if self._distance(new_config, goal_config) < 0.5:
                    # Connect to goal if possible
                    if self._is_line_collision_free(new_config, goal_config):
                        tree.append(goal_config)
                        goal_idx = len(tree) - 1
                        parent_map[goal_idx] = new_idx
                        return self._extract_path(parent_map, goal_idx, tree)

        return None  # Failed to find path

    def _find_nearest(self, tree, config):
        """Find nearest configuration in tree to given config"""
        distances = [self._distance(node, config) for node in tree]
        return np.argmin(distances)

    def _extend_toward(self, start_config, target_config, step_size=0.1):
        """Extend from start toward target by step size"""
        direction = target_config - start_config
        distance = np.linalg.norm(direction)

        if distance <= step_size:
            return target_config

        normalized_direction = direction / distance
        new_config = start_config + normalized_direction * step_size
        return new_config

    def _distance(self, config1, config2):
        """Calculate distance between two configurations"""
        return np.linalg.norm(config1 - config2)

    def _is_line_collision_free(self, config1, config2, num_samples=10):
        """Check if line between two configs is collision-free"""
        for i in range(num_samples + 1):
            t = i / num_samples
            intermediate_config = (1 - t) * config1 + t * config2

            if not self.is_collision_free(intermediate_config):
                return False
        return True

    def _extract_path(self, parent_map, goal_idx, tree):
        """Extract path from parent map"""
        path = []
        current_idx = goal_idx

        while current_idx is not None:
            path.append(tree[current_idx])
            current_idx = parent_map[current_idx]

        return path[::-1]  # Reverse to get start->goal path

class HumanoidModel:
    def __init__(self):
        # Simplified humanoid model with basic kinematics
        self.num_joints = 12  # Simplified for example
        self.joint_limits = {
            'min': np.full(self.num_joints, -np.pi/2),
            'max': np.full(self.num_joints, np.pi/2)
        }

        # Base position and orientation
        self.base_position = np.zeros(3)
        self.base_orientation = np.array([0, 0, 0, 1])  # quaternion

    def get_robot_points(self, configuration):
        """Get key points of robot in given configuration"""
        # Simplified model - return some key points
        # In reality, this would involve forward kinematics
        base_pos = configuration[:3]  # First 3 elements are base position

        points = [
            base_pos,  # Base
            base_pos + np.array([0, 0, 0.5]),  # Torso
            base_pos + np.array([0, 0, 1.0]),  # Head
            base_pos + np.array([0.3, 0, 0.8]),  # Hand 1
            base_pos + np.array([-0.3, 0, 0.8])  # Hand 2
        ]

        # Add points based on joint angles (simplified)
        joint_angles = configuration[3:3+self.num_joints]
        for i, angle in enumerate(joint_angles[:2]):  # Use first 2 joint angles
            offset = np.array([np.cos(angle) * 0.3, np.sin(angle) * 0.3, 0])
            points.append(base_pos + offset)

        return np.array(points)

    def check_balance(self, configuration):
        """Check if configuration maintains balance"""
        # Simplified balance check
        base_pos = configuration[:3]

        # Check if center of mass is within support polygon
        # This is a very simplified check
        return base_pos[2] > 0.1  # Must be above ground

class PathOptimizer:
    def __init__(self, planner):
        self.planner = planner

    def optimize_path(self, path, max_iterations=50):
        """Optimize path to make it smoother and more efficient"""
        optimized_path = path.copy()

        for iteration in range(max_iterations):
            improved = False

            for i in range(1, len(optimized_path) - 1):
                # Try to shortcut by connecting non-adjacent points
                prev_config = optimized_path[i-1]
                next_config = optimized_path[i+1]

                if self.planner._is_line_collision_free(prev_config, next_config):
                    # Replace current point with direct connection
                    optimized_path.pop(i)
                    improved = True
                    break  # Restart optimization from beginning

            if not improved:
                break

        return optimized_path

# Example usage
if __name__ == "__main__":
    # Create humanoid robot model
    robot = HumanoidModel()

    # Create motion planner
    planner = MotionPlanner(robot)

    # Add some obstacles
    planner.add_obstacle(center=[2, 0, 1], dimensions=[1, 1, 2])
    planner.add_obstacle(center=[0, 2, 1], dimensions=[1, 1, 2])

    # Define start and goal configurations
    start_config = np.array([0, 0, 0.8] + [0] * robot.num_joints)  # Start at origin
    goal_config = np.array([4, 4, 0.8] + [0] * robot.num_joints)   # Goal at [4,4]

    print("Planning path from", start_config[:3], "to", goal_config[:3])

    # Plan path using RRT
    path = planner.plan_path_rrt(start_config, goal_config)

    if path:
        print(f"Path found with {len(path)} waypoints!")

        # Optimize the path
        optimizer = PathOptimizer(planner)
        optimized_path = optimizer.optimize_path(path)
        print(f"Optimized path has {len(optimized_path)} waypoints")

        # Print some waypoints
        print("First few waypoints:")
        for i, waypoint in enumerate(optimized_path[:5]):
            print(f"  Waypoint {i}: pos=({waypoint[0]:.2f}, {waypoint[1]:.2f}, {waypoint[2]:.2f})")

        # Check final path properties
        total_distance = 0
        for i in range(1, len(optimized_path)):
            total_distance += np.linalg.norm(optimized_path[i] - optimized_path[i-1])

        print(f"Total path distance: {total_distance:.2f} meters")
    else:
        print("No path found!")