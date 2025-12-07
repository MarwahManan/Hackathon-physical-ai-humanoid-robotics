---
title: Perception Systems
sidebar_label: "Lesson 2.1: Perception Systems"
sidebar_position: 1
description: Understanding how humanoid robots perceive their environment through sensors and computer vision
keywords: [robotics-perception, computer-vision, sensors, robot-sensing]
---

# Perception Systems

## Introduction

This lesson explores how humanoid robots perceive their environment using various sensors and computer vision techniques. Perception is the first step in the Physical AI loop, enabling robots to understand their surroundings and make informed decisions.

### Learning Objectives

- Understand different types of sensors used in humanoid robots
- Learn about computer vision fundamentals for robotics
- Explore sensor fusion techniques
- Know how to implement basic perception algorithms

### Prerequisites

- Understanding of Physical AI concepts (from Chapter 1)
- Basic knowledge of sensors and data processing

### Estimated Time

45 minutes

## Core Concepts

Perception systems in humanoid robots are responsible for gathering information about the environment and the robot's own state. These systems form the foundation of the perception-action loop that characterizes Physical AI.

![Perception System](/img/perception-system.svg)

### Types of Sensors

Humanoid robots employ various types of sensors to perceive their environment:

#### Vision Sensors
- **Cameras**: RGB, depth, and stereo cameras for visual information
- **Event-based cameras**: Capture changes in brightness with high temporal resolution
- **Infrared sensors**: Detect heat signatures and operate in low-light conditions

#### Proprioceptive Sensors
- **Inertial Measurement Units (IMUs)**: Measure acceleration, angular velocity, and orientation
- **Joint encoders**: Provide information about joint angles and positions
- **Force/torque sensors**: Measure forces and torques at joints and end effectors

#### Exteroceptive Sensors
- **LIDAR**: Provides 3D point cloud data for environment mapping
- **Ultrasonic sensors**: Measure distances using sound waves
- **Tactile sensors**: Detect contact, pressure, and texture

### Computer Vision for Robotics

Computer vision enables robots to interpret visual information from cameras. Key techniques include:

1. **Object Detection**: Identifying and localizing objects in the environment
2. **Pose Estimation**: Determining the position and orientation of objects
3. **Scene Understanding**: Interpreting the spatial relationships between objects
4. **Visual Tracking**: Following objects or features over time

### Sensor Fusion

Sensor fusion combines data from multiple sensors to create a more accurate and robust understanding of the environment. Common approaches include:

- **Kalman Filters**: Optimal estimation for linear systems with Gaussian noise
- **Particle Filters**: Non-parametric approach for non-linear, non-Gaussian systems
- **Bayesian Networks**: Probabilistic models for reasoning under uncertainty

## Code Implementation

