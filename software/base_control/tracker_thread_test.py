from marker_tracking import MarkerTracking
import time

tracker = MarkerTracking()

tracker.start()

while(1):
    print(tracker.markers)

    time.sleep(1)