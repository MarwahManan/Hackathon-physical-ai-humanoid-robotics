---
title: Simulation Environments
sidebar_label: "Lesson 1.3: Simulation Environments"
sidebar_position: 3
description: Introduction to robotics simulation environments for safe experimentation with humanoid robots
keywords: [robotics-simulation, gazebo, pybullet, webots, robot-simulation]
---

# Simulation Environments

## Introduction

This lesson introduces robotics simulation environments that provide safe and cost-effective platforms for experimenting with humanoid robots. Simulation environments allow developers to test algorithms, validate designs, and train robots without the risks and costs associated with physical hardware.

### Learning Objectives

- Understand the importance of simulation in robotics development
- Learn about popular simulation platforms for humanoid robots
- Explore how to set up and use simulation environments
- Recognize the benefits and limitations of simulation

### Prerequisites

- Understanding of Physical AI concepts (from Lesson 1.1)
- Basic understanding of humanoid robot components (from Lesson 1.2)

### Estimated Time

40 minutes

## Core Concepts

Simulation environments are essential tools in robotics development that provide virtual worlds where robots can be tested, trained, and validated before deployment on physical hardware. These environments offer numerous advantages for both research and education.

![Simulation Environment](/img/simulation-environment.svg)

### Why Simulation is Important

Robotics simulation serves several critical purposes:

1. **Safety**: Test dangerous or experimental behaviors without risk to hardware or humans
2. **Cost-Effectiveness**: Reduce expenses associated with physical prototypes and repairs
3. **Repeatability**: Create consistent test conditions for algorithm validation
4. **Speed**: Run experiments faster than real-time to accelerate development
5. **Accessibility**: Enable development without expensive physical hardware

### Popular Simulation Platforms

#### Gazebo
Gazebo is one of the most widely used robotics simulators, particularly in the ROS ecosystem. It provides high-fidelity physics simulation and realistic sensor models.

Features:
- Realistic physics engine (ODE, Bullet, Simbody)
- Wide range of sensor models (cameras, LIDAR, IMU)
- Plugin system for custom sensors and controllers
- Integration with ROS/ROS2

#### PyBullet
PyBullet is a Python-based physics engine that's particularly popular for research and machine learning applications.

Features:
- Fast physics simulation with multiple engines
- Built-in collision detection
- Support for reinforcement learning
- Easy Python integration

#### Webots
Webots is a general-purpose robot simulator that's particularly well-suited for education and research.

Features:
- Built-in robot models and environments
- Multiple programming interfaces (C, Python, Java, etc.)
- Web-based interface capabilities
- Support for various robot types

### Simulation vs. Reality Gap

While simulation environments are powerful tools, they have inherent limitations:

- **Physics Approximation**: Simulated physics may not perfectly match real-world behavior
- **Sensor Noise**: Real sensors have noise and imperfections that may not be fully modeled
- **Environmental Factors**: Real-world conditions like lighting, surfaces, and dynamics vary
- **Latency**: Real systems have communication and processing delays

## Code Implementation