```python
# Example code demonstrating sensor fusion for robot perception
import numpy as np
from scipy.spatial.transform import Rotation as R

class PerceptionSystem:
    def __init__(self):
        # Initialize different sensor types
        self.camera = CameraSensor()
        self.imu = IMUSensor()
        self.lidar = LIDARSensor()
        self.fusion_filter = KalmanFilter()

        # State variables for robot pose estimation
        self.position = np.zeros(3)  # x, y, z
        self.orientation = np.array([0, 0, 0, 1])  # quaternion
        self.velocity = np.zeros(3)  # x, y, z velocities

    def process_camera_data(self, image):
        """Process visual data to detect objects and estimate poses"""
        # Detect objects in the image
        objects = self.camera.detect_objects(image)

        # Estimate distances using stereo vision or depth data
        for obj in objects:
            if obj.depth_available:
                obj.distance = obj.depth
            else:
                obj.distance = self.estimate_distance(obj.bounding_box)

        return objects

    def process_imu_data(self, imu_reading):
        """Process IMU data for orientation and acceleration"""
        # Update orientation using gyroscope data
        angular_velocity = np.array(imu_reading['gyroscope'])
        dt = imu_reading['timestamp'] - self.last_imu_time

        # Integrate angular velocity to get orientation change
        orientation_change = self.integrate_angular_velocity(angular_velocity, dt)

        # Update current orientation
        self.orientation = self.quaternion_multiply(
            self.orientation,
            orientation_change
        )

        # Update position using accelerometer data
        acceleration = np.array(imu_reading['accelerometer'])
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        return {
            'position': self.position,
            'orientation': self.orientation,
            'velocity': self.velocity
        }

    def process_lidar_data(self, point_cloud):
        """Process LIDAR data for environment mapping"""
        # Convert point cloud to useful representations
        obstacles = self.extract_obstacles(point_cloud)
        ground_plane = self.fit_ground_plane(point_cloud)

        # Create occupancy grid map
        occupancy_grid = self.create_occupancy_grid(point_cloud)

        return {
            'obstacles': obstacles,
            'ground_plane': ground_plane,
            'occupancy_grid': occupancy_grid
        }

    def sensor_fusion(self, sensor_data):
        """Combine data from multiple sensors using Kalman filtering"""
        # Prediction step: predict state based on motion model
        predicted_state = self.fusion_filter.predict(
            self.position,
            self.orientation,
            self.velocity
        )

        # Update step: incorporate sensor measurements
        for sensor_type, measurement in sensor_data.items():
            predicted_state = self.fusion_filter.update(
                predicted_state,
                sensor_type,
                measurement
            )

        # Update internal state with fused estimate
        self.position = predicted_state['position']
        self.orientation = predicted_state['orientation']
        self.velocity = predicted_state['velocity']

        return predicted_state

class CameraSensor:
    def __init__(self):
        self.resolution = (640, 480)
        self.focal_length = 500  # pixels
        self.intrinsic_matrix = np.array([
            [self.focal_length, 0, self.resolution[0]/2],
            [0, self.focal_length, self.resolution[1]/2],
            [0, 0, 1]
        ])

    def detect_objects(self, image):
        """Detect objects in the image using a simple approach"""
        # This would typically use a deep learning model in practice
        # For this example, we'll simulate object detection
        import random

        objects = []
        for i in range(random.randint(1, 5)):  # Random 1-5 objects
            obj = {
                'id': i,
                'class': random.choice(['person', 'chair', 'table', 'box']),
                'bounding_box': [
                    random.randint(0, self.resolution[0]-50),
                    random.randint(0, self.resolution[1]-50),
                    random.randint(20, 100),  # width
                    random.randint(20, 100)   # height
                ],
                'confidence': random.uniform(0.7, 0.99)
            }
            objects.append(obj)

        return objects

class IMUSensor:
    def __init__(self):
        self.bias = np.zeros(6)  # 3 for accelerometer, 3 for gyroscope

    def read(self):
        """Simulate IMU reading"""
        # Simulate realistic IMU data with noise
        import random

        return {
            'accelerometer': [
                random.gauss(0, 0.01),  # x
                random.gauss(0, 0.01),  # y
                random.gauss(9.81, 0.01)  # z (gravity)
            ],
            'gyroscope': [
                random.gauss(0, 0.001),  # x
                random.gauss(0, 0.001),  # y
                random.gauss(0, 0.001)   # z
            ],
            'timestamp': 0.0  # This would be actual time
        }

class LIDARSensor:
    def __init__(self):
        self.fov_horizontal = 360  # degrees
        self.fov_vertical = 30     # degrees
        self.max_range = 20.0      # meters

    def scan(self):
        """Simulate LIDAR scan"""
        # Generate a simple point cloud
        points = []
        for angle in range(0, 360, 5):  # 5-degree increments
            for elev in range(-15, 15, 5):  # elevation angles
                # Simulate distance measurement with some obstacles
                distance = self.max_range
                if random.random() < 0.3:  # 30% chance of obstacle
                    distance = random.uniform(0.5, 10.0)

                # Convert polar to Cartesian coordinates
                angle_rad = np.radians(angle)
                elev_rad = np.radians(elev)

                x = distance * np.cos(elev_rad) * np.cos(angle_rad)
                y = distance * np.cos(elev_rad) * np.sin(angle_rad)
                z = distance * np.sin(elev_rad)

                points.append([x, y, z])

        return np.array(points)

class KalmanFilter:
    def __init__(self):
        # Initialize state covariance matrix
        self.P = np.eye(13) * 0.1  # 13 state variables: pos(3), orient(4), vel(3), bias(3)
        self.Q = np.eye(13) * 0.01  # Process noise
        self.R = np.eye(6) * 0.1    # Measurement noise (for IMU)

    def predict(self, position, orientation, velocity):
        """Predict next state based on motion model"""
        # Simplified motion model - in practice this would be more complex
        dt = 0.01  # time step

        # Predict position based on velocity
        predicted_pos = position + velocity * dt

        # For orientation, we'll assume minimal change for simplicity
        predicted_orient = orientation

        return {
            'position': predicted_pos,
            'orientation': predicted_orient,
            'velocity': velocity  # Assume constant velocity
        }

    def update(self, predicted_state, sensor_type, measurement):
        """Update state estimate with sensor measurement"""
        # This is a simplified implementation
        # In practice, this would involve full Kalman filter equations

        if sensor_type == 'camera':
            # Use camera data to correct position estimate
            # This is a placeholder for actual sensor fusion logic
            corrected_state = predicted_state.copy()
            # Apply correction based on camera measurements
            return corrected_state
        elif sensor_type == 'imu':
            # Use IMU data to correct orientation and velocity
            corrected_state = predicted_state.copy()
            # Apply correction based on IMU measurements
            return corrected_state
        else:
            return predicted_state

# Example usage
if __name__ == "__main__":
    # Create perception system
    perception = PerceptionSystem()

    # Simulate sensor readings
    camera_image = np.random.rand(480, 640, 3)  # Simulated image
    imu_reading = perception.imu.read()
    lidar_point_cloud = perception.lidar.scan()

    # Process each sensor modality
    camera_objects = perception.process_camera_data(camera_image)
    imu_state = perception.process_imu_data(imu_reading)
    lidar_data = perception.process_lidar_data(lidar_point_cloud)

    # Combine sensor data
    sensor_data = {
        'camera': camera_objects,
        'imu': imu_state,
        'lidar': lidar_data
    }

    fused_state = perception.sensor_fusion(sensor_data)

    print("Perception System Results:")
    print(f"Estimated Position: {fused_state['position']}")
    print(f"Estimated Orientation: {fused_state['orientation']}")
    print(f"Estimated Velocity: {fused_state['velocity']}")
    print(f"Detected Objects: {len(camera_objects)} objects")
    print(f"LIDAR Points: {len(lidar_point_cloud)} points")
```

## Hands-On Exercise

Implement a simple object detection system using multiple sensors.

1. Create a new Python file called `sensor_fusion_exercise.py`
2. Implement a `MultiSensorFusion` class that combines camera and IMU data
3. Add a method to detect when an object is moving toward the robot
4. Implement a simple tracking algorithm that follows an object

**Expected outcome:** Your program should simulate multiple sensors detecting an object and tracking its movement relative to the robot.

**Verification steps:**
- Run your code and verify it doesn't crash
- Check that sensor fusion improves position estimates compared to single sensors
- Verify that the tracking algorithm correctly follows moving objects

## Summary

In this lesson, you learned about perception systems in humanoid robots, including different sensor types, computer vision techniques, and sensor fusion methods. You now understand how robots gather information about their environment and combine multiple sensor modalities for more robust perception.

### Key Takeaways

- Perception systems are crucial for robot-environment interaction
- Multiple sensor types provide complementary information
- Sensor fusion improves accuracy and robustness
- Computer vision enables complex scene understanding

### Next Steps

With perception systems understood, you're ready to move on to motion planning and control systems in the next lesson.