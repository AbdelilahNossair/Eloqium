import cv2
from gaze_tracking import GazeTracking

# Initialize gaze tracking and video capture
gaze = GazeTracking()
webcam = cv2.VideoCapture(1)

frames_looking_at_camera = 0
total_frames = 0

try:
    while True:
        # Read a frame from the webcam
        ret, frame = webcam.read()
        if not ret:
            break

        total_frames += 1

        # Refresh gaze analysis on the current frame
        gaze.refresh(frame)
        annotated_frame = gaze.annotated_frame()

        # Determine gaze direction
        if gaze.is_blinking():
            status_text = "Blinking"
        elif gaze.is_right():
            status_text = "Looking right"
        elif gaze.is_left():
            status_text = "Looking left"
        elif gaze.is_center():
            status_text = "Looking center"
            frames_looking_at_camera += 1
        else:
            status_text = "Face not detected"

        # Display status on the frame
        cv2.putText(annotated_frame, status_text, (90, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        # Show the annotated frame
        cv2.imshow("Gaze Detection", annotated_frame)

        # Exit loop if 'Esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

finally:
    # Release resources
    webcam.release()
    cv2.destroyAllWindows()

    # Calculate and print percentage of eye contact
    if total_frames > 0:
        percentage = (frames_looking_at_camera / total_frames) * 100
        print(f"Percentage of eye contact: {percentage:.2f}%")
    else:
        print("No frames captured.")