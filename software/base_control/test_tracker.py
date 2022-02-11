from marker_tracking import MarkerTracking
import cv2

tracker = MarkerTracking()
tracker.setCameraConstants([[2.0, 0.0, 300.0], 
                            [0.0, 2.0, 300.0],
                            [0.0, 0.0, 1.0]],
                            [0.0, 0.0, 0.0, 0.0, 0.0])

# https://aliyasineser.medium.com/opencv-camera-calibration-e9a48bdd1844
# https://aliyasineser.medium.com/aruco-marker-tracking-with-opencv-8cb844c26628

# tracker.get_markers(image)

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()  

    frame = tracker.get_markers(frame)

    # Display the resulting frame
    cv2.imshow('frame',frame)
          
    # If "q" is pressed on the keyboard, 
    # exit this loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  