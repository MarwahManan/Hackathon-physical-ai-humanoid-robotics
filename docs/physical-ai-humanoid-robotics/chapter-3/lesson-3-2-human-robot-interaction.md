---
title: Human-Robot Interaction
sidebar_label: "Lesson 3.2: Human-Robot Interaction"
sidebar_position: 2
description: Designing effective interfaces and interaction paradigms for humanoid robots
keywords: [human-robot-interaction, hri, social-robotics, interaction-design]
---

# Human-Robot Interaction

## Introduction

This lesson explores the principles and techniques for designing effective interactions between humans and humanoid robots. Human-Robot Interaction (HRI) is crucial for creating robots that can work alongside humans in various environments, from homes to workplaces.

### Learning Objectives

- Understand the principles of effective human-robot interaction
- Learn about communication modalities (speech, gesture, gaze)
- Explore social robotics concepts and design principles
- Know how to implement basic HRI systems

### Prerequisites

- Understanding of perception systems (from Chapter 2)
- Basic knowledge of user interface design concepts

### Estimated Time

50 minutes

## Core Concepts

Human-Robot Interaction encompasses all aspects of how humans and robots communicate, collaborate, and work together. Effective HRI design is essential for humanoid robots to be accepted and useful in human environments.

![Human-Robot Interaction](/img/hri-concept.svg)

### Communication Modalities

#### Speech Interaction
- **Natural Language Processing**: Understanding human speech
- **Speech Synthesis**: Generating natural robot speech
- **Dialogue Management**: Maintaining coherent conversations

#### Non-Verbal Communication
- **Gestures**: Hand and body movements for communication
- **Gaze**: Eye contact and attention direction
- **Facial Expressions**: Conveying emotions and intentions
- **Proxemics**: Managing personal space and distance

#### Multimodal Interaction
- **Fusion of modalities**: Combining speech, gesture, and other inputs
- **Context awareness**: Understanding interaction context
- **Adaptive interfaces**: Adjusting to user preferences and abilities

### Social Robotics Principles

#### Anthropomorphism
- **Appropriate design**: Human-like features where beneficial
- **Uncanny valley**: Avoiding unsettling robot appearances
- **Social cues**: Using human social signals appropriately

#### Trust and Acceptance
- **Transparency**: Making robot intentions clear
- **Predictability**: Consistent and reliable behavior
- **Safety**: Ensuring physical and psychological safety

### HRI Challenges

Human-robot interaction faces several unique challenges:
- **Cultural differences**: Varying social norms across cultures
- **Individual differences**: Adapting to different users
- **Context sensitivity**: Understanding situational appropriateness
- **Privacy concerns**: Managing personal data and interactions

## Code Implementation

