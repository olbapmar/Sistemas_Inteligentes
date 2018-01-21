from videoHandler_semaforos import VideoHandler
import sys
import cv2

videoHandler = VideoHandler()
print(sys.argv[1])

try:
    videoHandler.start(sys.argv[1])
except (Exception, cv2.error) as e:
    raise e
except KeyboardInterrupt:
    videoHandler.parar()