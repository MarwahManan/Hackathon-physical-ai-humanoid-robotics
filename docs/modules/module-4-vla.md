---
sidebar_position: 5
title: Module 4 - Vision-Language-Action (VLA)
---

# Module 4: Vision-Language-Action (VLA)

## Focus: The convergence of LLMs and Robotics

Vision-Language-Action (VLA) systems represent the cutting edge of embodied AI, enabling robots to understand and execute natural language commands in physical environments. This integration of perception, language, and action creates truly interactive humanoid robots.

## Vision-Language Integration in Robotics

VLA systems combine three critical components:

### Vision Processing
- **Object Recognition**: Identifying and localizing objects in the environment
- **Scene Understanding**: Comprehending spatial relationships and context
- **Visual Tracking**: Following objects and people through space and time
- **Depth Perception**: Understanding 3D structure for manipulation and navigation

### Language Understanding
- **Natural Language Processing**: Interpreting human commands and queries
- **Semantic Mapping**: Connecting linguistic concepts to physical entities
- **Context Awareness**: Understanding commands in environmental context
- **Dialogue Management**: Handling multi-turn conversations with humans

### Action Execution
- **Task Planning**: Breaking down high-level commands into executable steps
- **Motion Planning**: Generating safe and efficient movement trajectories
- **Manipulation Control**: Executing precise object interactions
- **Feedback Integration**: Adapting to environmental changes and failures

## Voice-to-Action Pipeline Implementation

### Speech Recognition with OpenAI Whisper

Advanced speech recognition for humanoid robots requires robust performance in real-world environments:

```python
import rclpy
from rclpy.node import Node
import whisper
import speech_recognition as sr
import numpy as np
import threading
import queue
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped

class AdvancedVoiceCommandNode(Node):
    def __init__(self):
        super().__init__('advanced_voice_command_node')

        # Publishers
        self.command_pub = self.create_publisher(String, '/voice_command', 10)
        self.interaction_status_pub = self.create_publisher(Bool, '/interaction_active', 10)
        self.command_pose_pub = self.create_publisher(PoseStamped, '/commander_location', 10)

        # Parameters
        self.declare_parameter('whisper_model', 'base')
        self.declare_parameter('wake_word', 'robot')
        self.declare_parameter('confidence_threshold', 0.7)

        # Initialize components
        model_name = self.get_parameter('whisper_model').get_parameter_value().string_value
        self.whisper_model = whisper.load_model(model_name)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Configuration
        self.wake_word = self.get_parameter('wake_word').get_parameter_value().string_value
        self.confidence_threshold = self.get_parameter('confidence_threshold').get_parameter_value().double_value

        # Audio processing queue
        self.audio_queue = queue.Queue()

        # Setup microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        # Start listening thread
        self.listening_thread = threading.Thread(target=self.listen_continuously, daemon=True)
        self.listening_thread.start()

        self.get_logger().info(f"Advanced voice command system initialized with wake word: '{self.wake_word}'")

    def listen_continuously(self):
        """Continuously listen for voice commands"""
        while rclpy.ok():
            try:
                with self.microphone as source:
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=1.0, phrase_time_limit=5.0)

                    # Convert to format for Whisper
                    audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)

                    # Process with Whisper
                    result = self.whisper_model.transcribe(audio_data.astype(np.float32) / 32768.0)
                    command_text = result["text"].strip()

                    if command_text:
                        # Check for wake word if needed
                        if self.wake_word.lower() in command_text.lower():
                            # Extract actual command (remove wake word)
                            actual_command = command_text.lower().replace(self.wake_word.lower(), "").strip()
                            if actual_command:
                                self.process_command(actual_command)
                        elif not self.wake_word:  # If no wake word required
                            self.process_command(command_text)

            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                continue
            except Exception as e:
                self.get_logger().error(f"Audio processing error: {e}")
                continue

    def process_command(self, command_text):
        """Process and publish the recognized command"""
        # Publish the recognized command
        cmd_msg = String()
        cmd_msg.data = command_text
        self.command_pub.publish(cmd_msg)

        # Publish interaction status
        status_msg = Bool()
        status_msg.data = True
        self.interaction_status_pub.publish(status_msg)

        self.get_logger().info(f"Voice command received: '{command_text}'")

        # Reset interaction status after delay
        timer = self.create_timer(5.0, lambda: self.reset_interaction_status())

    def reset_interaction_status(self):
        """Reset the interaction status after command processing"""
        status_msg = Bool()
        status_msg.data = False
        self.interaction_status_pub.publish(status_msg)

def main():
    rclpy.init()
    node = AdvancedVoiceCommandNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### Audio Enhancement for Robot Environments

Robots often operate in noisy environments, requiring specialized audio processing:

```python
import pyaudio
import webrtcvad
import collections
import numpy as np
from scipy import signal

