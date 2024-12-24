import cv2
import mediapipe as mp

class PosDetector:

    def __init__(self):
        mp_face_detection = mp.solutions.face_detection
        self.cap = cv2.VideoCapture(0)
        
        self.mp_drawing = mp.solutions.drawing_utils

        self.face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    def capture_facesx(self):




        
        with self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # To improve performance, mark the image as not writeable to pass by reference
            image.flags.writeable = False
            
            # Process the image and detect faces
            results = face_detection.process(image) 

            return results
   

    def capture_faces(self):

            if self.cap.isOpened():
                ret, frame = self.cap.read()
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
                if results.detections:
                    print(results.detections)
                    for i, detection in enumerate(results.detections):
                        # Draw the face bounding box and keypoints
                        self.mp_drawing.draw_detection(image, detection)

                        # Extract face bounding box coordinates
                        bboxC = detection.location_data.relative_bounding_box
                        ih, iw, _ = image.shape
                        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                        # Annotate the image with face ID
                        cv2.putText(image, f'Face {i + 1}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Display the output
                cv2.imshow('Face Detection', image)