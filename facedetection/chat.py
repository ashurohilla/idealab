import cv2
import mediapipe as mp
import serial

# Initialize the FaceMesh model and the video capture device
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
cap = cv2.VideoCapture(1)

# Connect to the Arduino serial port
ArduinoSerial = serial.Serial('com3', 9600)
def sendingdata(string ):
    ArduinoSerial.write(string.encode('utf-8'))
    print(string)

while True:
    # Capture a frame from the video device
    success, frame = cap.read()
    if not success:
        break

    # Convert the BGR image to RGB and process it with the FaceMesh model
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # If landmarks are detected, draw them on the image and send their coordinates to the Arduino
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x = int (landmark.x * image.shape[1])
                y = int (landmark.y * image.shape[0])
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
                string = 'X{0:d}Y{1:d}'.format((x), (y))
                sendingdata()
                

    # Display the image
    cv2.imshow('Face Mesh', frame)
    if cv2.waitKey(1) == ord('q'):
        break
# Release the resources
cap.release()
cv2.destroyAllWindows()