class RobotAudioProcessor:
    def __init__(self, sample_rate=16000, frame_duration=30):
        self.sample_rate = sample_rate
        self.frame_duration = frame_duration
        self.frame_size = int(sample_rate * frame_duration / 1000)

        # Voice activity detection
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2

        # Audio buffers
        self.ring_buffer = collections.deque(maxlen=30)
        self.speech_buffer = []

        # Noise reduction parameters
        self.noise_threshold = 0.01

    def apply_noise_reduction(self, audio_data):
        """Apply noise reduction to audio signal"""
        # Simple spectral subtraction for noise reduction
        fft_data = np.fft.fft(audio_data)
        magnitude = np.abs(fft_data)
        phase = np.angle(fft_data)

        # Estimate noise floor
        noise_floor = np.mean(magnitude) * self.noise_threshold

        # Subtract noise
        enhanced_magnitude = np.maximum(magnitude - noise_floor, 0)

        # Reconstruct signal
        enhanced_fft = enhanced_magnitude * np.exp(1j * phase)
        enhanced_audio = np.real(np.fft.ifft(enhanced_fft))

        return enhanced_audio.astype(np.int16)

    def detect_voice_activity(self, audio_frame):
        """Detect voice activity in audio frame"""
        try:
            return self.vad.is_speech(audio_frame.tobytes(), self.sample_rate)
        except:
            return False
```

## Cognitive Planning with Large Language Models

### Advanced Task Planning System

```python
import openai
import json
import time
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class TaskStep:
    action: str
    parameters: Dict[str, Any]
    priority: int = 0
    dependencies: List[str] = None
    estimated_duration: float = 0.0  # in seconds

