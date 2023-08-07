#!/usr/bin/env python
import csv
from scipy.spatial.transform import Rotation as R
import numpy as np
import shutil
import os

# -----------------------------------------------------------------------------
# Copy PoseID file (from cvsl_example_tracking) into root directory of the CVSL recording!

# Needed files and directories in record folder:
# cam0.txt
# cam0
# PoseID

# Set focal length as provided in config.yaml!
focal_length = 426

# -----------------------------------------------------------------------------

# Create directories
if not os.path.exists("ace-dataset/train/poses"):
    os.makedirs("ace-dataset/train/poses")

if not os.path.exists("ace-dataset/train/rgb"):
    os.makedirs("ace-dataset/train/rgb")

if not os.path.exists("ace-dataset/train/calibration"):
    os.makedirs("ace-dataset/train/calibration")

# Get image filenames
images = open('cam0.txt', 'r')
im_filenames = [row[1] for row in csv.reader(images, delimiter=' ')]

with open ('PoseID', 'r') as f:
    for row in csv.reader(f, delimiter=' '):
        id = row[0]

        qx = row[4]
        qy = row[5]
        qz = row[6]
        qw = row[7]

        T = np.eye(4, dtype=float)
        T[:3, :3] = R.from_quat([qx, qy, qz, qw]).as_matrix()
        T[0, 3] = row[1]
        T[1, 3] = row[2]
        T[2, 3] = row[3]
        
        np.savetxt("ace-dataset/train/poses/seq-01-frame-" + id + ".txt", T, delimiter=" ", fmt='%.10f')
        shutil.copy2(im_filenames[int(id)], "ace-dataset/train/rgb/seq-01-frame-" + id + ".color.png")
        
        calibration_file = open("ace-dataset/train/calibration/seq-01-frame-" + id + ".txt", "w")
        calibration_file.write(str(focal_length))
        calibration_file.close()