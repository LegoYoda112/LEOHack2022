from base_control import sat_msgs
import cv2
from cv2 import aruco
import numpy as np
from scipy.spatial.transform import Rotation as R
import math

import depthai as dai

import coloredlogs, logging

import threading

import time

# Reference: https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/

class MarkerTracking:

    def __init__(self, live_id = 69, dead_id = 420, display = True, logging_level = logging.DEBUG):

        # Install colored logs :)
        coloredlogs.install(level=logging_level)

        # Set the basic config up with correct log level
        logging.basicConfig(level=logging_level)

        # Make a new logger
        self.logger = logging.getLogger('Marker tracking')
        
        self.sat_pose = False
        self.good_sat_reading = False

        self.dead_sat_pose = sat_msgs.Pose2D()

        # Create dictionary and paremters
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
        self.parameters = cv2.aruco.DetectorParameters_create()

        self.cameraMatrix = None
        self.distCoeff = None

        self.display = display

        self.markers = {'live': None, 'dead': None}

        self.tracking_thread = None
        self.tracking_thread_lock = threading.Lock()

        self.live_id = live_id
        self.dead_id = dead_id

        self.setup_dai()
    
    def setCameraConstants(self, cameraMatrix, distCoeff):
        self.cameraMatrix = np.array(cameraMatrix)
        print(self.cameraMatrix)
        self.distCoeff = np.array(distCoeff)

    def euler_from_quaternion(self, x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
            
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
            
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
            
        return roll_x, pitch_y, yaw_z # in radians

    def get_markers(self, image, draw = True):
        """ Returns the pose of markers in an image """

        frame = image

        markers = {}
        
        # Detect ArUco markers in the video frame
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            frame, self.aruco_dict, parameters = self.parameters)
            
        # Check that at least one ArUco marker was detected
        if np.all(ids is not None): 
            
            # Loop over the detected ArUco corners
            for i, marker_id in enumerate(ids):

                if(marker_id == self.live_id or marker_id == self.dead_id):
                    rvecs, tvecs, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.096, self.cameraMatrix, self.distCoeff)
                    # (rvecs - tvecs).any()  # get rid of that nasty numpy value array error
                    cv2.aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers
                    cv2.aruco.drawAxis(frame, self.cameraMatrix, self.distCoeff, rvecs, tvecs, 0.02)

                    rotation_matrix = np.eye(4)
                    rotation_matrix[0:3, 0:3] = cv2.Rodrigues(np.array(rvecs[0][0]))[0]
                    r = R.from_matrix(rotation_matrix[0:3, 0:3])
                    quat = r.as_quat()   

                    # Quaternion format     
                    transform_rotation_x = quat[0] 
                    transform_rotation_y = quat[1] 
                    transform_rotation_z = quat[2] 
                    transform_rotation_w = quat[3] 
                    
                    # Euler angle format in radians
                    roll_x, pitch_y, yaw_z = self.euler_from_quaternion(transform_rotation_x, 
                                                                transform_rotation_y, 
                                                                transform_rotation_z, 
                                                                transform_rotation_w)

                    # Store the translation (i.e. position) information
                    translation_x = tvecs[0][0][0]
                    translation_y = tvecs[0][0][1]
                    translation_z = tvecs[0][0][2]

                    marker_pose = sat_msgs.Pose2D()

                    marker_pose.x = -translation_x
                    marker_pose.y = -translation_z
                    marker_pose.theta = -pitch_y + 3.1415/2
                    
                    markers[marker_id[0]] = marker_pose
                    
                    # print(marker_id, " = ", translation_x, translation_z, pitch_y)
                    #print(quat) 
                    #print(tvec)

                    
                    # if draw:
                    #     # Draw the bounding box of the ArUco detection
                    #     cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
                    #     cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
                    #     cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
                    #     cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)
                            
                    #     # Calculate and draw the center of the ArUco marker
                    #     center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                    #     center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                    #     cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)
                            
                    #     # Draw the ArUco marker ID on the video frame
                    #     # The ID is always located at the top_left of the ArUco marker
                    #     cv2.putText(frame, str(marker_id), 
                    #         (top_left[0], top_left[1] - 15),
                    #         cv2.FONT_HERSHEY_SIMPLEX,
                    #         0.5, (0, 255, 0), 2)

        ret_markers = {}
        # print(markers)
        if(self.live_id in markers):
            ret_markers['live'] = markers[self.live_id]
        else:
            ret_markers['live'] = None
        
        if(self.dead_id in markers):
            ret_markers['dead'] = markers[self.dead_id]
        else:
            ret_markers['dead'] = None

        return frame, ret_markers

    def start(self):
        print("starting thread")
        self.tracking_thread = threading.Thread(target = self.tracking_thread_function, daemon=True)
        self.tracking_thread.start()

        self.tracking_thread_lock.acquire()
        time.sleep(0.1)

    def tracking_thread_function(self):
        self.tracking_thread_lock.acquire()

        self.logger.debug("Running tracking thread")

        # Connect to device and start pipeline
        with dai.Device(self.pipeline, usb2Mode = True) as device:

            calibData = device.readCalibration()

            M_rgb, width, height = calibData.getDefaultIntrinsics(dai.CameraBoardSocket.RGB)
            M_rgb = np.array(M_rgb) / 2
            # print(M_rgb / 2)
            # print(width / 2)
            # print(height / 2)

            D_rgb = calibData.getDistortionCoefficients(dai.CameraBoardSocket.RGB)
            print(D_rgb)

            self.setCameraConstants(M_rgb, D_rgb)

            video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

            self.tracking_thread_lock.release()

            while True:
                videoIn = video.get()

                frame = videoIn.getCvFrame()
                frame, new_markers = self.get_markers(frame)

                if(new_markers['dead'] != None):
                    self.markers['dead'] = new_markers['dead']
                
                self.markers['live'] = new_markers['live']

                # print(self.markers)

                if self.display:
                    cv2.imshow("video", frame)

                    if cv2.waitKey(1) == ord('q'):
                        break
    
    def setup_dai(self):
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define source and output
        camRgb = self.pipeline.create(dai.node.ColorCamera)
        xoutVideo = self.pipeline.create(dai.node.XLinkOut)

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