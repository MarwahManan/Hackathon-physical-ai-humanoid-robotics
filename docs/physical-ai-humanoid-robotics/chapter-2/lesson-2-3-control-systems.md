---
title: Control Systems
sidebar_label: "Lesson 2.3: Control Systems"
sidebar_position: 3
description: Understanding feedback control and motor control systems for humanoid robots
keywords: [robotics-control, feedback-control, motor-control, PID-control]
---

# Control Systems

## Introduction

This lesson explores control systems that enable humanoid robots to execute planned motions with precision and stability. Control systems are essential for translating high-level plans into actual physical movements while maintaining balance and responding to disturbances.

### Learning Objectives

- Understand feedback control principles for robotics
- Learn about PID controllers and their applications
- Explore advanced control techniques for humanoid robots
- Know how to implement basic control algorithms

### Prerequisites

- Understanding of motion planning (from Lesson 2.2)
- Basic knowledge of calculus and differential equations

### Estimated Time

45 minutes

## Core Concepts

Control systems in humanoid robots ensure that the robot follows desired trajectories while maintaining stability. These systems operate at multiple levels, from low-level motor control to high-level balance control.

![Control System](/img/control-system.svg)

### Feedback Control Loop

The fundamental feedback control loop consists of:
1. **Reference Input**: Desired behavior or trajectory
2. **Controller**: Computes control actions based on error
3. **Plant**: The physical system being controlled (robot)
4. **Sensor**: Measures actual system state
5. **Feedback**: Error signal used to adjust control actions

### Types of Control Systems

#### Low-Level Motor Control
- **PID Controllers**: Proportional-Integral-Derivative control
- **Current Control**: Controls motor current for precise torque
- **Position Control**: Maintains desired joint positions

#### High-Level Control
- **Balance Control**: Maintains center of mass within support polygon
- **Impedance Control**: Controls robot's mechanical impedance
- **Admittance Control**: Controls robot's response to external forces

### Control Challenges in Humanoid Robots

Humanoid robots face unique control challenges:
- **Underactuation**: Fewer actuators than degrees of freedom
- **Dynamic balance**: Maintaining stability during motion
- **Contact transitions**: Managing foot-ground contact changes
- **Disturbance rejection**: Responding to external forces

## Code Implementation

