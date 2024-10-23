import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

latency_data = []
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

def init_plot():
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    return line,

def update_plot(frame):
    line.set_data(range(len(latency_data)), latency_data)
    return line,

cap = cv2.VideoCapture(0)

ani = FuncAnimation(fig, update_plot, init_func=init_plot, blit=True)

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
    combined = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    return combined

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    start_time = time.time()
    
    processed_frame = process_frame(frame)
    
    latency = (time.time() - start_time) * 1000
    latency_data.append(latency)
    
    if len(latency_data) > 100:
        latency_data.pop(0)
    
    combined_frame = np.hstack((frame, processed_frame))
    
    cv2.imshow('Original and Processed Video', combined_frame)
    
    plt.pause(0.001)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
