import cv2
import depthai as dai
import time
import numpy as np

from marker_tracking import MarkerTracking

# https://docs.luxonis.com/projects/api/en/latest/samples/calibration/calibration_reader/?highlight=camera%20matrix

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB) # THE_1080_P
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(1920, 1080)
# camRgb.setVideoSize(1920 * 2, 1080 * 2)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Linking
camRgb.video.link(xoutVideo.input)

# Marker tracking
tracker = MarkerTracking()


# Connect to device and start pipeline
with dai.Device(pipeline, usb2Mode = True) as device:

    calibData = device.readCalibration()

    M_rgb, width, height = calibData.getDefaultIntrinsics(dai.CameraBoardSocket.RGB)
    M_rgb = np.array(M_rgb) / 2
    # print(M_rgb / 2)
    # print(width / 2)
    # print(height / 2)

    D_rgb = calibData.getDistortionCoefficients(dai.CameraBoardSocket.RGB)
    print(D_rgb)

    tracker.setCameraConstants(M_rgb, D_rgb)

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    while True:
        videoIn = video.get()

        frame = videoIn.getCvFrame()
        frame, markers = tracker.get_markers(frame)

        cv2.imshow("video", frame)

        if cv2.waitKey(1) == ord('q'):
            break