```python
# Example code demonstrating how to work with simulation environments
import pybullet
import pybullet_data
import time
import numpy as np

class SimulationEnvironment:
    def __init__(self, use_gui=True):
        # Connect to physics server
        if use_gui:
            self.client = pybullet.connect(pybullet.GUI)
        else:
            self.client = pybullet.connect(pybullet.DIRECT)

        # Set gravity
        pybullet.setGravity(0, 0, -9.81)

        # Load plane
        pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.plane_id = pybullet.loadURDF("plane.urdf")

        # Store robot information
        self.robot_id = None
        self.joint_indices = []

    def load_robot(self, urdf_path):
        """Load a robot from URDF file"""
        self.robot_id = pybullet.loadURDF(
            urdf_path,
            basePosition=[0, 0, 1],  # Start 1m above ground
            useFixedBase=False
        )

        # Get joint information
        num_joints = pybullet.getNumJoints(self.robot_id)
        for i in range(num_joints):
            joint_info = pybullet.getJointInfo(self.robot_id, i)
            joint_type = joint_info[2]
            if joint_type == pybullet.JOINT_REVOLUTE or joint_type == pybullet.JOINT_PRISMATIC:
                self.joint_indices.append(i)

        print(f"Loaded robot with {num_joints} joints")
        return self.robot_id

    def get_robot_state(self):
        """Get current state of the robot"""
        if self.robot_id is None:
            return None

        # Get base position and orientation
        pos, orn = pybullet.getBasePositionAndOrientation(self.robot_id)

        # Get joint states
        joint_states = pybullet.getJointStates(self.robot_id, self.joint_indices)
        joint_positions = [state[0] for state in joint_states]
        joint_velocities = [state[1] for state in joint_states]

        return {
            'position': pos,
            'orientation': orn,
            'joint_positions': joint_positions,
            'joint_velocities': joint_velocities
        }

    def set_joint_commands(self, joint_commands):
        """Send commands to robot joints"""
        if self.robot_id is None:
            return

        # Apply joint forces/torques
        pybullet.setJointMotorControlArray(
            self.robot_id,
            self.joint_indices,
            pybullet.POSITION_CONTROL,
            targetPositions=joint_commands
        )

    def step_simulation(self):
        """Step the simulation forward"""
        pybullet.stepSimulation()
        time.sleep(1./240.)  # Real-time factor for 240 Hz simulation

    def reset_simulation(self):
        """Reset the simulation"""
        pybullet.resetSimulation()
        pybullet.setGravity(0, 0, -9.81)
        pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.plane_id = pybullet.loadURDF("plane.urdf")
        self.robot_id = None
        self.joint_indices = []

    def disconnect(self):
        """Disconnect from the physics server"""
        pybullet.disconnect(self.client)

class SimpleController:
    def __init__(self, robot_id, joint_indices):
        self.robot_id = robot_id
        self.joint_indices = joint_indices

    def balance_control(self, current_state):
        """Simple balance control for humanoid robot"""
        # Get center of mass information
        com_pos = pybullet.getBasePositionAndOrientation(self.robot_id)[0]

        # Simple proportional control to maintain upright position
        target_angles = []
        for i, joint_idx in enumerate(self.joint_indices):
            # Simple balance control based on robot tilt
            current_pos, current_orn = pybullet.getBasePositionAndOrientation(self.robot_id)

            # Calculate desired joint position based on balance
            # This is a simplified example - real controllers are more complex
            target_angle = 0.0  # Default to neutral position
            target_angles.append(target_angle)

        return target_angles

# Example usage
if __name__ == "__main__":
    # Create simulation environment
    sim = SimulationEnvironment(use_gui=True)

    # Load a simple robot (using a basic model for demonstration)
    # In practice, you would load a humanoid robot URDF
    try:
        # For demonstration, we'll use a simple model
        # In real applications, you would load a humanoid robot model
        sim.load_robot("r2d2.urdf")  # Using a simple model for this example

        # Create a simple controller
        controller = SimpleController(sim.robot_id, sim.joint_indices)

        # Run simulation loop
        print("Starting simulation loop. Press Ctrl+C to stop.")
        for step in range(1000):  # Run for 1000 steps
            # Get current state
            state = sim.get_robot_state()

            # Calculate control commands (simplified)
            commands = [0.0] * len(sim.joint_indices)  # Hold neutral position

            # Send commands to robot
            sim.set_joint_commands(commands)

            # Step simulation
            sim.step_simulation()

            # Print position occasionally
            if step % 100 == 0:
                print(f"Step {step}, Robot position: {state['position']}")

    except Exception as e:
        print(f"Simulation error: {e}")

    finally:
        # Clean up
        sim.disconnect()
```

## Hands-On Exercise

Create a simple simulation environment that loads a robot and implements basic movement.

1. Create a new Python file called `simple_simulation.py`
2. Implement a `RobotSimulation` class that connects to a physics engine
3. Add methods to load a robot, get its state, and send movement commands
4. Create a simple controller that moves the robot in a pattern

**Expected outcome:** Your program should create a simulation environment, load a robot, and make it move in a simple pattern.

**Verification steps:**
- Run your code and verify the simulation starts without errors
- Check that the robot loads correctly in the simulation
- Verify that movement commands are processed properly
- Test that the simulation can be properly shut down

## Summary

In this lesson, you learned about simulation environments for robotics, including popular platforms like Gazebo, PyBullet, and Webots. You now understand the importance of simulation in robotics development and how to implement basic simulation functionality.

### Key Takeaways

- Simulation environments provide safe and cost-effective platforms for robotics development
- Popular platforms include Gazebo, PyBullet, and Webots with different strengths
- Simulation helps with testing, validation, and training without physical hardware
- There are important considerations regarding the simulation-to-reality gap

### Next Steps

Continue to the next chapter to learn about perception systems in humanoid robots.