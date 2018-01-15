import cv2

vidFile = cv2.VideoCapture(0)

fps = 25

ret, frame = vidFile.read() # read first frame, and the return code of the function.
while ret:  # note that we don't have to use frame number here, we could read from a live written file.
    print("yes")
    cv2.imshow("frameWindow", frame)
    cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
    ret, frame = vidFile.read()
