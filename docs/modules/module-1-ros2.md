---
sidebar_position: 2
title: Module 1 - The Robotic Nervous System (ROS 2)
---

# Module 1: The Robotic Nervous System (ROS 2)

## Focus: Middleware for robot control

ROS 2 (Robot Operating System 2) serves as the communication backbone for robotic systems, enabling different components to interact seamlessly. It provides the infrastructure for robot applications through a distributed computing framework, implementing the publish-subscribe and service-request patterns for inter-process communication.

## Architecture and Concepts

### Nodes: The Fundamental Building Blocks

Nodes are independent processes that perform computation and are the basic execution units in ROS 2. In humanoid robotics, nodes typically handle specialized subsystems:

- **Joint Controllers**: Manage individual joint positions, velocities, and efforts
- **Sensor Processing**: Handle IMU, camera, LiDAR, and other sensor data
- **Path Planning**: Compute navigation paths and trajectories
- **Human-Robot Interaction**: Process speech, gestures, and social cues
- **State Estimation**: Track robot pose and state through sensor fusion
- **Motion Planning**: Plan complex multi-limb movements
- **Perception**: Object detection, recognition, and scene understanding

### Topics: Continuous Communication Channels

Topics use a publish-subscribe communication pattern for continuous data streams:

- **Sensor Data Streams**: IMU readings, camera images, LiDAR scans, joint states
- **Actuator Commands**: Joint trajectories, gripper commands, head movements
- **Robot State Information**: Odometry, transforms, battery status
- **Perception Results**: Detected objects, people tracking, SLAM maps
- **System Status**: CPU usage, memory, thermal management

### Services: Discrete Request-Response Interactions

Services provide synchronous request-response communication for discrete interactions:

- **Navigation Requests**: Send goal poses to navigation stack
- **Calibration Commands**: Calibrate sensors and actuators
- **System Status Queries**: Request current system state
- **Map Services**: Load, save, or query map information
- **Action Execution**: Execute predefined behaviors or skills

### Actions: Asynchronous Goal-Oriented Communication

Actions extend services to handle long-running operations with feedback:

- **Navigation Actions**: Move to goal with progress feedback
- **Manipulation Actions**: Grasp and place objects with status updates
- **Calibration Actions**: Perform calibration with progress updates
- **Learning Actions**: Train models with progress feedback

## Advanced ROS 2 Concepts for Humanoid Robotics

### Quality of Service (QoS) Settings

For humanoid robots operating in real-time environments, QoS settings are crucial:

```python
import rclpy
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from sensor_msgs.msg import JointState, Imu
from std_msgs.msg import String

class HumanoidQoSNode(rclpy.node.Node):
    def __init__(self):
        super().__init__('humanoid_qos_node')

        # High-frequency sensor data - reliable, keep last 10
        sensor_qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST
        )

        # Joint state publisher with specific QoS
        self.joint_pub = self.create_publisher(JointState, '/joint_states', sensor_qos)

        # Command topics - best effort for real-time control
        cmd_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST
        )

        self.cmd_pub = self.create_publisher(String, '/robot_commands', cmd_qos)

        # State estimation - reliable with history
        state_qos = QoSProfile(
            depth=100,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_ALL
        )

        self.state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_callback, state_qos)

    def joint_callback(self, msg):
        # Process joint state with appropriate timing
        self.get_logger().debug(f'Received joint state with {len(msg.name)} joints')
```

### Parameter Management for Humanoid Systems

Humanoid robots have many configurable parameters:

```python
class HumanoidParameterNode(rclpy.node.Node):
    def __init__(self):
        super().__init__('humanoid_param_node')

        # Declare parameters with descriptions
        self.declare_parameter('control_loop_rate', 100,
                              'Rate for main control loop (Hz)')
        self.declare_parameter('max_joint_velocity', 2.0,
                              'Maximum joint velocity (rad/s)')
        self.declare_parameter('balance_threshold', 0.05,
                              'Balance stability threshold')
        self.declare_parameter('safety_limits.enabled', True,
                              'Enable safety limit enforcement')
        self.declare_parameter('safety_limits.max_torque', 100.0,
                              'Maximum torque limit (Nm)')

        # Set up parameter callback for dynamic reconfiguration
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        """Handle parameter updates"""
        for param in params:
            if param.name == 'balance_threshold':
                self.get_logger().info(f'Balance threshold updated to {param.value}')
                # Update balance control algorithm
            elif param.name == 'max_joint_velocity':
                self.get_logger().info(f'Max velocity updated to {param.value}')
                # Update joint controller limits
        return rclpy.node.SetParametersResult(successful=True)
```

## Advanced Humanoid Control Systems

### Joint Trajectory Control

```python
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
import numpy as np

class HumanoidTrajectoryController(Node):
    def __init__(self):
        super().__init__('humanoid_trajectory_controller')

        # Joint trajectory publisher
        self.trajectory_pub = self.create_publisher(
            JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)

        # Action client for more sophisticated control
        self.trajectory_client = ActionClient(
            self, FollowJointTrajectory, '/joint_trajectory_controller/follow_joint_trajectory')

        # Joint names for a typical humanoid
        self.joint_names = [
            'left_hip_joint', 'left_knee_joint', 'left_ankle_joint',
            'right_hip_joint', 'right_knee_joint', 'right_ankle_joint',
            'left_shoulder_joint', 'left_elbow_joint', 'left_wrist_joint',
            'right_shoulder_joint', 'right_elbow_joint', 'right_wrist_joint',
            'head_pan_joint', 'head_tilt_joint'
        ]

        # Timer for control loop
        self.control_timer = self.create_timer(0.01, self.control_loop)  # 100 Hz
        self.time = 0.0

    def generate_walking_trajectory(self, step_length=0.3, step_height=0.05):
        """Generate a simple walking trajectory"""
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names

        # Create trajectory points for walking motion
        # This is a simplified example - real walking would be much more complex
        for t in np.linspace(0, 2.0, 200):  # 2 seconds, 200 points
            point = JointTrajectoryPoint()

            # Simplified walking pattern - in practice, this would use inverse kinematics
            # and proper gait planning algorithms
            left_leg_pos = [
                np.sin(t * np.pi) * 0.1,      # hip flexion/extension
                np.sin(t * np.pi * 2) * 0.2,  # knee flexion
                np.sin(t * np.pi) * 0.05      # ankle
            ]

            right_leg_pos = [
                np.sin(t * np.pi + np.pi) * 0.1,  # out of phase with left
                np.sin(t * np.pi * 2 + np.pi) * 0.2,
                np.sin(t * np.pi + np.pi) * 0.05
            ]

            # Set positions for all joints
            positions = left_leg_pos + [0.0] * 3 + right_leg_pos + [0.0] * 3 + [0.0, 0.0]
            point.positions = positions

            # Set timing
            point.time_from_start = Duration(sec=int(t), nanosec=int((t - int(t)) * 1e9))

            trajectory.points.append(point)

        return trajectory

    def send_trajectory(self, trajectory):
        """Send trajectory to controller"""
        self.trajectory_pub.publish(trajectory)
        self.get_logger().info(f'Published trajectory with {len(trajectory.points)} points')

    def control_loop(self):
        """Main control loop"""
        # Generate and send walking trajectory periodically
        if self.time % 5.0 < 0.01:  # Every 5 seconds
            walking_traj = self.generate_walking_trajectory()
            self.send_trajectory(walking_traj)

        self.time += 0.01
```

### Sensor Fusion and State Estimation

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, JointState
from geometry_msgs.msg import Pose, Twist
from tf2_ros import TransformBroadcaster
import numpy as np
from scipy.spatial.transform import Rotation as R