```python
# Example code demonstrating control systems for humanoid robots
import numpy as np
import time
import math

class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, output_limits=(-np.inf, np.inf)):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Min and max output values

        self.reset()

    def reset(self):
        """Reset the PID controller"""
        self.previous_error = 0.0
        self.integral = 0.0
        self.previous_time = time.time()

    def update(self, setpoint, measured_value):
        """Update the PID controller with new measurements"""
        current_time = time.time()
        dt = current_time - self.previous_time

        if dt <= 0:
            dt = 1e-6  # Avoid division by zero

        # Calculate error
        error = setpoint - measured_value

        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral += error * dt
        integral = self.ki * self.integral

        # Derivative term
        derivative = self.kd * (error - self.previous_error) / dt

        # Calculate output
        output = proportional + integral + derivative

        # Apply output limits
        output = np.clip(output, self.output_limits[0], self.output_limits[1])

        # Store values for next iteration
        self.previous_error = error
        self.previous_time = current_time

        return output

class JointController:
    def __init__(self, joint_name, kp=10.0, ki=0.1, kd=1.0):
        self.joint_name = joint_name
        self.position_controller = PIDController(kp, ki, kd)
        self.velocity_controller = PIDController(kp/10, ki/10, kd/10)

        self.target_position = 0.0
        self.target_velocity = 0.0
        self.current_position = 0.0
        self.current_velocity = 0.0

    def set_target(self, position, velocity=0.0):
        """Set the target position and velocity for the joint"""
        self.target_position = position
        self.target_velocity = velocity

    def update(self, current_position, current_velocity):
        """Update the joint controller with current state"""
        # Update position controller
        position_error = self.target_position - current_position
        position_correction = self.position_controller.update(
            self.target_position, current_position
        )

        # Update velocity controller
        velocity_correction = self.velocity_controller.update(
            self.target_velocity, current_velocity
        )

        # Combine corrections
        total_correction = position_correction + velocity_correction

        # Store current values
        self.current_position = current_position
        self.current_velocity = current_velocity

        return total_correction

class BalanceController:
    def __init__(self, robot_mass=50.0, gravity=9.81):
        self.robot_mass = robot_mass
        self.gravity = gravity

        # Zero Moment Point (ZMP) controller
        self.zmp_controller = PIDController(kp=100.0, ki=10.0, kd=5.0)

        # Center of Mass (CoM) controller
        self.com_controller = PIDController(kp=50.0, ki=5.0, kd=2.0)

        # Current state
        self.current_com = np.array([0.0, 0.0, 1.0])  # x, y, z
        self.current_com_velocity = np.array([0.0, 0.0, 0.0])
        self.current_com_acceleration = np.array([0.0, 0.0, 0.0])

        # Support polygon (simplified as a rectangle)
        self.support_polygon = {
            'min_x': -0.1, 'max_x': 0.1,
            'min_y': -0.05, 'max_y': 0.05
        }

    def update_com_state(self, com_position, com_velocity, com_acceleration):
        """Update the current Center of Mass state"""
        self.current_com = np.array(com_position)
        self.current_com_velocity = np.array(com_velocity)
        self.current_com_acceleration = np.array(com_acceleration)

    def calculate_zmp(self):
        """Calculate Zero Moment Point from CoM state"""
        # ZMP calculation: ZMP = CoM - (CoM_height / gravity) * CoM_acceleration
        zmp_x = self.current_com[0] - (self.current_com[2] / self.gravity) * self.current_com_acceleration[0]
        zmp_y = self.current_com[1] - (self.current_com[2] / self.gravity) * self.current_com_acceleration[1]

        return np.array([zmp_x, zmp_y])

    def is_balanced(self):
        """Check if the robot is balanced based on ZMP"""
        zmp = self.calculate_zmp()

        return (self.support_polygon['min_x'] <= zmp[0] <= self.support_polygon['max_x'] and
                self.support_polygon['min_y'] <= zmp[1] <= self.support_polygon['max_y'])

    def compute_balance_correction(self, target_com_position):
        """Compute balance correction torques"""
        # Calculate error in CoM position
        com_error = np.array(target_com_position) - self.current_com

        # Use PID controller to compute correction
        correction_x = self.com_controller.update(target_com_position[0], self.current_com[0])
        correction_y = self.com_controller.update(target_com_position[1], self.current_com[1])

        # Calculate ZMP error
        current_zmp = self.calculate_zmp()
        target_zmp = np.array([0.0, 0.0])  # Target ZMP at origin
        zmp_error = target_zmp - current_zmp

        # Apply ZMP correction
        zmp_correction_x = self.zmp_controller.update(target_zmp[0], current_zmp[0])
        zmp_correction_y = self.zmp_controller.update(target_zmp[1], current_zmp[1])

        # Combine corrections
        total_correction = np.array([
            correction_x + zmp_correction_x,
            correction_y + zmp_correction_y,
            0.0  # No correction for z-axis
        ])

        return total_correction

class WholeBodyController:
    def __init__(self, robot_model):
        self.robot = robot_model

        # Initialize joint controllers for each joint
        self.joint_controllers = {}
        for joint_name in self.robot.joint_names:
            self.joint_controllers[joint_name] = JointController(joint_name)

        # Initialize balance controller
        self.balance_controller = BalanceController(robot_model.mass)

        # Trajectory tracking controller
        self.trajectory_controller = PIDController(kp=1.0, ki=0.01, kd=0.1)

    def set_joint_targets(self, target_positions, target_velocities=None):
        """Set target positions for all joints"""
        if target_velocities is None:
            target_velocities = {name: 0.0 for name in target_positions.keys()}

        for joint_name, position in target_positions.items():
            velocity = target_velocities.get(joint_name, 0.0)
            self.joint_controllers[joint_name].set_target(position, velocity)

    def update_balance(self, target_com_position):
        """Update balance control"""
        # Get current CoM state from robot
        current_com = self.robot.get_com_position()
        current_com_vel = self.robot.get_com_velocity()
        current_com_acc = self.robot.get_com_acceleration()

        # Update balance controller with current state
        self.balance_controller.update_com_state(
            current_com, current_com_vel, current_com_acc
        )

        # Compute balance correction
        balance_correction = self.balance_controller.compute_balance_correction(target_com_position)

        # Apply balance correction to joints
        self.apply_balance_correction(balance_correction)

    def apply_balance_correction(self, correction):
        """Apply balance correction to joint controllers"""
        # Distribute balance correction to relevant joints
        # This is a simplified approach - in reality, this would involve
        # more complex whole-body control algorithms
        for joint_name, controller in self.joint_controllers.items():
            if 'hip' in joint_name or 'ankle' in joint_name:
                # Apply more correction to joints that affect balance
                controller.position_controller.kp += correction[0] * 0.1
            elif 'shoulder' in joint_name or 'elbow' in joint_name:
                # Apply less correction to upper body joints
                controller.position_controller.kp += correction[1] * 0.05

    def update(self, current_joint_positions, current_joint_velocities):
        """Update all controllers with current robot state"""
        # Update joint controllers
        control_commands = {}
        for joint_name, position in current_joint_positions.items():
            velocity = current_joint_velocities.get(joint_name, 0.0)
            control_output = self.joint_controllers[joint_name].update(position, velocity)
            control_commands[joint_name] = control_output

        # Update balance controller
        target_com = [0.0, 0.0, 1.0]  # Target CoM position
        self.update_balance(target_com)

        # Check if robot is balanced
        is_balanced = self.balance_controller.is_balanced()

        return control_commands, is_balanced

class SimpleRobotModel:
    def __init__(self):
        self.joint_names = ['left_hip', 'right_hip', 'left_knee', 'right_knee',
                           'left_ankle', 'right_ankle', 'left_shoulder', 'right_shoulder',
                           'left_elbow', 'right_elbow', 'neck', 'waist']
        self.mass = 50.0  # kg

        # Initialize joint positions
        self.joint_positions = {name: 0.0 for name in self.joint_names}
        self.joint_velocities = {name: 0.0 for name in self.joint_names}

        # Initialize CoM
        self.com_position = np.array([0.0, 0.0, 1.0])
        self.com_velocity = np.array([0.0, 0.0, 0.0])
        self.com_acceleration = np.array([0.0, 0.0, 0.0])

    def get_com_position(self):
        """Get current Center of Mass position"""
        return self.com_position

    def get_com_velocity(self):
        """Get current Center of Mass velocity"""
        return self.com_velocity

    def get_com_acceleration(self):
        """Get current Center of Mass acceleration"""
        return self.com_acceleration

    def update_state(self, control_commands, dt=0.01):
        """Update robot state based on control commands"""
        # Apply control commands to joints
        for joint_name, command in control_commands.items():
            if joint_name in self.joint_positions:
                # Simple integration to update position
                self.joint_velocities[joint_name] += command * dt
                self.joint_positions[joint_name] += self.joint_velocities[joint_name] * dt

        # Update CoM based on simplified dynamics
        external_force = np.array([0.0, 0.0, 0.0])  # External forces
        self.com_acceleration = external_force / self.mass
        self.com_velocity += self.com_acceleration * dt
        self.com_position += self.com_velocity * dt

# Example usage
if __name__ == "__main__":
    # Create robot model
    robot = SimpleRobotModel()

    # Create whole body controller
    controller = WholeBodyController(robot)

    # Define target joint positions (simple pose)
    target_positions = {
        'left_hip': 0.1, 'right_hip': 0.1,
        'left_knee': -0.2, 'right_knee': -0.2,
        'left_ankle': 0.1, 'right_ankle': 0.1
    }

    print("Starting control simulation...")
    print("Target joint positions:", target_positions)

    # Simulation parameters
    dt = 0.01  # 100 Hz control loop
    simulation_time = 2.0  # 2 seconds
    steps = int(simulation_time / dt)

    for step in range(steps):
        # Set targets
        controller.set_joint_targets(target_positions)

        # Update controller with current state
        control_commands, is_balanced = controller.update(
            robot.joint_positions,
            robot.joint_velocities
        )

        # Update robot state
        robot.update_state(control_commands, dt)

        # Print status every 100 steps (1 second)
        if step % 100 == 0:
            print(f"Step {step}: Balanced = {is_balanced}, CoM = {robot.get_com_position()}")

    print("Control simulation completed!")
    print(f"Final CoM position: {robot.get_com_position()}")
    print(f"Final joint positions: {dict(list(robot.joint_positions.items())[:6])}...")  # Show first 6