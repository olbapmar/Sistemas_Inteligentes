from videoHandler import VideoHandler
import sys

videoHandler = VideoHandler()
print(sys.argv[1])

try:
    videoHandler.start(sys.argv[1])
except (KeyboardInterrupt, SystemExit):
    videoHandler.noParar = False
    sys.exit()
            


