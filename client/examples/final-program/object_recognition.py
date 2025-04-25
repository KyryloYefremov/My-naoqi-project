import cv2  # type: ignore
import numpy as np  # type: ignore
import time
import os, sys
from imageai.Detection import ObjectDetection    # type: ignore


RUN_ON_NAO = True  # `True` to stream on NAO robot, set to `False` to run on local webcam

####### NAOqi3 library import #######
# add the current working directory to the system path
sys.path.insert(0, os.getcwd())
try:
    import naoqi3  # type: ignore
except ImportError:
    print("NAOqi3 library not found.")
    if RUN_ON_NAO:
        print("This script requires the NAOqi3 library to run on NAO robot.")
        sys.exit(1)

try:
    import vision_definitions as vd  # type: ignore
    from config import *  # type: ignore
except ImportError:
    print("vision_definitions or config module not found.")
    if RUN_ON_NAO:
        print("This script requires the vision_definitions and config modules to run on NAO robot.")
        sys.exit(1)
#####################################

# Configuration
LOW_RES = (320, 240)
BACKGROUND_UPDATE_ALPHA = 0.01
MOTION_THRESHOLD = 50
MIN_CONTOUR_AREA = 1000
COOLDOWN_TIME = 3
RETINA_MODEL_FILE = "retinanet_resnet.pth"
TINY_YOLO_MODEL_FILE = "tiny-yolov3.pt"


class MotionTriggeredDetector:
    def __init__(
            self, 
            model_file: str = TINY_YOLO_MODEL_FILE,
            stream_on_nao: bool = False,
    ):
        """
        Initialize the MotionTriggeredDetector with the specified model file and stream mode.
        
        :param model_file: Path to the model file for object detection.
        :param stream_on_nao: Boolean indicating whether to stream video on NAO robot.
        """
        self.stream_on_nao = stream_on_nao
        self.source = "NAO" if stream_on_nao else "Webcam"

        self.execution_path = os.getcwd() + "\\examples\\final-program\\"
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsTinyYOLOv3()
        path = self.execution_path +  model_file
        print(path)
        self.detector.setModelPath(path)
        self.detector.loadModel()
        
        if self.stream_on_nao:
            # Initialize video capture for NAO robot
            self.camera = naoqi3.ALProxy("ALVideoDevice", IP, PORT)  # type: ignore
            resolution = vd.kQVGA  # 320x240
            colorSpace = vd.kBGRColorSpace  # RGB formát
            fps = 30
            # Get string handle under which the module is known from ALVideoDevice
            self.name_id = self.camera.subscribe("python_GVM", resolution, colorSpace, fps)
            print("Initialized camera stream on NAO with ID:", self.name_id)
            # assign the method to get image from NAO
            self.get_image = self._get_image_from_nao 

            # Set language to english
            self.tts = naoqi3.ALProxy("ALTextToSpeech", IP, PORT)
            self.tts.setLanguage("English")
            self.tts.say("Hello, I am ready to detect objects.")
        else:
            # Initialize video capture for local webcam
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, LOW_RES[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, LOW_RES[1])
            # Initialize background model
            _, frame = self.camera.read()
            print("Initialized camera stream on local webcam.")\
            # assign the method to get image from webcam
            self.get_image = self._get_image_from_webcam

        # Initialize background model
        ret, frame = self.get_image()
        if not ret:
            raise RuntimeError(f"Failed to capture frame from {self.source}.")
        # Convert to grayscale and initialize as float32
        self.background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
        self.background = cv2.GaussianBlur(self.background, (21, 21), 0)  # Add blur for stability
        
        self.last_detection = 0

    def _get_image_from_nao(self):
        """
        Capture an image from the NAO robot's camera.
        """
        image = self.camera.getImageRemote(self.name_id)

        if image is None:
            return False, None

        width = image[0]
        height = image[1]
        channels = image[2]
        array = np.frombuffer(image[6], dtype=np.uint8).reshape((height, width, channels))
        return True, array.copy()


    def _get_image_from_webcam(self):
        """
        Capture an image from the local webcam.
        """
        ret, frame = self.camera.read()
        return ret, frame

    
    def show_result(self, detected_obj: dict):
        """
        SHow the result of the detection. If stream_on_nao is True, Nao will also say the result.
        :param detected_obj: The detected object.
        """
        print(f"Detected {detected_obj['name']} ({detected_obj['percentage_probability']:.1f}%)")
        if self.stream_on_nao:
            self.tts.say(detected_obj['name'])
    

    def release_camera(self):
        """
        Release the camera stream.
        """
        if self.stream_on_nao:
            self.camera.releaseImage(self.name_id)
            self.camera.unsubscribe(self.name_id)
            print(f"Unsubscribed from NAO camera stream ID: {self.name_id}.")
        else:
            self.camera.release()
            print("Released local webcam stream.")


    def detect_motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Update background model
        cv2.accumulateWeighted(gray.astype(np.float32), self.background, BACKGROUND_UPDATE_ALPHA)
        
        # Compare with background
        bg_uint8 = self.background.astype(np.uint8)
        diff = cv2.absdiff(bg_uint8, gray)
        _, thresh = cv2.threshold(diff, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return any(cv2.contourArea(c) > MIN_CONTOUR_AREA for c in contours)

    def process_frame(self, frame):
        # Convert frame to PIL Image
        frame_pil = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform object detection with RetinaNet
        detections = self.detector.detectObjectsFromImage(
            input_image=frame_pil,
            output_type="array",
            minimum_percentage_probability=40
        )
        
        # Return both annotated image and detection data
        return detections

    def run(self):
        try:
            while True:
                ret, frame = self.get_image()
                if not ret:
                    break

                if self.detect_motion(frame):
                    if time.time() - self.last_detection > COOLDOWN_TIME:
                        # Get detection results
                        annotated_image, detections = self.process_frame(frame)
                        
                        # Print and display results
                        for obj in detections:
                            self.show_result(obj)
                        
                        # Convert back to OpenCV format
                        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
                        cv2.imshow('Detection', annotated_image)
                        self.last_detection = time.time()
                    else:
                        cv2.imshow('Detection', frame)
                else:
                    cv2.imshow('Detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.release_camera()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = MotionTriggeredDetector(stream_on_nao=RUN_ON_NAO)
    detector.run()