import os
import cv2
import time
from ultralytics import YOLO

# Paths
model_path = os.path.abspath("E:/Project/pretrained/yolov8n.pt")
alert_folder_path = os.path.abspath("E:/Project/data/alerts/")

# Create alert folder if it doesn't exist
os.makedirs(alert_folder_path, exist_ok=True)

# Load YOLOv8 model
print("Loading YOLO model...")
model = YOLO(model_path)

# Access the live camera (use 0 for the default camera)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error accessing the camera.")
    exit()

fps = 30  # Assuming standard frame rate for live video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

frame_count = 0  # Frame counter for naming alert snapshots
last_snapshot_time = 0  # Timestamp of the last snapshot
snapshot_delay = 30  # Delay between snapshots in seconds

# Define the queue area (as percentage of frame size)
queue_top = int(frame_height * 0.1)
queue_bottom = int(frame_height * 0.8)
queue_left = int(frame_width * 0.25)
queue_right = int(frame_width * 0.75)

# Define the queue area rectangle for visualization
queue_area = (queue_left, queue_top, queue_right, queue_bottom)

print("Starting live video processing...")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from the camera.")
        break

    # Detect people using YOLOv8
    results = model.predict(source=frame, conf=0.5, show=False)
    detections = results[0].boxes.xyxy.cpu().numpy()  # Bounding boxes
    num_people_in_queue = 0  # Initialize people count in the queue area

    # Draw the queue area rectangle
    cv2.rectangle(frame, (queue_left, queue_top), (queue_right, queue_bottom), (255, 0, 0), 2)
    cv2.putText(frame, "Queue Area", (queue_left + 5, queue_top + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Count people in the queue area
    for det in detections:
        x1, y1, x2, y2 = map(int, det[:4])

        # Check if the detected person is inside the queue area
        if x2 > queue_left and x1 < queue_right and y2 > queue_top and y1 < queue_bottom:
            num_people_in_queue += 1
            # Draw bounding box for people in the queue area
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the number of people in the queue area on the frame
    cv2.putText(frame, f"Queue People Count: {num_people_in_queue}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Alert: Save snapshot if people count exceeds threshold and delay is respected
    current_time = time.time()
    if num_people_in_queue > 5 and (current_time - last_snapshot_time > snapshot_delay):
        alert_snapshot_path = os.path.join(alert_folder_path, f"alert_frame_{frame_count}.jpg")
        cv2.imwrite(alert_snapshot_path, frame)
        last_snapshot_time = current_time  # Update the last snapshot time
        print(f"Alert: People count exceeded threshold. Snapshot saved to {alert_snapshot_path}")

    # Display the live video feed with detections
    cv2.imshow("Live Video Feed", frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
print(f"Alert snapshots saved in: {alert_folder_path}")