class HumanoidStateEstimator(Node):
    def __init__(self):
        super().__init__('humanoid_state_estimator')

        # Subscriptions for various sensors
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10)
        self.joint_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_callback, 10)

        # Publishers for estimated state
        self.pose_pub = self.create_publisher(Pose, '/robot_pose', 10)
        self.twist_pub = self.create_publisher(Twist, '/robot_twist', 10)

        # TF broadcaster for robot transforms
        self.tf_broadcaster = TransformBroadcaster(self)

        # State estimation variables
        self.orientation = R.from_quat([0, 0, 0, 1])  # Identity rotation
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.angular_velocity = np.array([0.0, 0.0, 0.0])

        # Timer for state estimation loop
        self.estimation_timer = self.create_timer(0.01, self.estimation_loop)  # 100 Hz

        self.last_imu_time = self.get_clock().now()
        self.joint_states = {}

    def imu_callback(self, msg):
        """Process IMU data for orientation and angular velocity"""
        # Extract orientation from IMU (if available)
        if msg.orientation.w != 0 or msg.orientation.x != 0 or \
           msg.orientation.y != 0 or msg.orientation.z != 0:
            self.orientation = R.from_quat([
                msg.orientation.x,
                msg.orientation.y,
                msg.orientation.z,
                msg.orientation.w
            ])

        # Extract angular velocity
        self.angular_velocity = np.array([
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z
        ])

        # Extract linear acceleration (for integration to velocity)
        current_time = self.get_clock().now()
        dt = (current_time - self.last_imu_time).nanoseconds / 1e9
        self.last_imu_time = current_time

        # Integrate acceleration to get velocity (simplified)
        linear_acc = np.array([
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z
        ])

        # Apply gravity compensation and integrate
        gravity = np.array([0, 0, 9.81])
        corrected_acc = self.orientation.apply(linear_acc) - gravity
        self.velocity += corrected_acc * dt

    def joint_callback(self, msg):
        """Process joint state data"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_states[name] = {
                    'position': msg.position[i],
                    'velocity': msg.velocity[i] if i < len(msg.velocity) else 0.0,
                    'effort': msg.effort[i] if i < len(msg.effort) else 0.0
                }

    def estimation_loop(self):
        """Main state estimation loop"""
        # Update robot pose based on sensor fusion
        current_pose = Pose()
        current_pose.position.x = float(self.position[0])
        current_pose.position.y = float(self.position[1])
        current_pose.position.z = float(self.position[2])

        # Set orientation
        quat = self.orientation.as_quat()
        current_pose.orientation.x = quat[0]
        current_pose.orientation.y = quat[1]
        current_pose.orientation.z = quat[2]
        current_pose.orientation.w = quat[3]

        # Publish estimated pose
        self.pose_pub.publish(current_pose)

        # Publish velocity
        current_twist = Twist()
        current_twist.linear.x = float(self.velocity[0])
        current_twist.linear.y = float(self.velocity[1])
        current_twist.linear.z = float(self.velocity[2])

        current_twist.angular.x = float(self.angular_velocity[0])
        current_twist.angular.y = float(self.angular_velocity[1])
        current_twist.angular.z = float(self.angular_velocity[2])

        self.twist_pub.publish(current_twist)

        # Broadcast transforms for visualization
        self.broadcast_transforms()

    def broadcast_transforms(self):
        """Broadcast robot transforms for RViz and other tools"""
        from geometry_msgs.msg import TransformStamped

        # Example: Broadcast base link transform
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'

        t.transform.translation.x = self.position[0]
        t.transform.translation.y = self.position[1]
        t.transform.translation.z = self.position[2]

        quat = self.orientation.as_quat()
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        self.tf_broadcaster.sendTransform(t)
```

## Understanding URDF (Unified Robot Description Format) for Humanoids

URDF describes robot structure, kinematics, and dynamics. For humanoid robots, URDF becomes more complex due to multiple limbs and sophisticated joint structures:

```xml
<?xml version="1.0"?>
<robot name="advanced_humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Material definitions -->
  <material name="black">
    <color rgba="0.0 0.0 0.0 1.0"/>
  </material>
  <material name="blue">
    <color rgba="0.0 0.0 0.8 1.0"/>
  </material>
  <material name="green">
    <color rgba="0.0 0.8 0.0 1.0"/>
  </material>
  <material name="grey">
    <color rgba="0.5 0.5 0.5 1.0"/>
  </material>
  <material name="silver">
    <color rgba="0.9 0.9 0.9 1.0"/>
  </material>
  <material name="orange">
    <color rgba="1.0 0.423529411765 0.0392156862745 1.0"/>
  </material>
  <material name="brown">
    <color rgba="0.870588235294 0.811764705882 0.764705882353 1.0"/>
  </material>
  <material name="red">
    <color rgba="0.8 0.0 0.0 1.0"/>
  </material>
  <material name="white">
    <color rgba="1.0 1.0 1.0 1.0"/>
  </material>

  <!-- Base/Fixed link -->
  <link name="base_link">
    <inertial>
      <mass value="5.0"/>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.2 0.2"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.2 0.2"/>
      </geometry>
    </collision>
  </link>

  <!-- Torso -->
  <joint name="torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
  </joint>

  <link name="torso">
    <inertial>
      <mass value="8.0"/>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <inertia ixx="0.3" ixy="0" ixz="0" iyy="0.3" iyz="0" izz="0.1"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <geometry>
        <box size="0.25 0.2 0.5"/>
      </geometry>
      <material name="grey"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <geometry>
        <box size="0.25 0.2 0.5"/>
      </geometry>
    </collision>
  </link>

  <!-- Head -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/> <!-- Pitch axis -->
    <limit lower="-0.5" upper="0.5" effort="10" velocity="2"/>
  </joint>

  <link name="head">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.02"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
    </collision>
  </link>

  <!-- Head pan joint -->
  <joint name="head_pan_joint" type="revolute">
    <parent link="head"/>
    <child link="head_camera"/>
    <origin xyz="0.05 0 0.05" rpy="0 0 0"/>
    <axis xyz="0 0 1"/> <!-- Yaw axis -->
    <limit lower="-1.57" upper="1.57" effort="5" velocity="3"/>
  </joint>

  <link name="head_camera">
    <inertial>
      <mass value="0.1"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Left Arm -->
  <!-- Shoulder -->
  <joint name="left_shoulder_pitch_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.15 0.1 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/> <!-- Pitch -->
    <limit lower="-1.57" upper="1.57" effort="50" velocity="2"/>
  </joint>

  <link name="left_upper_arm">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <inertia ixx="0.05" ixy="0" ixz="0" iyy="0.05" iyz="0" izz="0.01"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.05" length="0.2"/>
      </geometry>
      <material name="orange"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.05" length="0.2"/>
      </geometry>
    </collision>
  </link>

  <!-- Elbow -->
  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="1 0 0"/> <!-- Roll -->
    <limit lower="0" upper="2.5" effort="40" velocity="2"/>
  </joint>

  <link name="left_lower_arm">
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <inertia ixx="0.03" ixy="0" ixz="0" iyy="0.03" iyz="0" izz="0.008"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.04" length="0.16"/>
      </geometry>
      <material name="orange"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.04" length="0.16"/>
      </geometry>
    </collision>
  </link>

  <!-- Left Hand -->
  <joint name="left_wrist_joint" type="revolute">
    <parent link="left_lower_arm"/>
    <child link="left_hand"/>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/> <!-- Pitch -->
    <limit lower="-1.0" upper="1.0" effort="20" velocity="3"/>
  </joint>

  <link name="left_hand">
    <inertial>
      <mass value="0.5"/>
      <origin xyz="0 0 -0.05" rpy="0 0 0"/>
      <inertia ixx="0.002" ixy="0" ixz="0" iyy="0.002" iyz="0" izz="0.001"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.1 0.08 0.1"/>
      </geometry>
      <material name="silver"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.1 0.08 0.1"/>
      </geometry>
    </collision>
  </link>

  <!-- Right Arm (symmetric to left) -->
  <joint name="right_shoulder_pitch_joint" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="0.15 -0.1 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="2"/>
  </joint>

  <link name="right_upper_arm">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <inertia ixx="0.05" ixy="0" ixz="0" iyy="0.05" iyz="0" izz="0.01"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.05" length="0.2"/>
      </geometry>
      <material name="orange"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.05" length="0.2"/>
      </geometry>
    </collision>
  </link>

  <joint name="right_elbow_joint" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_lower_arm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="0" upper="2.5" effort="40" velocity="2"/>
  </joint>

  <link name="right_lower_arm">
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <inertia ixx="0.03" ixy="0" ixz="0" iyy="0.03" iyz="0" izz="0.008"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.04" length="0.16"/>
      </geometry>
      <material name="orange"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.04" length="0.16"/>
      </geometry>
    </collision>
  </link>

  <joint name="right_wrist_joint" type="revolute">
    <parent link="right_lower_arm"/>
    <child link="right_hand"/>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.0" upper="1.0" effort="20" velocity="3"/>
  </joint>

  <link name="right_hand">
    <inertial>
      <mass value="0.5"/>
      <origin xyz="0 0 -0.05" rpy="0 0 0"/>
      <inertia ixx="0.002" ixy="0" ixz="0" iyy="0.002" iyz="0" izz="0.001"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.1 0.08 0.1"/>
      </geometry>
      <material name="silver"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.1 0.08 0.1"/>
      </geometry>
    </collision>
  </link>

  <!-- Left Leg -->
  <joint name="left_hip_yaw_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_hip"/>
    <origin xyz="-0.05 0.08 -0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/> <!-- Yaw -->
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1"/>
  </joint>

  <link name="left_hip">
    <inertial>
      <mass value="3.0"/>
      <origin xyz="0 0 -0.1" rpy="0 0 0"/>
      <inertia ixx="0.08" ixy="0" ixz="0" iyy="0.08" iyz="0" izz="0.02"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.1" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.06" length="0.1"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.1" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.06" length="0.1"/>
      </geometry>
    </collision>
  </link>

  <joint name="left_hip_roll_joint" type="revolute">
    <parent link="left_hip"/>
    <child link="left_thigh"/>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <axis xyz="1 0 0"/> <!-- Roll -->
    <limit lower="-0.3" upper="0.3" effort="100" velocity="1"/>
  </joint>

  <link name="left_thigh">
    <inertial>
      <mass value="5.0"/>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <inertia ixx="0.2" ixy="0" ixz="0" iyy="0.2" iyz="0" izz="0.05"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.08" length="0.3"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.08" length="0.3"/>
      </geometry>
    </collision>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_thigh"/>
    <child link="left_shin"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/> <!-- Pitch -->
    <limit lower="0" upper="2.0" effort="100" velocity="1"/>
  </joint>

  <link name="left_shin">
    <inertial>
      <mass value="4.0"/>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <inertia ixx="0.15" ixy="0" ixz="0" iyy="0.15" iyz="0" izz="0.04"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.07" length="0.3"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.07" length="0.3"/>
      </geometry>
    </collision>
  </link>

  <joint name="left_ankle_joint" type="revolute">
    <parent link="left_shin"/>
    <child link="left_foot"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/> <!-- Pitch -->
    <limit lower="-0.5" upper="0.5" effort="50" velocity="1"/>
  </joint>

  <link name="left_foot">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0.1 0 -0.05" rpy="0 0 0"/>
      <inertia ixx="0.05" ixy="0" ixz="0" iyy="0.08" iyz="0" izz="0.03"/>
    </inertial>
    <visual>
      <origin xyz="0.1 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.25 0.15 0.1"/>
      </geometry>
      <material name="brown"/>
    </visual>
    <collision>
      <origin xyz="0.1 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.25 0.15 0.1"/>
      </geometry>
    </collision>
  </link>

  <!-- Right Leg (symmetric to left) -->
  <joint name="right_hip_yaw_joint" type="revolute">
    <parent link="torso"/>
    <child link="right_hip"/>
    <origin xyz="-0.05 -0.08 -0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1"/>
  </joint>

  <link name="right_hip">
    <inertial>
      <mass value="3.0"/>
      <origin xyz="0 0 -0.1" rpy="0 0 0"/>
      <inertia ixx="0.08" ixy="0" ixz="0" iyy="0.08" iyz="0" izz="0.02"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.1" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.06" length="0.1"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.1" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.06" length="0.1"/>
      </geometry>
    </collision>
  </link>

  <joint name="right_hip_roll_joint" type="revolute">
    <parent link="right_hip"/>
    <child link="right_thigh"/>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-0.3" upper="0.3" effort="100" velocity="1"/>
  </joint>

  <link name="right_thigh">
    <inertial>
      <mass value="5.0"/>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <inertia ixx="0.2" ixy="0" ixz="0" iyy="0.2" iyz="0" izz="0.05"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.08" length="0.3"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.08" length="0.3"/>
      </geometry>
    </collision>
  </link>

  <joint name="right_knee_joint" type="revolute">
    <parent link="right_thigh"/>
    <child link="right_shin"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="0" upper="2.0" effort="100" velocity="1"/>
  </joint>

  <link name="right_shin">
    <inertial>
      <mass value="4.0"/>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <inertia ixx="0.15" ixy="0" ixz="0" iyy="0.15" iyz="0" izz="0.04"/>
    </inertial>
    <visual>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.07" length="0.3"/>
      </geometry>
      <material name="green"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <capsule radius="0.07" length="0.3"/>
      </geometry>
    </collision>
  </link>

  <joint name="right_ankle_joint" type="revolute">
    <parent link="right_shin"/>
    <child link="right_foot"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-0.5" upper="0.5" effort="50" velocity="1"/>
  </joint>

  <link name="right_foot">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0.1 0 -0.05" rpy="0 0 0"/>
      <inertia ixx="0.05" ixy="0" ixz="0" iyy="0.08" iyz="0" izz="0.03"/>
    </inertial>
    <visual>
      <origin xyz="0.1 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.25 0.15 0.1"/>
      </geometry>
      <material name="brown"/>
    </visual>
    <collision>
      <origin xyz="0.1 0 -0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.25 0.15 0.1"/>
      </geometry>
    </collision>
  </link>

  <!-- Gazebo plugin for simulation -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/humanoid_robot</robotNamespace>
    </plugin>
  </gazebo>

</robot>
```

## Advanced ROS 2 Tools for Humanoid Development

### Robot State Publisher

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Header
import math

class AdvancedRobotStatePublisher(Node):
    def __init__(self):
        super().__init__('advanced_robot_state_publisher')

        # Subscribe to joint states
        self.joint_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_callback, 10)

        # TF broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Store joint positions
        self.joint_positions = {}

        # Timer for publishing transforms
        self.timer = self.create_timer(0.02, self.publish_transforms)  # 50 Hz

    def joint_callback(self, msg):
        """Update joint positions from joint state message"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]

    def publish_transforms(self):
        """Publish all robot transforms"""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'

        # For a humanoid, you might want to compute transforms based on
        # forward kinematics rather than fixed transforms
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.8  # Standing height
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)

        # Publish additional transforms for each joint
        # (In practice, you'd compute these based on joint angles using FK)
        self.publish_link_transform('torso', 'base_link', [0, 0, 0.1], [0, 0, 0, 1])
        self.publish_link_transform('head', 'torso', [0, 0, 0.5], [0, 0, 0, 1])

    def publish_link_transform(self, child_frame, parent_frame, translation, rotation):
        """Helper to publish a single transform"""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = parent_frame
        t.child_frame_id = child_frame
        t.transform.translation.x = translation[0]
        t.transform.translation.y = translation[1]
        t.transform.translation.z = translation[2]
        t.transform.rotation.x = rotation[0]
        t.transform.rotation.y = rotation[1]
        t.transform.rotation.z = rotation[2]
        t.transform.rotation.w = rotation[3]
        self.tf_broadcaster.sendTransform(t)

def main():
    rclpy.init()
    node = AdvancedRobotStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

This comprehensive overview of ROS 2 for humanoid robotics covers the essential concepts needed to build and control complex humanoid robots. The middleware provides the communication infrastructure that allows all the different subsystems of a humanoid robot to work together seamlessly, enabling the sophisticated behaviors required for physical AI applications.