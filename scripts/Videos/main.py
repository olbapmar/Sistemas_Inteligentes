from videoHandler import VideoHandler
import sys

videoHandler = VideoHandler()
print(sys.argv[1])

try:
    videoHandler.start(sys.argv[1])
except Exception as e:
    raise e
except KeyboardInterrupt:
    videoHandler.parar()


