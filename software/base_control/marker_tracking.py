from base_control import sat_msgs
import cv2
from cv2 import aruco
import numpy as np

# Reference: https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/

class MarkerTracking:

    def __init__(self):
        
        self.sat_pose = False
        self.good_sat_reading = False

        self.dead_sat_pose = False

        # Create dictionary and paremters
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
        self.parameters = cv2.aruco.DetectorParameters_create()

        self.cameraMatrix = None
        self.distCoeff = None
    
    def setCameraConstants(self, cameraMatrix, distCoeff):
        self.cameraMatrix = np.array(cameraMatrix)
        print(self.cameraMatrix)
        self.distCoeff = np.array(distCoeff)

    def get_markers(self, image, draw = True):
        """ Returns the pose of markers in an image """

        frame = image
        
        # Detect ArUco markers in the video frame
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            frame, self.aruco_dict, parameters = self.parameters)
            
        # Check that at least one ArUco marker was detected
        if np.all(ids is not None): 
            
            # Loop over the detected ArUco corners
            for i in range(0, len(ids)):

                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, self.cameraMatrix, self.distCoeff)
                (rvec - tvec).any()  # get rid of that nasty numpy value array error
                cv2.aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers
                cv2.aruco.drawAxis(frame, self.cameraMatrix, self.distCoeff, rvec, tvec, 0.01)
                
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

        return frame