```python
# Example code demonstrating Human-Robot Interaction systems
import numpy as np
import speech_recognition as sr
import pyttsx3
import cv2
import mediapipe as mp
from dataclasses import dataclass
from typing import Optional, List, Dict
import time
import threading
import queue

@dataclass
class UserIntent:
    """Represents user intent parsed from interaction"""
    action: str
    target: Optional[str] = None
    parameters: Dict[str, str] = None

@dataclass
class InteractionContext:
    """Maintains context of the interaction"""
    conversation_history: List[str]
    user_attention: bool  # Is user paying attention to robot?
    interaction_mode: str  # 'collaborative', 'assistant', 'companion'
    last_interaction_time: float

class SpeechProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()

        # Configure TTS engine
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level

        # Simple intent recognition patterns
        self.intent_patterns = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'command': ['please', 'can you', 'could you', 'help me', 'assist'],
            'navigation': ['go to', 'move to', 'navigate to', 'walk to'],
            'object_interaction': ['pick up', 'grasp', 'take', 'get', 'bring'],
            'question': ['what', 'where', 'when', 'how', 'why', 'can', 'do']
        }

    def listen(self) -> Optional[str]:
        """Listen for user speech and return recognized text"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)

            text = self.recognizer.recognize_google(audio).lower()
            print(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

    def speak(self, text: str):
        """Speak text using TTS"""
        print(f"Robot says: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def parse_intent(self, text: str) -> UserIntent:
        """Parse user intent from speech"""
        text_lower = text.lower()

        # Simple pattern matching for intent recognition
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return UserIntent(action=intent_type, target=None)

        # Default to general conversation
        return UserIntent(action='conversation', target=text)

class GestureProcessor:
    def __init__(self):
        # Initialize MediaPipe for gesture recognition
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_gestures(self, frame):
        """Detect hand gestures in the frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        gestures = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = self._analyze_hand_pose(hand_landmarks)
                gestures.append(gesture)

                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return gestures, frame

    def _analyze_hand_pose(self, landmarks):
        """Analyze hand pose to determine gesture"""
        # Get key landmark positions
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

        # Simple gesture recognition
        if self._is_fist(landmarks):
            return "fist"
        elif self._is_open_palm(landmarks):
            return "open_palm"
        elif self._is_pointing(landmarks):
            return "pointing"
        elif self._is_victory(landmarks):
            return "victory"
        else:
            return "unknown"

    def _is_fist(self, landmarks):
        """Check if hand is in fist position"""
        # Check if fingertips are close to palm
        wrist = landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Calculate distances
        thumb_to_wrist = self._distance(thumb_tip, wrist)
        index_to_wrist = self._distance(index_tip, wrist)

        return thumb_to_wrist < 0.1 and index_to_wrist < 0.1

    def _is_open_palm(self, landmarks):
        """Check if hand is in open palm position"""
        # Check if all fingers are extended
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_pip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        wrist = landmarks.landmark[self.mp_hands.HandLandmark.WRIST]

        # Calculate if finger tip is far from base
        index_to_wrist = self._distance(index_tip, wrist)
        index_pip_to_wrist = self._distance(index_pip, wrist)

        return index_to_wrist > index_pip_to_wrist * 1.5

    def _is_pointing(self, landmarks):
        """Check if hand is pointing"""
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        index_pip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]

        # Index finger extended, others curled
        index_to_pip = self._distance(index_tip, index_pip)
        middle_to_pip = self._distance(middle_tip, index_pip)

        return index_to_pip > middle_to_pip * 1.5

    def _is_victory(self, landmarks):
        """Check if hand is in victory sign"""
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]

        # Index and middle extended, others curled
        return (self._distance(index_tip, landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) >
                self._distance(ring_tip, landmarks.landmark[self.mp_hands.HandLandmark.WRIST]) * 1.2)

    def _distance(self, point1, point2):
        """Calculate distance between two landmarks"""
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

class AttentionDetector:
    def __init__(self):
        # Initialize face detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_attention(self, frame):
        """Detect if user is paying attention to the robot"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape

                # Check if face is centered (rough attention check)
                center_x = bbox.xmin + bbox.width / 2
                center_y = bbox.ymin + bbox.height / 2

                # Consider attentive if face is in center region (simplified)
                is_attentive = (0.3 < center_x < 0.7) and (0.3 < center_y < 0.7)

                # Draw bounding box
                self.mp_drawing.draw_detection(frame, detection)

                return is_attentive, frame

        return False, frame

class SocialRobot:
    def __init__(self):
        self.speech_processor = SpeechProcessor()
        self.gesture_processor = GestureProcessor()
        self.attention_detector = AttentionDetector()

        # Interaction context
        self.context = InteractionContext(
            conversation_history=[],
            user_attention=False,
            interaction_mode='assistant',
            last_interaction_time=time.time()
        )

        # Robot state
        self.is_interacting = False
        self.user_name = "User"

    def start_interaction_loop(self):
        """Start the main interaction loop"""
        print("Starting Human-Robot Interaction system...")

        # Start camera for gesture and attention detection
        cap = cv2.VideoCapture(0)

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue

                # Process gestures
                gestures, frame = self.gesture_processor.detect_gestures(frame)

                # Detect attention
                is_attentive, frame = self.attention_detector.detect_attention(frame)
                self.context.user_attention = is_attentive

                # Show camera feed
                cv2.imshow('HRI System', frame)

                # Check for speech input periodically
                if not self.is_interacting:
                    speech = self.speech_processor.listen()
                    if speech:
                        self.process_speech_input(speech)

                # Handle keyboard input to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

    def process_speech_input(self, speech: str):
        """Process user speech input"""
        self.is_interacting = True

        # Parse intent from speech
        intent = self.speech_processor.parse_intent(speech)

        # Update context
        self.context.conversation_history.append(f"User: {speech}")
        self.context.last_interaction_time = time.time()

        # Generate response based on intent
        response = self.generate_response(intent, speech)

        # Add to conversation history
        self.context.conversation_history.append(f"Robot: {response}")

        # Speak response
        self.speech_processor.speak(response)

        self.is_interacting = False

    def generate_response(self, intent: UserIntent, original_text: str) -> str:
        """Generate appropriate response based on intent"""
        if intent.action == 'greeting':
            return f"Hello {self.user_name}! How can I assist you today?"
        elif intent.action == 'question':
            return "I'm here to help. Could you please specify what you need assistance with?"
        elif intent.action == 'command':
            return "I understand you need help. Could you be more specific about what you'd like me to do?"
        elif intent.action == 'conversation':
            return f"I heard you say: '{original_text}'. How can I help you with this?"
        else:
            return "I understand. How can I assist you further?"

    def respond_to_gesture(self, gesture: str):
        """Respond to detected gesture"""
        responses = {
            'fist': "I see you made a fist gesture.",
            'open_palm': "Open palm detected. Hello!",
            'pointing': f"I see you're pointing. How can I help?",
            'victory': "Nice victory sign! Is there something positive I can help with?"
        }

        response = responses.get(gesture, "I detected a gesture but I'm not sure what it means.")
        self.speech_processor.speak(response)

# Example usage and simulation
class HRIExample:
    def __init__(self):
        self.robot = SocialRobot()

    def simulate_interaction(self):
        """Simulate a simple interaction without actual hardware"""
        print("=== Human-Robot Interaction Simulation ===")

        # Simulate various interaction scenarios
        test_inputs = [
            "Hello robot",
            "Can you help me?",
            "What time is it?",
            "Please move to the kitchen"
        ]

        for user_input in test_inputs:
            print(f"\nUser says: {user_input}")

            # Parse intent
            intent = self.robot.speech_processor.parse_intent(user_input)
            print(f"Detected intent: {intent.action}")

            # Generate and show response
            response = self.robot.generate_response(intent, user_input)
            print(f"Robot responds: {response}")

            # Update context
            self.robot.context.conversation_history.append(f"User: {user_input}")
            self.robot.context.conversation_history.append(f"Robot: {response}")
            self.robot.context.last_interaction_time = time.time()

            time.sleep(1)  # Simulate processing time

    def demonstrate_gesture_response(self):
        """Demonstrate gesture processing"""
        print("\n=== Gesture Processing Demo ===")

        test_gestures = ['pointing', 'open_palm', 'victory', 'fist']

        for gesture in test_gestures:
            print(f"Detected gesture: {gesture}")
            self.robot.respond_to_gesture(gesture)
            time.sleep(1)

# Example usage
if __name__ == "__main__":
    hri_example = HRIExample()

    print("Physical AI & Humanoid Robotics - Human-Robot Interaction")
    print("=" * 60)

    # Run simulation
    hri_example.simulate_interaction()

    # Demonstrate gesture processing
    hri_example.demonstrate_gesture_response()

    print("\nInteraction simulation completed!")
    print(f"Final conversation history has {len(hri_example.robot.context.conversation_history)} exchanges")
    print(f"Current interaction mode: {hri_example.robot.context.interaction_mode}")
    print(f"Last interaction: {time.time() - hri_example.robot.context.last_interaction_time:.2f} seconds ago")