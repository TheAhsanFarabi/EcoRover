import cv2
import numpy as np
try:
    # On RPi, use tflite_runtime if full tensorflow is too heavy
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

class ObjectDetector:
    def __init__(self, model_path="models/yolov11n_float16.tflite"):
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

    def detect(self, frame):
        """
        Takes a frame, runs inference, returns list of detections:
        [{'label': 'bottle', 'box': [ymin, xmin, ymax, xmax], 'score': 0.85}, ...]
        """
        frame_resized = cv2.resize(frame, (self.width, self.height))
        input_data = np.expand_dims(frame_resized, axis=0).astype(np.float32)
        
        # Normalize if model requires it (usually 0-1 or -1 to 1)
        input_data = input_data / 255.0

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        # Retrieve outputs (YOLO output format varies, simplifying for standard detection)
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # Bounding boxes
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Class Index
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0] # Confidence

        results = []
        for i in range(len(scores)):
            if scores[i] > 0.5: # Confidence threshold
                # Logic to filter only "waste" classes (e.g., bottle, can)
                results.append({
                    'class_id': int(classes[i]),
                    'score': float(scores[i]),
                    'box': boxes[i] # [ymin, xmin, ymax, xmax]
                })
        return results