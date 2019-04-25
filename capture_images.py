import cv2
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description="===> CAPTURE STEREO IMAGES THROUGH THE LOGITECH C270 HD CAMERAS <===")
parser.add_argument("devices", type=int, nargs=2, help="Device numbers for the cameras that should be accessed in order: (right_camera, left_camera)")
parser.add_argument("--out_folder", help="Folder to write output images")
parser.add_argument("--show_frames", type=int, default=0, help="Defines if the frames are shown or not (1 to show or 0 to not show) (default=0)")
args = parser.parse_args()

# ============================================================

# Get current frames from cameras
captures = [cv2.VideoCapture(device) for device in args.devices]

# Change frames resolution
for capture in captures:
    capture.set(3, 1280)
    capture.set(4, 960)

# Read current frames from cameras
images = [np.rot90(capture.read()[1]) for capture in captures]

# Save frames
if args.out_folder:
    for side, image in zip(("right", "left"), images):
        filename = "image_{}.jpg".format(side)
        output_path = os.path.join(args.out_folder, filename)
        cv2.imwrite(output_path, image)

# Show frames
if args.show_frames is 1:
    for side, image in zip(("Right", "Left"), images):
        window_name = "Image_{}.jpg".format(side)
        cv2.imshow(window_name, image)
    cv2.waitKey()

# ============================================================

