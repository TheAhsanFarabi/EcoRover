import cv2
from src.vision import ObjectDetector
from src.controller import RobotController

def main():
    # Initialize components
    detector = ObjectDetector(model_path="models/yolov11n_float16.tflite")
    bot = RobotController(port='/dev/ttyACM0') # Standard Arduino port on Pi
    cap = cv2.VideoCapture(0)

    print("EcoRover System Started...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret: break

            # 1. Detect Waste
            detections = detector.detect(frame)

            if detections:
                target = detections[0] # Target the highest confidence object
                box = target['box']
                
                # 2. Control Logic (Simple visual servoing)
                # Calculate center of the object (x_center ranges 0.0 to 1.0)
                x_center = (box[1] + box[3]) / 2 

                if 0.4 < x_center < 0.6:
                    # Object is centered, move forward
                    print("Target Centered. Moving Forward.")
                    bot.move_forward()
                    
                    # If object is very large (close), stop and grab
                    # (box height implies distance)
                    box_height = box[2] - box[0]
                    if box_height > 0.8: 
                        print("Target Close. Initiating Grab.")
                        bot.stop()
                        bot.grab_object()
                        break # End loop after collection (or reset)
                
                elif x_center <= 0.4:
                    print("Target on Left. Adjusting.")
                    bot.turn_left()
                
                elif x_center >= 0.6:
                    print("Target on Right. Adjusting.")
                    bot.turn_right()
            else:
                # No object, search or stop
                bot.stop()

            # Display feed (Optional, disable for headless)
            cv2.imshow('EcoRover Vision', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        bot.stop()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()