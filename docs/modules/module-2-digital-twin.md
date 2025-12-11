---
sidebar_position: 3
title: Module 2 - The Digital Twin (Gazebo & Unity)
---

# Module 2: The Digital Twin (Gazebo & Unity)

## Focus: Physics simulation and environment building

Digital twins enable safe testing and training of humanoid robots in virtual environments before deployment in the real world. These virtual environments allow for extensive testing, validation, and training without the risks and costs associated with physical hardware.

## Advanced Physics Simulation in Gazebo

Gazebo provides sophisticated physics simulation capabilities essential for humanoid robotics development:

### Core Physics Engine Features

Gazebo supports multiple physics engines (ODE, Bullet, Simbody) with support for:

- **Gravity and Inertial Properties**: Accurate modeling of gravitational effects and mass distribution
- **Collision Detection**: Precise contact modeling between objects
- **Joint Dynamics**: Realistic actuator behavior and compliance
- **Contact Forces**: Proper force computation at contact points
- **Friction Modeling**: Static and dynamic friction coefficients
- **Damping Effects**: Velocity-dependent resistance forces

### Advanced Gazebo World Configuration

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="advanced_humanoid_world">

    <!-- Physics Engine Configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000.0</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>

      <!-- Solver Configuration -->
      <ode>
        <solver>
          <type>quick</type>
          <iters>1000</iters>
          <sor>1.3</sor>
        </solver>

        <!-- Constraints Configuration -->
        <constraints>
          <cfm>0.0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>

    <!-- Atmosphere Simulation -->
    <atmosphere type="adiabatic">
      <temperature>288.15</temperature>
      <pressure>101325.0</pressure>
    </atmosphere>

    <!-- Wind Effects -->
    <wind>
      <linear_velocity>0.5 0 0</linear_velocity>
    </wind>

    <!-- Ground Plane with Advanced Materials -->
    <include>
      <uri>model://ground_plane</uri>
      <pose>0 0 0 0 0 0</pose>
    </include>

    <!-- Lighting System -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.6 0.4 -0.8</direction>
    </light>

    <!-- Ambient Light -->
    <light name="ambient_light" type="point">
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.2 0.2 0.2 1</diffuse>
      <attenuation>
        <range>20</range>
        <constant>0.2</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
    </light>

    <!-- Example Humanoid Robot -->
    <include>
      <uri>model://humanoid_robot</uri>
      <pose>0 0 0.8 0 0 0</pose>
    </include>

    <!-- Various Objects for Testing -->
    <include>
      <uri>model://table</uri>
      <pose>2 0 0 0 0 0</pose>
    </include>

    <include>
      <uri>model://cube</uri>
      <pose>2.5 0 0.5 0 0 0</pose>
    </include>

    <!-- Sensors for Environment Perception -->
    <model name="environment_sensors">
      <pose>5 0 2 0 0 0</pose>
      <link name="sensor_link">
        <pose>0 0 0 0 0 0</pose>
        <visual>
          <geometry>
            <box>
              <size>0.1 0.1 0.1</size>
            </box>
          </geometry>
        </visual>
        <collision>
          <geometry>
            <box>
              <size>0.1 0.1 0.1</size>
            </box>
          </geometry>
        </collision>
      </link>
    </model>

  </world>
