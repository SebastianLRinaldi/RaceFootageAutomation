import numpy as np
import cv2

frame_width, frame_height = 640, 480
frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
bar_y = 460  # near bottom

cv2.line(frame, (0, bar_y), (frame_width, bar_y), (0, 255, 255), 5)
cv2.imshow('test', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()