# Author: Zein Al-Haffei (https://github.com/ZeinHaffei)
# License: MIT


Background Subtraction and Movement-Triggered Recording Tool

A modular Python tool for **background subtraction, motion detection, and region-of-interest (ROI) selection** in video streams, camera feeds, or image sequences. Automatically records video segments only when significant movement is detected within a user-defined region.


Features

- Input flexibility: process video files, live camera feeds, or sequences of images.
- Multiple background subtraction algorithms: KNN, MOG, MOG2, GMG (OpenCV).
- Region of Interest (ROI): select interactively with mouse, or specify exact coordinates.
- Motion-triggered recording: saves video only when movement exceeds a threshold.
- Command-line interface: all options controllable via CLI arguments.
- Visual feedback: live display of input, ROI overlay, and movement mask.


Installation

1. Clone this repo:   
   git clone https://github.com/your-username/background-subtraction-roi.git
   cd background-subtraction-roi

2. Install dependencies:

   pip install -r requirements.txt

   or, if you use all background subtractors:
   
     pip install opencv-contrib-python numpy keyboard

Usage

Run from the command line:

  python ZoneWatch.py <input_type> <input_path> <subtractor_type> [--threshold INT] [--define_roi_manually | --roi_points X1 Y1 X2 Y2 ...]


Arguments
  1. input_type:

    video (video file)

    camera (live webcam, specify camera index, e.g., 0)

    image_sequence (folder of images)

  2.input_path:

    Path to video file, camera index, or image folder path

  3. subtractor_type:

    KNN, MOG, MOG2, or GMG

  4. --threshold (optional):

  5. Movement threshold (default: 10000)

  6. --define_roi_manually (optional):

    Select ROI using the mouse (press Enter to confirm)

  7. --roi_points (optional):

    Coordinates of ROI polygon (e.g. --roi_points 10 10 100 10 100 100 10 100)



Example Commands
  1. Video file, manual ROI:
     
     python your_script.py video path/to/video.mp4 KNN --define_roi_manually
  
  2. Live webcam, default settings:
       python your_script.py camera 0 MOG2

  3. Image sequence with explicit ROI:
     python your_script.py image_sequence path/to/images GMG --roi_points 50 50 200 50 200 200 50 200

Output
  1. Video segments are automatically saved (AVI format) when motion is detected within the ROI.
  2. Output files are named by timestamp (e.g., video_20250714_231512.avi).
  3. Live windows show the current frame, ROI, and motion mask.

Notes
  1. For image sequences, only .webp images are supported by default (you can easily modify this for other formats).
  2. The script requires Python 3.7+ and OpenCV with contrib modules for some subtractors.
  3. Press Esc to quit the live display at any time.





   
