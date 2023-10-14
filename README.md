# Object_detection_cv2
# Object Detection using OpenCV and Pre-trained Model

Welcome to the Object Detection project! This repository contains a Python script `detector.py` that performs real-time object detection using OpenCV and a pre-trained model on the COCO dataset.

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)

## Introduction
The `detector.py` script demonstrates real-time object detection using the OpenCV library and a pre-trained model from the COCO dataset. This script takes input from a video source (camera or file) and overlays bounding boxes and labels on detected objects.

## Getting Started
### Prerequisites
- Python 3.10
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)

### Installation
1. Clone the repository: `git clone https://github.com/Praveenbabloo/Object_detection_cv2.git`
2. Navigate to the project directory: `cd #repo`

## Usage
1. Make sure you have a video file or a camera connected for real-time detection.
2. Update the paths in `main.py` for `configPath`, `modelPath`, and `classesPath` to point to the relevant model and class files.
3. Run the main script: `python main.py`
4. Press the 'q' key to exit the detection window.
  
## Contributing
Contributions are welcome! If you'd like to add improvements, please fork the repository and create a pull request.