class AdvancedCognitivePlanner:
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

        # Robot capabilities database
        self.robot_capabilities = {
            "navigation": ["navigate_to", "move_to", "go_to"],
            "manipulation": ["grasp_object", "pick_up", "place_object", "put_down"],
            "perception": ["detect_object", "find_object", "identify_object"],
            "communication": ["speak", "say", "communicate"],
            "interaction": ["greet", "hand_over", "assist"]
        }

        # Environment knowledge
        self.environment_map = {
            "locations": ["kitchen", "living_room", "bedroom", "office", "dining_room", "bathroom"],
            "objects": ["cup", "bottle", "book", "phone", "keys", "food", "water"],
            "people": ["person", "human", "user", "owner"]
        }

    def plan_from_command(self, natural_language_command: str) -> List[TaskStep]:
        """Generate detailed task plan from natural language command"""
        prompt = self._create_planning_prompt(natural_language_command)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000
            )

            response_text = response.choices[0].message.content
            plan_data = self._extract_json_from_response(response_text)

            if plan_data and "actions" in plan_data:
                return self._convert_to_task_steps(plan_data["actions"])
            else:
                return self._fallback_plan(natural_language_command)

        except Exception as e:
            self.get_logger().error(f"Planning error: {e}")
            return self._fallback_plan(natural_language_command)

    def _create_planning_prompt(self, command: str) -> str:
        """Create detailed prompt for task planning"""
        return f"""
        You are an advanced robotic task planner for a humanoid robot. Your role is to decompose natural language commands into detailed, executable action sequences.

        Context:
        - Robot capabilities: {self.robot_capabilities}
        - Environment locations: {self.environment_map['locations']}
        - Common objects: {self.environment_map['objects']}
        - Available sensors: cameras, LIDAR, IMU, touch sensors
        - Available actuators: arms, legs, head, torso, grippers

        Command: "{command}"

        Requirements:
        1. Break down the command into specific, executable actions
        2. Consider spatial relationships and object properties
        3. Account for robot kinematics and workspace limitations
        4. Include error handling and fallback strategies
        5. Specify required parameters for each action

        Actions should be from this list with appropriate parameters:
        - navigate_to(location, approach_angle=None, speed="normal")
        - detect_object(object_type, search_area="default", max_attempts=3)
        - grasp_object(object_id, grasp_type="default", force=50)
        - place_object(location, placement_type="surface", orientation="default")
        - speak(text, language="en", speed=1.0)
        - look_at(target, duration=2.0)
        - wait(duration)
        - ask_for_clarification(question, options=None)
        - report_status(message, status_type="info")

        Return the plan as valid JSON with this structure:
        {{
            "actions": [
                {{
                    "action": "action_name",
                    "parameters": {{
                        "param1": "value1",
                        "param2": "value2"
                    }},
                    "priority": 0,
                    "estimated_duration": 5.0,
                    "dependencies": ["action_id_1", "action_id_2"]
                }}
            ],
            "metadata": {{
                "confidence": 0.8,
                "complexity": "medium",
                "estimated_total_time": 60.0
            }}
        }}

        Example for "Bring me the red cup from the kitchen":
        {{
            "actions": [
                {{
                    "action": "navigate_to",
                    "parameters": {{"location": "kitchen"}},
                    "priority": 1,
                    "estimated_duration": 15.0
                }},
                {{
                    "action": "detect_object",
                    "parameters": {{"object_type": "red cup", "search_area": "countertops"}},
                    "priority": 2,
                    "estimated_duration": 10.0,
                    "dependencies": ["navigate_to"]
                }},
                {{
                    "action": "grasp_object",
                    "parameters": {{"object_id": "red_cup_1", "grasp_type": "top_grasp"}},
                    "priority": 3,
                    "estimated_duration": 5.0,
                    "dependencies": ["detect_object"]
                }},
                {{
                    "action": "navigate_to",
                    "parameters": {{"location": "user_location"}},
                    "priority": 4,
                    "estimated_duration": 20.0,
                    "dependencies": ["grasp_object"]
                }},
                {{
                    "action": "place_object",
                    "parameters": {{"location": "near_user", "placement_type": "handover"}},
                    "priority": 5,
                    "estimated_duration": 5.0,
                    "dependencies": ["navigate_to"]
                }}
            ],
            "metadata": {{
                "confidence": 0.9,
                "complexity": "medium",
                "estimated_total_time": 55.0
            }}
        }}
        """

    def _extract_json_from_response(self, response_text: str) -> Dict:
        """Extract JSON from LLM response"""
        try:
            # Find JSON within triple backticks or plain JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return None

    def _convert_to_task_steps(self, action_list: List[Dict]) -> List[TaskStep]:
        """Convert action list to TaskStep objects"""
        task_steps = []
        for action in action_list:
            step = TaskStep(
                action=action.get("action", ""),
                parameters=action.get("parameters", {}),
                priority=action.get("priority", 0),
                dependencies=action.get("dependencies", []),
                estimated_duration=action.get("estimated_duration", 0.0)
            )
            task_steps.append(step)
        return task_steps

    def _fallback_plan(self, command: str) -> List[TaskStep]:
        """Create a simple fallback plan if LLM fails"""
        # Simple fallback based on keywords
        command_lower = command.lower()

        if any(word in command_lower for word in ["bring", "get", "fetch", "pick up"]):
            return [
                TaskStep(action="ask_for_clarification",
                        parameters={"question": f"What would you like me to {command.split()[0]}?"}),
            ]
        elif any(word in command_lower for word in ["go", "move", "navigate"]):
            return [
                TaskStep(action="ask_for_clarification",
                        parameters={"question": "Where would you like me to go?"}),
            ]
        else:
            return [
                TaskStep(action="speak",
                        parameters={"text": f"I'm not sure how to '{command}'. Can you rephrase?"}),
            ]

    def validate_plan(self, plan: List[TaskStep], environment_state: Dict) -> bool:
        """Validate plan against current environment state"""
        # Check if required objects/locations are available
        for step in plan:
            if step.action == "navigate_to":
                location = step.parameters.get("location", "")
                if location not in environment_state.get("accessible_locations", []):
                    return False
            elif step.action == "detect_object":
                obj_type = step.parameters.get("object_type", "")
                if obj_type not in environment_state.get("detectable_objects", []):
                    return False
        return True