</sdf>
```

### Advanced Robot Model Configuration

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="advanced_humanoid_robot">

    <!-- Base Link -->
    <link name="base_link">
      <pose>0 0 0.8 0 0 0</pose>
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.1</iyy>
          <iyz>0.0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>

      <visual name="base_visual">
        <geometry>
          <box>
            <size>0.3 0.2 0.2</size>
          </box>
        </geometry>
        <material>
          <script>
            <uri>file://media/materials/scripts/gazebo.material</uri>
            <name>Gazebo/Blue</name>
          </script>
        </material>
      </visual>

      <collision name="base_collision">
        <geometry>
          <box>
            <size>0.3 0.2 0.2</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Torso -->
    <joint name="torso_joint" type="fixed">
      <parent>base_link</parent>
      <child>torso</child>
      <pose>0 0 0.1 0 0 0</pose>
    </joint>

    <link name="torso">
      <inertial>
        <mass>8.0</mass>
        <inertia>
          <ixx>0.2</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.2</iyy>
          <iyz>0.0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>

      <visual name="torso_visual">
        <geometry>
          <box>
            <size>0.25 0.2 0.5</size>
          </box>
        </geometry>
        <material>
          <script>
            <uri>file://media/materials/scripts/gazebo.material</uri>
            <name>Gazebo/Grey</name>
          </script>
        </material>
      </visual>

      <collision name="torso_collision">
        <geometry>
          <box>
            <size>0.25 0.2 0.5</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Head -->
    <joint name="neck_joint" type="revolute">
      <parent>torso</parent>
      <child>head</child>
      <pose>0 0 0.5 0 0 0</pose>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
          <effort>10</effort>
          <velocity>2</velocity>
        </limit>
      </axis>
    </joint>

    <link name="head">
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.02</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.02</iyy>
          <iyz>0.0</iyz>
          <izz>0.02</izz>
        </inertia>
      </inertial>

      <visual name="head_visual">
        <geometry>
          <sphere>
            <radius>0.15</radius>
          </sphere>
        </geometry>
        <material>
          <script>
            <uri>file://media/materials/scripts/gazebo.material</uri>
            <name>Gazebo/White</name>
          </script>
        </material>
      </visual>

      <collision name="head_collision">
        <geometry>
          <sphere>
            <radius>0.15</radius>
          </sphere>
        </geometry>
      </collision>
    </link>

    <!-- Left Arm -->
    <joint name="left_shoulder_joint" type="revolute">
      <parent>torso</parent>
      <child>left_upper_arm</child>
      <pose>0.15 0.1 0.3 0 0 0</pose>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>50</effort>
          <velocity>2</velocity>
        </limit>
      </axis>
    </joint>

    <link name="left_upper_arm">
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.05</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.05</iyy>
          <iyz>0.0</iyz>
          <izz>0.01</izz>
        </inertia>
      </inertial>

      <visual name="left_upper_arm_visual">
        <geometry>
          <capsule>
            <radius>0.05</radius>
            <length>0.3</length>
          </capsule>
        </geometry>
        <material>
          <script>
            <uri>file://media/materials/scripts/gazebo.material</uri>
            <name>Gazebo/Orange</name>
          </script>
        </material>
      </visual>

      <collision name="left_upper_arm_collision">
        <geometry>
          <capsule>
            <radius>0.05</radius>
            <length>0.3</length>
          </capsule>
        </geometry>
      </collision>
    </link>

    <!-- Additional joints and links for complete humanoid model -->
    <!-- ... (elided for brevity) ... -->

    <!-- Sensors in Gazebo -->

    <!-- IMU Sensor -->
    <sensor name="imu_sensor" type="imu">
      <always_on>1</always_on>
      <update_rate>100</update_rate>
      <pose>0 0 0 0 0 0</pose>
      <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
        <ros>
          <namespace>/humanoid_robot</namespace>
          <remapping>~/out:=imu/data</remapping>
        </ros>
        <initial_orientation_as_reference>false</initial_orientation_as_reference>
        <gaussian_noise>0.01</gaussian_noise>
      </plugin>
    </sensor>

    <!-- Camera Sensor -->
    <sensor name="camera_sensor" type="camera">
      <always_on>1</always_on>
      <update_rate>30</update_rate>
      <pose>0.1 0 0.1 0 0 0</pose>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>10</far>
        </clip>
      </camera>
      <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/humanoid_robot</namespace>
          <remapping>image_raw:=camera/image_raw</remapping>
          <remapping>camera_info:=camera/camera_info</remapping>
        </ros>
      </plugin>
    </sensor>

    <!-- LiDAR Sensor -->
    <sensor name="lidar_sensor" type="ray">
      <always_on>1</always_on>
      <update_rate>10</update_rate>
      <pose>0.15 0 0.2 0 0 0</pose>
      <ray>
        <scan>
          <horizontal>
            <samples>720</samples>
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>
            <max_angle>3.14159</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>30.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="lidar_plugin" filename="libgazebo_ros_laser.so">
        <ros>
          <namespace>/humanoid_robot</namespace>
          <remapping>scan:=lidar/scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
      </plugin>
    </sensor>

    <!-- Joint State Publisher Plugin -->
    <gazebo>
      <plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
        <ros>
          <namespace>/humanoid_robot</namespace>
          <remapping>~/out:=joint_states</remapping>
        </ros>
        <update_rate>30</update_rate>
        <joint_name>left_shoulder_joint</joint_name>
        <joint_name>right_shoulder_joint</joint_name>
        <!-- Add more joints as needed -->
      </plugin>
    </gazebo>

  </model>
</sdf>
```

