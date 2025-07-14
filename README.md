# Author: Zein Al Haffei (https://github.com/ZeinHaffei)
# License: MIT

# ROI Motion Detector

A modular Python tool for **background subtraction, motion detection, and region-of-interest (ROI) selection** in video streams, camera feeds, or image sequences. Automatically records video segments only when significant movement is detected within a user-defined region.

---

## Features

- **Input flexibility**: process video files, live camera feeds, or sequences of images.
- **Multiple background subtraction algorithms**: KNN, MOG, MOG2, GMG (OpenCV).
- **Region of Interest (ROI)**: select interactively with mouse, or specify exact coordinates.
- **Motion-triggered recording**: saves video only when movement exceeds a threshold.
- **Command-line interface**: all options controllable via CLI arguments.
- **Visual feedback**: live display of input, ROI overlay, and movement mask.

---

## Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/your-username/roi-motion-detector.git
   cd roi-motion-detector
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   or, if you use all background subtractors:

   ```bash
   pip install opencv-contrib-python numpy keyboard
   ```

---

## Usage

Run from the command line:

```bash
python your_script.py <input_type> <input_path> <subtractor_type> [--threshold INT] [--define_roi_manually | --roi_points X1 Y1 X2 Y2 ...]
```

### **Arguments**

- `input_type`:
  - `video` (video file)
  - `camera` (live webcam, specify camera index, e.g., 0)
  - `image_sequence` (folder of images)
- `input_path`:
  - Path to video file, camera index, or image folder path
- `subtractor_type`:
  - `KNN`, `MOG`, `MOG2`, or `GMG`
- `--threshold` (optional):
  - Movement threshold (default: 10000)
- `--define_roi_manually` (optional):
  - Select ROI using the mouse (press Enter to confirm)
- `--roi_points` (optional):
  - Coordinates of ROI polygon (e.g. `--roi_points 10 10 100 10 100 100 10 100`)

---

### **Example Commands**

- **Video file, manual ROI:**

  ```bash
  python your_script.py video path/to/video.mp4 KNN --define_roi_manually
  ```

- **Live webcam, default settings:**

  ```bash
  python your_script.py camera 0 MOG2
  ```

- **Image sequence with explicit ROI:**

  ```bash
  python your_script.py image_sequence path/to/images GMG --roi_points 50 50 200 50 200 200 50 200
  ```

---

## Output

- Video segments are automatically saved (AVI format) when motion is detected within the ROI.
- Output files are named by timestamp (e.g., `video_20250714_231512.avi`).
- Live windows show the current frame, ROI, and motion mask.

---

## Notes

- For **image sequences**, only `.webp` images are supported by default (you can easily modify this for other formats).
- The script requires Python 3.7+ and OpenCV with contrib modules for some subtractors.
- Press `Esc` to quit the live display at any time.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

- [Zein AL Haffei](https://github.com/ZeinHaffei)

---

**Feel free to open issues or contribute!**