```

### Multi-Modal Perception Integration

```python
import cv2
import numpy as np
import torch
from transformers import pipeline
from ultralytics import YOLO

class MultiModalPerception:
    def __init__(self):
        # Object detection model
        self.object_detector = YOLO('yolov8x.pt')

        # Visual question answering
        self.vqa_pipeline = pipeline("visual-question-answering",
                                    model="dandelin/vilt-b32-finetuned-vqa")

        # CLIP for zero-shot classification
        self.clip_model = torch.hub.load('openai/clip:main', 'clip', name='ViT-B/32')

        # Scene understanding
        self.scene_classifier = pipeline("image-classification",
                                        model="facebook/dino-vits8")

    def analyze_scene(self, image: np.ndarray) -> Dict:
        """Analyze the current scene with multiple perception modalities"""
        results = {}

        # Object detection
        detection_results = self.object_detector(image)
        objects = []
        for detection in detection_results[0].boxes:
            obj_info = {
                'class': detection_results[0].names[int(detection.cls)],
                'confidence': float(detection.conf),
                'bbox': detection.xyxy[0].tolist(),
                'center': [(detection.xyxy[0][0] + detection.xyxy[0][2]) / 2,
                          (detection.xyxy[0][1] + detection.xyxy[0][3]) / 2]
            }
            objects.append(obj_info)

        results['objects'] = objects

        # Scene classification
        scene_result = self.scene_classifier(image)
        results['scene'] = scene_result[0]['label']
        results['scene_confidence'] = scene_result[0]['score']

        # Spatial relationships
        results['spatial_relationships'] = self._analyze_spatial_relationships(objects)

        return results

    def _analyze_spatial_relationships(self, objects: List[Dict]) -> List[Dict]:
        """Analyze spatial relationships between detected objects"""
        relationships = []

        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i != j:
                    # Calculate spatial relationship
                    center1 = obj1['center']
                    center2 = obj2['center']

                    dx = center2[0] - center1[0]
                    dy = center2[1] - center1[1]

                    distance = np.sqrt(dx*dx + dy*dy)

                    # Determine direction
                    if abs(dx) > abs(dy):
                        direction = "left" if dx < 0 else "right"
                    else:
                        direction = "above" if dy < 0 else "below"

                    relationship = {
                        'subject': obj1['class'],
                        'relation': direction,
                        'object': obj2['class'],
                        'distance': float(distance),
                        'confidence': min(obj1['confidence'], obj2['confidence'])
                    }

                    relationships.append(relationship)

        return relationships

    def answer_visual_question(self, image: np.ndarray, question: str) -> str:
        """Answer questions about the visual scene"""
        inputs = {
            "image": image,
            "question": question
        }

        answer = self.vqa_pipeline(inputs)
        return answer[0]['answer']