## High-Fidelity Rendering and Human-Robot Interaction in Unity

Unity provides photorealistic rendering capabilities for advanced robotics applications:

### Unity Robotics Simulation Setup

```csharp
using UnityEngine;
using UnityEngine.Rendering.HighDefinition;
using System.Collections;
using RosMessageTypes.Sensor;
using RosMessageTypes.Geometry;

public class UnityHumanoidSimulator : MonoBehaviour
{
    [Header("Robot Configuration")]
    public GameObject humanoidRobot;
    public Transform[] jointTransforms;
    public ArticulationBody[] articulationBodies;

    [Header("Camera Configuration")]
    public Camera robotCamera;
    public Camera headCamera;
    public RenderTexture cameraRenderTexture;

    [Header("ROS Connection")]
    public string rosBridgeAddress = "ws://localhost:9090";
    private RosSharp.RosBridgeClient.RosSocket rosSocket;

    void Start()
    {
        InitializeRobot();
        ConnectToRosBridge();
        StartCoroutine(PublishRobotState());
    }

    void InitializeRobot()
    {
        // Configure articulation bodies for realistic joint behavior
        foreach (var body in articulationBodies)
        {
            ConfigureArticulationBody(body);
        }

        // Set up camera with realistic parameters
        SetupCameras();
    }

    void ConfigureArticulationBody(ArticulationBody body)
    {
        // Configure joint limits, drive, and other parameters
        ArticulationDrive drive = body.xDrive;
        drive.forceLimit = 1000f;
        drive.damping = 10f;
        drive.stiffness = 100f;
        body.xDrive = drive;

        // Similar configuration for other axes if needed
        body.linearLockX = ArticulationDofLock.Locked;
        body.linearLockY = ArticulationDofLock.LimitedMotion;
        body.linearLockZ = ArticulationDofLock.Locked;
    }

    void SetupCameras()
    {
        // Configure robot-mounted cameras
        if (robotCamera != null)
        {
            robotCamera.fieldOfView = 60f; // Typical for RGB cameras
            robotCamera.allowMSAA = true;
            robotCamera.allowDynamicResolution = true;
        }

        if (headCamera != null)
        {
            headCamera.fieldOfView = 90f; // Wider field of view for head camera
        }
    }

    void ConnectToRosBridge()
    {
        RosSharp.RosBridgeClient.WebSocketProtocols.UnityWebSocket.WebSocket socket =
            new RosSharp.RosBridgeClient.WebSocketProtocols.UnityWebSocket.WebSocket(rosBridgeAddress);
        rosSocket = new RosSharp.RosBridgeClient.RosSocket(socket);
    }

    IEnumerator PublishRobotState()
    {
        while (true)
        {
            // Publish joint states
            PublishJointStates();

            // Publish camera images
            PublishCameraImages();

            // Publish IMU data
            PublishIMUMessage();

            yield return new WaitForSeconds(0.033f); // ~30 Hz
        }
    }

    void PublishJointStates()
    {
        // Create and populate joint state message
        var jointStateMsg = new JointStateMsg();
        jointStateMsg.name = new string[jointTransforms.Length];
        jointStateMsg.position = new double[jointTransforms.Length];
        jointStateMsg.velocity = new double[jointTransforms.Length];
        jointStateMsg.effort = new double[jointTransforms.Length];

        for (int i = 0; i < jointTransforms.Length; i++)
        {
            jointStateMsg.name[i] = jointTransforms[i].name;
            jointStateMsg.position[i] = jointTransforms[i].localEulerAngles.y * Mathf.Deg2Rad;
            // Add velocity and effort calculations
        }

        rosSocket.Publish("/joint_states", jointStateMsg);
    }

    void PublishCameraImages()
    {
        if (robotCamera != null)
        {
            // Capture camera image and convert to ROS message
            RenderTexture.active = cameraRenderTexture;
            Texture2D texture2D = new Texture2D(cameraRenderTexture.width, cameraRenderTexture.height, TextureFormat.RGB24, false);
            texture2D.ReadPixels(new Rect(0, 0, cameraRenderTexture.width, cameraRenderTexture.height), 0, 0);
            texture2D.Apply();

            // Convert to ROS Image message
            ImageMsg imageMsg = new ImageMsg();
            imageMsg.header = new StandardHeaderMsg();
            imageMsg.header.stamp = new TimeMsg(System.DateTime.Now.Second, System.DateTime.Now.Millisecond * 1000000);
            imageMsg.header.frame_id = "camera_rgb_optical_frame";

            // Set image properties
            imageMsg.height = (uint)texture2D.height;
            imageMsg.width = (uint)texture2D.width;
            imageMsg.encoding = "rgb8";
            imageMsg.is_bigendian = 0;
            imageMsg.step = (uint)(texture2D.width * 3); // 3 bytes per pixel for RGB

            // Convert texture to byte array
            byte[] imageData = texture2D.EncodeToPNG();
            imageMsg.data = imageData;

            rosSocket.Publish("/camera/image_raw", imageMsg);

            // Clean up
            Destroy(texture2D);
        }
    }

    void PublishIMUMessage()
    {
        var imuMsg = new ImuMsg();
        imuMsg.header = new StandardHeaderMsg();
        imuMsg.header.stamp = new TimeMsg();
        imuMsg.header.frame_id = "imu_link";

        // Set orientation (from robot's rotation)
        Quaternion robotRotation = humanoidRobot.transform.rotation;
        imuMsg.orientation.x = robotRotation.x;
        imuMsg.orientation.y = robotRotation.y;
        imuMsg.orientation.z = robotRotation.z;
        imuMsg.orientation.w = robotRotation.w;

        // Set angular velocity
        // This would typically come from ArticulationBody angular velocity
        imuMsg.angular_velocity.x = 0.0;
        imuMsg.angular_velocity.y = 0.0;
        imuMsg.angular_velocity.z = 0.0;

        // Set linear acceleration
        imuMsg.linear_acceleration.x = 0.0;
        imuMsg.linear_acceleration.y = -9.81; // Gravity
        imuMsg.linear_acceleration.z = 0.0;

        rosSocket.Publish("/imu/data", imuMsg);
    }

    public void SetJointPositions(double[] positions)
    {
        // Update robot joint positions based on incoming ROS commands
        for (int i = 0; i < Mathf.Min(positions.Length, jointTransforms.Length); i++)
        {
            jointTransforms[i].localEulerAngles = new Vector3(0, positions[i] * Mathf.Rad2Deg, 0);
        }
    }
}
```

