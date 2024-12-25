import cv2
import mediapipe as mp

class PosDetector:

    def __init__(self):
        mp_face_detection = mp.solutions.face_detection
        self.face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

        self.capture = cv2.VideoCapture(0)
        
        self.mp_drawing = mp.solutions.drawing_utils

        

    def capture_faces(self):
            if self.capture.isOpened():
                ret, frame = self.capture.read()
                if not ret:
                    print("Failed to grab frame")
                    
                # Convert the image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # To improve performance, mark the image as not writeable to pass by reference
                image.flags.writeable = False
                
                # Process the image and detect faces
                results = self.face_detection.process(image)

                # Draw the face detection results
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                return results