```

## Integration with ROS 2 Execution Framework

### Action Execution Manager

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from action_msgs.msg import GoalStatus

from robot_controllers_msgs.action import FollowJointTrajectory
from nav2_msgs.action import NavigateToPose
from manipulation_msgs.action import GraspObject

class ActionExecutionManager(Node):
    def __init__(self):
        super().__init__('action_execution_manager')

        # Action clients
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.manipulation_client = ActionClient(self, GraspObject, 'grasp_object')
        self.trajectory_client = ActionClient(self, FollowJointTrajectory, 'follow_joint_trajectory')

        # Publishers
        self.status_pub = self.create_publisher(String, '/task_status', 10)
        self.feedback_pub = self.create_publisher(String, '/task_feedback', 10)

        # Task queue
        self.task_queue = []
        self.current_task = None

        # Timer for task execution
        self.task_timer = self.create_timer(0.1, self.execute_next_task)

        self.get_logger().info("Action execution manager initialized")

    def execute_task_sequence(self, task_steps: List[TaskStep]):
        """Execute a sequence of tasks"""
        self.task_queue.extend(task_steps)
        self.get_logger().info(f"Added {len(task_steps)} tasks to execution queue")

    def execute_next_task(self):
        """Execute the next task in the queue"""
        if not self.task_queue or self.current_task is not None:
            return

        task = self.task_queue.pop(0)
        self.current_task = task

        # Update status
        status_msg = String()
        status_msg.data = f"Executing: {task.action}"
        self.status_pub.publish(status_msg)

        # Execute based on task type
        if task.action == "navigate_to":
            self._execute_navigation(task)
        elif task.action == "grasp_object":
            self._execute_grasp(task)
        elif task.action == "speak":
            self._execute_speech(task)
        else:
            self._execute_generic_action(task)

    def _execute_navigation(self, task: TaskStep):
        """Execute navigation task"""
        goal_msg = NavigateToPose.Goal()

        # Set target pose
        location = task.parameters.get("location", "")
        target_pose = self._get_pose_for_location(location)
        goal_msg.pose = target_pose

        # Send goal
        self.nav_client.wait_for_server()
        future = self.nav_client.send_goal_async(goal_msg)
        future.add_done_callback(self._navigation_callback)

    def _execute_grasp(self, task: TaskStep):
        """Execute grasping task"""
        goal_msg = GraspObject.Goal()

        # Set object and grasp parameters
        goal_msg.object_id = task.parameters.get("object_id", "")
        goal_msg.grasp_type = task.parameters.get("grasp_type", "default")
        goal_msg.force = task.parameters.get("force", 50.0)

        # Send goal
        self.manipulation_client.wait_for_server()
        future = self.manipulation_client.send_goal_async(goal_msg)
        future.add_done_callback(self._grasp_callback)

    def _navigation_callback(self, future):
        """Handle navigation result"""
        goal_handle = future.result()
        if goal_handle.accepted:
            self.get_logger().info("Navigation goal accepted")
            # Wait for result
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self._navigation_result_callback)

    def _navigation_result_callback(self, future):
        """Handle navigation result"""
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Navigation succeeded")
            self._task_completed()
        else:
            self.get_logger().error("Navigation failed")
            self._task_failed()

    def _task_completed(self):
        """Handle task completion"""
        self.current_task = None
        feedback_msg = String()
        feedback_msg.data = "Task completed successfully"
        self.feedback_pub.publish(feedback_msg)

    def _task_failed(self):
        """Handle task failure"""
        self.current_task = None
        feedback_msg = String()
        feedback_msg.data = "Task failed"
        self.feedback_pub.publish(feedback_msg)
```

## Capstone Project: The Autonomous Humanoid System

The complete integrated system combines all modules into a cohesive autonomous humanoid:

```python
class AutonomousHumanoidSystem(Node):
    def __init__(self):
        super().__init__('autonomous_humanoid')

        # Initialize all subsystems
        self.voice_node = AdvancedVoiceCommandNode()
        self.cognitive_planner = AdvancedCognitivePlanner(api_key="your-api-key")
        self.perception_system = MultiModalPerception()
        self.action_manager = ActionExecutionManager()

        # Environment state tracker
        self.environment_state = {
            "objects": [],
            "locations": [],
            "people": [],
            "robot_pose": None,
            "accessible_locations": []
        }

        # Subscribe to environment updates
        self.environment_sub = self.create_subscription(
            String, '/environment_update', self.environment_callback, 10)

        self.get_logger().info("Autonomous Humanoid System initialized")

    def process_command(self, command: str):
        """Process a complete command through all subsystems"""
        # 1. Update environment state
        self._update_environment()

        # 2. Generate plan using LLM
        task_plan = self.cognitive_planner.plan_from_command(command)

        # 3. Validate plan against environment
        if self.cognitive_planner.validate_plan(task_plan, self.environment_state):
            # 4. Execute the plan
            self.action_manager.execute_task_sequence(task_plan)
        else:
            # 5. Request clarification or alternative
            self._request_clarification(command)

    def _update_environment(self):
        """Update environment state from perception systems"""
        # This would integrate with perception nodes
        # to update the current state of the world
        pass

    def _request_clarification(self, command: str):
        """Request clarification when plan is invalid"""
        clarification = f"I'm not sure how to execute '{command}'. Could you provide more details?"
        self.voice_node.speak(clarification)

def main():
    rclpy.init()
    system = AutonomousHumanoidSystem()

    try:
        rclpy.spin(system)
    except KeyboardInterrupt:
        pass
    finally:
        system.destroy_node()
        rclpy.shutdown()
```

This comprehensive Vision-Language-Action system enables humanoid robots to understand natural language commands, perceive their environment, plan complex tasks, and execute them safely in the physical world. The integration of multiple AI technologies creates a truly autonomous robotic system capable of natural human interaction.