### Advanced Unity Scene Setup for Human-Robot Interaction

```csharp
using UnityEngine;
using UnityEngine.XR;
using System.Collections.Generic;

public class HumanRobotInteractionScene : MonoBehaviour
{
    [Header("Environment Setup")]
    public GameObject[] furniturePrefabs;
    public GameObject[] obstaclePrefabs;
    public Light[] sceneLights;

    [Header("Human Interaction")]
    public GameObject[] humanAvatars;
    public AnimationController[] humanAnimators;

    [Header("Physics Configuration")]
    public PhysicMaterial highFrictionMaterial;
    public PhysicMaterial lowFrictionMaterial;

    [Header("Domain Randomization")]
    public Color[] randomColors;
    public Material[] randomMaterials;
    public float domainRandomizationInterval = 10.0f;

    private List<GameObject> spawnedObjects = new List<GameObject>();
    private float lastRandomizationTime = 0.0f;

    void Start()
    {
        InitializeEnvironment();
        StartCoroutine(DomainRandomizationLoop());
    }

    void InitializeEnvironment()
    {
        // Spawn furniture and obstacles
        SpawnEnvironmentObjects();

        // Configure lighting for realistic rendering
        ConfigureLighting();

        // Set up physics materials for realistic interaction
        ConfigurePhysicsMaterials();

        // Initialize human avatars
        InitializeHumanAvatars();
    }

    void SpawnEnvironmentObjects()
    {
        // Randomly spawn furniture in the environment
        int numFurniture = Random.Range(5, 15);
        for (int i = 0; i < numFurniture; i++)
        {
            Vector3 spawnPosition = new Vector3(
                Random.Range(-10f, 10f),
                0f,
                Random.Range(-10f, 10f)
            );

            GameObject prefab = furniturePrefabs[Random.Range(0, furniturePrefabs.Length)];
            GameObject spawnedObject = Instantiate(prefab, spawnPosition, Quaternion.identity);
            spawnedObjects.Add(spawnedObject);
        }

        // Spawn obstacles
        int numObstacles = Random.Range(3, 8);
        for (int i = 0; i < numObstacles; i++)
        {
            Vector3 spawnPosition = new Vector3(
                Random.Range(-8f, 8f),
                0.5f,
                Random.Range(-8f, 8f)
            );

            GameObject prefab = obstaclePrefabs[Random.Range(0, obstaclePrefabs.Length)];
            GameObject spawnedObject = Instantiate(prefab, spawnPosition, Quaternion.identity);
            spawnedObjects.Add(spawnObject);
        }
    }

    void ConfigureLighting()
    {
        // Randomize lighting conditions for domain randomization
        foreach (Light light in sceneLights)
        {
            light.color = Random.ColorHSV(0.8f, 1.0f, 0.8f, 1.0f, 0.8f, 1.0f);
            light.intensity = Random.Range(0.5f, 1.5f);

            // Add subtle movement to lights for realism
            StartCoroutine(MoveLight(light));
        }
    }

    IEnumerator MoveLight(Light light)
    {
        Vector3 originalPosition = light.transform.position;
        while (true)
        {
            // Apply subtle movement
            light.transform.position = originalPosition +
                new Vector3(Mathf.Sin(Time.time) * 0.1f,
                           Mathf.Cos(Time.time * 0.7f) * 0.05f,
                           Mathf.Sin(Time.time * 0.5f) * 0.1f);
            yield return null;
        }
    }

    void ConfigurePhysicsMaterials()
    {
        // Assign appropriate friction materials to surfaces
        Collider[] colliders = FindObjectsOfType<Collider>();
        foreach (Collider col in colliders)
        {
            if (col.name.Contains("floor") || col.name.Contains("ground"))
            {
                col.material = highFrictionMaterial; // For stable walking
            }
            else if (col.name.Contains("table") || col.name.Contains("desk"))
            {
                col.material = lowFrictionMaterial; // For sliding objects
            }
        }
    }

    void InitializeHumanAvatars()
    {
        // Position human avatars in the scene
        for (int i = 0; i < humanAvatars.Length; i++)
        {
            Vector3 spawnPos = new Vector3(
                Random.Range(-5f, 5f),
                0f,
                Random.Range(-5f, 5f)
            );
            humanAvatars[i].transform.position = spawnPos;

            // Assign random animations
            if (humanAnimators.Length > 0)
            {
                AnimationController animator = humanAvatars[i].GetComponent<AnimationController>();
                if (animator != null)
                {
                    // Play random human activities
                    string[] activities = {"walking", "standing", "sitting", "gesturing"};
                    string randomActivity = activities[Random.Range(0, activities.Length)];
                    animator.Play(randomActivity);
                }
            }
        }
    }

    IEnumerator DomainRandomizationLoop()
    {
        while (true)
        {
            if (Time.time - lastRandomizationTime > domainRandomizationInterval)
            {
                ApplyDomainRandomization();
                lastRandomizationTime = Time.time;
            }
            yield return new WaitForSeconds(domainRandomizationInterval);
        }
    }

    void ApplyDomainRandomization()
    {
        // Change colors of objects
        foreach (GameObject obj in spawnedObjects)
        {
            Renderer renderer = obj.GetComponent<Renderer>();
            if (renderer != null)
            {
                Material randomMat = randomMaterials[Random.Range(0, randomMaterials.Length)];
                renderer.material = randomMat;
            }
        }

        // Change lighting
        ConfigureLighting();

        // Potentially move/reposition some objects
        RepositionSomeObjects();
    }

    void RepositionSomeObjects()
    {
        // Randomly reposition 30% of the objects
        int numToMove = Mathf.CeilToInt(spawnedObjects.Count * 0.3f);
        for (int i = 0; i < numToMove; i++)
        {
            int index = Random.Range(0, spawnedObjects.Count);
            Vector3 newPos = new Vector3(
                Random.Range(-10f, 10f),
                0f,
                Random.Range(-10f, 10f)
            );
            spawnedObjects[index].transform.position = newPos;
        }
    }

    // Methods for synthetic data generation
    public Texture2D CaptureSyntheticImage(Camera cam, int width, int height)
    {
        // Render to texture and return synthetic image data
        RenderTexture rt = new RenderTexture(width, height, 24);
        cam.targetTexture = rt;
        cam.Render();

        RenderTexture.active = rt;
        Texture2D image = new Texture2D(width, height, TextureFormat.RGB24, false);
        image.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        image.Apply();

        cam.targetTexture = null;
        RenderTexture.active = null;
        Destroy(rt);

        return image;
    }

    public void GenerateTrainingDataset(int numSamples, string savePath)
    {
        // Generate synthetic training data with labels
        StartCoroutine(CreateTrainingDataset(numSamples, savePath));
    }

    IEnumerator CreateTrainingDataset(int numSamples, string savePath)
    {
        for (int i = 0; i < numSamples; i++)
        {
            // Capture image
            Texture2D image = CaptureSyntheticImage(robotCamera, 640, 480);

            // Generate corresponding labels (object detection, segmentation, etc.)
            // This would involve complex labeling logic

            // Save image and labels
            // File.WriteAllBytes($"{savePath}/image_{i:D6}.png", image.EncodeToPNG());

            // Randomize environment for next sample
            ApplyDomainRandomization();

            yield return null;
        }
    }
}
```

