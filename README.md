# AI Hand Gesture Virtual Mouse & Controller 🖱️✋

An AI-driven Human-Computer Interaction (HCI) system that transforms any standard webcam or smartphone camera into a touchless, high-precision desktop mouse. Built using **OpenCV**, **Google MediaPipe**, and **PyAutoGUI**.

---

## 📌 Overview

This project replaces physical input hardware by tracking 21 3D hand keypoints in real time. It uses geometric vector interpolation, exponential smoothing filters, and discrete state machines to deliver low-latency cursor movement, single/double clicks, drag-and-drop operations, and vertical scrolling.

---

## ✨ Features

- **Real-Time Landmark Regression**: Powered by MediaPipe's lightweight two-stage pipeline running on CPU without dedicated GPU hardware.
- **Micro-Jitter Suppression**: Implements coordinate interpolation and moving-average smoothing to prevent camera hand-shake.
- **Bounding Box Interpolation**: Maps an interior active region to full display dimensions, allowing seamless edge-to-edge navigation.
- **Intuitive Gesture Control**:
  - 👆 **Cursor Move**: Direct tracking mapped to index fingertip coordinates.
  - 🤏 **Left Click**: Quick thumb + index pinch.
  - ✊ **Drag & Drop**: Thumb + pinky pinch lock with continuous dragging across windows and files.
  - 🖐️ **Vertical Scroll**: 4-finger open hand mode with dynamic up/down boundary detection.
- **IP Webcam Support**: Compatible with mobile network video streams (`http://<ip>:8080/video`) for wireless operation.

---

## 🖐️ Gesture Reference Guide

| Gesture | Action | Trigger Criteria |
| :--- | :--- | :--- |
| **Index Fingertip Point** | Cursor Movement | Index finger extended within active bounding box |
| **Thumb + Index Pinch** | Left Click | Euclidean distance between Landmark 4 & 8 < `0.05` |
| **Thumb + Pinky Pinch (Hold)**| Drag & Drop | Landmark 4 & 20 proximity lock (`mouseDown` → `mouseUp`) |
| **Four Fingers Extended (Up/Down)** | Page Scroll | All non-thumb fingers open + vertical thresholding |

---

## 🛠️ Tech Stack & Dependencies

- **Python 3.10 / 3.11**
- **OpenCV (`opencv-python`)**: Video ingestion, color space conversion, and HUD drawing.
- **Google MediaPipe (`mediapipe<0.10.15`)**: 21 3D hand keypoint extraction.
- **PyAutoGUI**: Native OS cursor event triggering.
- **NumPy**: Vector distance calculations and screen dimension linear interpolation.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/rafi_hand_mouse_controller.git](https://github.com/YourUsername/rafi_hand_mouse_controller.git)
cd rafi_hand_mouse_controller
