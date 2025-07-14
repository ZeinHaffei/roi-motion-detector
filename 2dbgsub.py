import os
from datetime import datetime

import cv2
import numpy as np
import keyboard

from collections import deque


class VideoProcessor:
    def __init__(self, input_type, input_path, subtractor_type, threshold, define_roi_manually, roi_points=None):
        self.input_type = input_type
        self.input_path = input_path  # 'video' 'camera' or 'image_sequence'
        self.subtractor_type = subtractor_type
        self.threshold = threshold
        self.define_roi_manually = define_roi_manually
        self.roi_points = roi_points if roi_points else []  # Initialize roi_points as an empty list
        self.mask_template = None

        if self.input_type == 'video':
            self.cap = cv2.VideoCapture(input_path)

        elif self.input_type == 'camera':
            self.cap = cv2.VideoCapture(int(input_path))

        elif self.input_type == 'image_sequence':
            self.image_files = [os.path.join(input_path, file) for file in os.listdir(input_path) if
                                file.endswith(".webp")]
            self.image_files.sort()

            if len(self.image_files) == 0:
                print("No image files found in the folder.")
                exit()
            else:
                self.current_image = 0
                self.cap = cv2.imread(self.image_files[self.current_image])
            # self.frame_iterator = iter(self.image_files)

        self.bg_subtractor = self.create_subtractor(subtractor_type)
        # Initialize a counter
        self.frame_rate = 100

        cv2.namedWindow('Video')

        if define_roi_manually:
            cv2.setMouseCallback('Video', self.select_roi)

    def create_subtractor(self, subtractor_type):
        if subtractor_type == 'KNN':
            return cv2.createBackgroundSubtractorKNN(detectShadows=False)
        elif subtractor_type == 'MOG2':
            return cv2.createBackgroundSubtractorMOG2()
        elif subtractor_type == 'MOG':
            return cv2.bgsegm.createBackgroundSubtractorMOG()
        elif subtractor_type == 'GMG':
            return cv2.bgsegm.createBackgroundSubtractorGMG()
        else:
            raise ValueError("Invalid subtractor_type. Use 'KNN' , 'MOG', 'MOG2, or 'GMG'.")

    def select_roi(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.roi_points.append((x, y))
            print(x, " ", y)

    def define_roi(self):
        print("Click on the video frame to select points for ROI. Press 'Enter' to confirm ROI selection.")

        while True:
            if self.input_type == 'video' or self.input_type == 'camera':
                ret, frame = self.cap.read()
            else:

                frame = cv2.imread(self.image_files[self.current_image])
                height, width, channels = frame.shape
                ret = True

            if not ret:
                break

            frame_with_roi = frame.copy()

            if len(self.roi_points) >= 2:
                cv2.polylines(frame_with_roi, [np.array(self.roi_points)], isClosed=True, color=(0, 255, 0), thickness=2)

            cv2.imshow('Video', frame_with_roi)

            if self.input_type == 'image_sequence':
                if self.current_image < len(self.image_files) - 1:
                    self.current_image += 1

            key = cv2.waitKey(int(1000 / self.frame_rate))

            if key == 13:  # Enter key pressed
                break

        self.roi_points = np.array(self.roi_points, dtype=np.int32)

        if self.input_type == 'video' or self.input_type == 'camera':
            self.mask_template = np.zeros((int(self.cap.get(4)), int(self.cap.get(3))), dtype=np.uint8)
        else:
            self.mask_template = np.zeros((int(height), int(width)), dtype=np.uint8)
        cv2.fillPoly(self.mask_template, [self.roi_points], (255))

        # Set the VideoCapture object to the beginning of the video
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def process_video(self):
        # Initialize video capture and recorder objects
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (640, 480))

        # Set parameters for temporal filtering
        window_size = 10  # Number of frames to consider for temporal filtering
        cooldown_duration = 1  # Cooldown period after stopping recording (in seconds)
        cooldown_counter = cooldown_duration * 20  # Convert cooldown duration to frames (assuming 20 fps)

        # Initialize data structures for temporal filtering
        movement_window = deque(maxlen=window_size)
        is_recording = False
        # cooldown_counter = 0

        ignore_first_frame = True  # First foreground mask has a max value, so it will start recording even
        # if there is no movement, so we ignore the first foreground value

        if self.define_roi_manually:
            self.define_roi()

        while True:
            if self.input_type == 'video' or self.input_type == 'camera':
                ret, frame = self.cap.read()
            else:
                self.cap = cv2.imread(self.image_files[self.current_image])
                frame = self.cap
                # self.cap = self.image_files[self.current_image]
                # frame = cv2.imread(self.cap)
                ret = True

            if not ret:
                if is_recording:
                    out.release()
                    break

            frame_to_save = frame.copy()

            masked_frame = cv2.bitwise_and(frame, frame, mask=self.mask_template)
            foreground_mask = self.bg_subtractor.apply(masked_frame)
            num_white_pixels = np.sum(foreground_mask)

            # Add the movement metric to the window
            movement_window.append(num_white_pixels)

            if ignore_first_frame:
                ignore_first_frame = False
                continue

            # Calculate aggregated movement
            aggregated_movement = sum(movement_window)

            cv2.polylines(frame, [np.array(self.roi_points)], isClosed=True, color=(0, 0, 255), thickness=2)

            if num_white_pixels > self.threshold and not is_recording:
                is_recording = True
                out = cv2.VideoWriter(f'video_{datetime.now().strftime("%Y%m%d_%H%M%S")}.avi', fourcc, 20.0, (640, 480))
                cooldown_counter = 0

            if num_white_pixels <= self.threshold and is_recording:
                cooldown_counter += 1
                if cooldown_counter >= cooldown_duration * 20:  # Assuming 20 frames per second
                    out.release()
                    is_recording = False

            if is_recording:
                out.write(frame_to_save)
                # print("Recording, Significant movement detected!")
                cv2.circle(frame, (25, 25), 15, (0, 0, 255), -1, -1)
            # else:
            #     print("Stop recording, No movement Detected.")

            cv2.imshow('Foreground Mask', foreground_mask)  # Show the foreground mask with ROI applied
            cv2.imshow('Video', frame)  # Display the original frame

            if self.input_type == 'image_sequence':
                if self.current_image < len(self.image_files) - 1:
                    self.current_image += 1
                else:
                    if is_recording:
                        out.release()
                    break
            key = cv2.waitKey(30)

            if key == 27:  # Press Esc to exit
                if is_recording:
                    out.release()
                break

        # self.cap.release()
        if is_recording:
            out.release()


        cv2.destroyAllWindows()

        print(self.current_image)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Background Subtraction with ROI Selection')
    parser.add_argument('input_type', type=str, choices=['video', 'camera', 'image_sequence'], help='Input type')
    parser.add_argument('input_path', type=str, help='Camera number or Path to the video file or image sequence folder')
    parser.add_argument('subtractor_type', type=str, choices=['KNN', 'MOG', 'MOG2', 'GMG'],
                        help='Background subtractor type')
    parser.add_argument('--threshold', type=int, default=10000, help='Threshold for significant change')
    parser.add_argument('--define_roi_manually', action='store_true', help='Define ROI manually with the mouse')
    parser.add_argument('--roi_points', type=int, nargs='+', help='Coordinates of ROI points')

    args = parser.parse_args()

    # Convert the provided ROI points into a list of tuples
    roi_points = [(args.roi_points[i], args.roi_points[i + 1]) for i in
                  range(0, len(args.roi_points), 2)] if args.roi_points else []

    video_processor = VideoProcessor(args.input_type, args.input_path, args.subtractor_type, args.threshold, args.define_roi_manually,
                                     roi_points)
    if args.define_roi_manually and args.roi_points:
        keyboard.press('enter')

    video_processor.process_video()