## Advanced Sensor Simulation

### Comprehensive Sensor Suite Configuration

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="advanced_sensors_suite">

    <!-- Multi-camera system -->
    <link name="sensors_mount">
      <pose>0.2 0 0.3 0 0 0</pose>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyy>0.001</iyy>
          <iyz>0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>

    <!-- RGB Camera -->
    <sensor name="rgb_camera" type="camera">
      <pose>0 0 0 0 0 0</pose>
      <camera>
        <horizontal_fov>1.047</horizontal_fov> <!-- 60 degrees -->
        <image>
          <width>1280</width>
          <height>720</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>30</far>
        </clip>
        <distortion>
          <k1>-0.15</k1>
          <k2>0.12</k2>
          <k3>-0.04</k3>
          <p1>0.0003</p1>
          <p2>-0.0002</p2>
          <center>0.5 0.5</center>
        </distortion>
      </camera>
      <always_on>1</always_on>
      <update_rate>30</update_rate>
      <visualize>true</visualize>
    </sensor>

    <!-- Depth Camera -->
    <sensor name="depth_camera" type="depth">
      <pose>0.05 0 0 0 0 0</pose>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
        </image>
        <clip>
          <near>0.1</near>
          <far>10</far>
        </clip>
      </camera>
      <always_on>1</always_on>
      <update_rate>30</update_rate>
      <visualize>true</visualize>
    </sensor>

    <!-- 360-degree LiDAR -->
    <sensor name="360_lidar" type="ray">
      <pose>0.1 0 0 0 0 0</pose>
      <ray>
        <scan>
          <horizontal>
            <samples>1440</samples> <!-- 0.25 degree resolution -->
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>
            <max_angle>3.14159</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>25.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <always_on>1</always_on>
      <update_rate>10</update_rate>
      <visualize>true</visualize>
    </sensor>

    <!-- 2D LiDAR (for navigation) -->
    <sensor name="navigation_lidar" type="ray">
      <pose>0.15 0 -0.05 0 0 0</pose>
      <ray>
        <scan>
          <horizontal>
            <samples>1081</samples> <!-- 0.33 degree resolution over 360 deg -->
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>
            <max_angle>3.14159</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>30.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <always_on>1</always_on>
      <update_rate>15</update_rate>
      <visualize>false</visualize>
    </sensor>

    <!-- IMU with realistic noise -->
    <sensor name="imu_sensor" type="imu">
      <pose>0.05 0.05 0.05 0 0 0</pose>
      <always_on>1</always_on>
      <update_rate>100</update_rate>
      <imu>
        <angular_velocity>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.01</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.01</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.01</stddev>
            </noise>
          </z>
        </angular_velocity>
        <linear_acceleration>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.1</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.1</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.1</stddev>
            </noise>
          </z>
        </linear_acceleration>
      </imu>
    </sensor>

    <!-- GPS Sensor -->
    <sensor name="gps_sensor" type="gps">
      <pose>0.2 -0.05 0.1 0 0 0</pose>
      <always_on>1</always_on>
      <update_rate>1</update_rate>
      <gps>
        <position_sensing>
          <horizontal>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.2</stddev>
            </noise>
          </horizontal>
          <vertical>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.5</stddev>
            </noise>
          </vertical>
        </position_sensing>
      </gps>
    </sensor>

    <!-- Force-Torque Sensor -->
    <sensor name="force_torque_sensor" type="force_torque">
      <pose>0 0 0 0 0 0</pose>
      <always_on>1</always_on>
      <update_rate>100</update_rate>
      <force_torque>
        <frame>child</frame>
        <measure_direction>child_to_parent</measure_direction>
      </force_torque>
    </sensor>

  </model>
</sdf>
```

## Simulation-to-Reality Transfer Techniques

### Domain Randomization for Robust Perception

```python
import numpy as np
import cv2
from PIL import Image
import random

class DomainRandomizer:
    def __init__(self):
        self.lighting_conditions = [
            {'intensity': 0.5, 'color_temp': 3000},  # Warm, dim
            {'intensity': 1.5, 'color_temp': 6500},  # Cool, bright
            {'intensity': 1.0, 'color_temp': 4500},  # Neutral
            {'intensity': 0.8, 'color_temp': 5500},  # Slightly cool
        ]

        self.textures = [
            'wood', 'metal', 'fabric', 'plastic', 'concrete'
        ]

        self.material_properties = {
            'roughness': (0.0, 1.0),
            'metallic': (0.0, 1.0),
            'specular': (0.0, 1.0)
        }

    def randomize_lighting(self, image, lighting_params):
        """Apply randomized lighting to image"""
        intensity = lighting_params['intensity']
        color_temp = lighting_params['color_temp']

        # Apply intensity adjustment
        img_float = image.astype(np.float32) * intensity

        # Apply color temperature (simplified)
        if color_temp < 4000:  # Warm light
            img_float[:, :, 0] *= 1.2  # Increase red
            img_float[:, :, 2] *= 0.8  # Decrease blue
        elif color_temp > 6000:  # Cool light
            img_float[:, :, 0] *= 0.8  # Decrease red
            img_float[:, :, 2] *= 1.2  # Increase blue

        # Clip values to valid range
        img_float = np.clip(img_float, 0, 255)
        return img_float.astype(np.uint8)

    def add_random_noise(self, image, noise_level=0.1):
        """Add realistic sensor noise"""
        # Add Gaussian noise
        gaussian_noise = np.random.normal(0, noise_level * 255, image.shape)
        noisy_img = image.astype(np.float32) + gaussian_noise

        # Add salt and pepper noise
        if random.random() < 0.1:  # 10% chance
            num_salt = np.ceil(0.001 * image.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape[:2]]
            noisy_img[coords[0], coords[1]] = 255

            num_pepper = np.ceil(0.001 * image.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape[:2]]
            noisy_img[coords[0], coords[1]] = 0

        return np.clip(noisy_img, 0, 255).astype(np.uint8)

    def randomize_texture(self, image, texture_type):
        """Apply texture-specific effects"""
        if texture_type == 'wood':
            # Add wood grain pattern
            h, w = image.shape[:2]
            for i in range(0, h, 10):  # Horizontal lines for wood grain
                alpha = random.uniform(0.1, 0.3)
                image[i:i+1, :] = cv2.addWeighted(
                    image[i:i+1, :], 1-alpha,
                    np.full_like(image[i:i+1, :], [139, 69, 19]), alpha, 0
                )
        elif texture_type == 'metal':
            # Add metallic sheen
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            image = cv2.filter2D(image, -1, kernel)

        return image

    def apply_domain_randomization(self, image):
        """Apply full domain randomization pipeline"""
        # Select random parameters
        lighting = random.choice(self.lighting_conditions)
        texture = random.choice(self.textures)
        noise_level = random.uniform(0.05, 0.15)

        # Apply transformations in sequence
        result = self.randomize_lighting(image.copy(), lighting)
        result = self.add_random_noise(result, noise_level)
        result = self.randomize_texture(result, texture)

        return result

class Sim2RealTransferTrainer:
    def __init__(self):
        self.domain_randomizer = DomainRandomizer()
        self.simulation_data = []
        self.real_data = []

    def generate_synthetic_dataset(self, base_images, num_samples=10000):
        """Generate large synthetic dataset with domain randomization"""
        synthetic_data = []

        for i in range(num_samples):
            # Select random base image
            base_img = random.choice(base_images)

            # Apply domain randomization
            randomized_img = self.domain_randomizer.apply_domain_randomization(base_img)

            # Generate corresponding labels (this would be more complex in practice)
            labels = self.generate_labels(randomized_img)

            synthetic_data.append({
                'image': randomized_img,
                'labels': labels,
                'domain_params': {
                    'lighting': random.choice(self.domain_randomizer.lighting_conditions),
                    'texture': random.choice(self.domain_randomizer.textures),
                    'noise': random.uniform(0.05, 0.15)
                }
            })

        return synthetic_data

    def generate_labels(self, image):
        """Generate labels for training (simplified)"""
        # In practice, this would involve complex labeling of objects,
        # segmentation masks, keypoints, etc.
        h, w = image.shape[:2]
        return {
            'object_bboxes': [],  # Bounding boxes of objects
            'segmentation_mask': np.zeros((h, w)),  # Segmentation mask
            'keypoints': [],  # Keypoints for pose estimation
            'depth_map': np.zeros((h, w))  # Depth information
        }

    def train_with_da(self, model, synthetic_data, real_data_ratio=0.1):
        """Train model with domain adaptation"""
        # Combine synthetic and real data
        combined_data = synthetic_data

        # Add small amount of real data for adaptation
        if real_data_ratio > 0 and len(self.real_data) > 0:
            num_real = int(len(synthetic_data) * real_data_ratio)
            real_subset = random.sample(self.real_data, min(num_real, len(self.real_data)))
            combined_data.extend(real_subset)

        # Shuffle the combined dataset
        random.shuffle(combined_data)

        # Train model on combined data
        # This is a simplified representation - actual implementation would depend on specific model
        print(f"Training with {len(combined_data)} samples ({len(synthetic_data)} synthetic, {len(combined_data) - len(synthetic_data)} real)")

        return model

# Example usage
def main():
    # Initialize the transfer trainer
    transfer_trainer = Sim2RealTransferTrainer()

    # Load base simulation images (these would come from your Gazebo/Unity simulation)
    # base_images = load_simulation_images()

    # Generate synthetic dataset
    # synthetic_dataset = transfer_trainer.generate_synthetic_dataset(base_images, num_samples=5000)

    # Train model with domain adaptation
    # trained_model = transfer_trainer.train_with_da(your_model, synthetic_dataset)

    print("Simulation-to-reality transfer pipeline initialized")

if __name__ == "__main__":
    main()
```

This comprehensive Digital Twin module covers advanced simulation techniques using both Gazebo and Unity, with detailed configurations for physics simulation, sensor modeling, and simulation-to-reality transfer techniques. The digital twin enables safe testing and training of humanoid robots in virtual environments, significantly reducing development time and costs while improving safety.