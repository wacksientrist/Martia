import cv2
import numpy as np
import multiprocessing

class Tracker():
    def __init__(self, color_hex) -> None:
        self.color_hex = color_hex
        self.average_x = '0'
        self.average_y = '0'
        self.average_z = '0'

        self.color_bgr = tuple(int(self.color_hex[i:i+2], 16) for i in (0, 2, 4))
        self.color_bgr = np.array([self.color_bgr], dtype=np.uint8)

        self.Camera1 = cv2.VideoCapture(0)
        #self.Camera2 = cv2.VideoCapture(0)
    def convert_rgb(self):
        Red = int(self.color_hex[0]+self.color_hex[1], 16)
        Green = int(self.color_hex[2]+self.color_hex[3], 16)
        Blue = int(self.color_hex[4]+self.color_hex[5], 16)

        return np.array([Red,Green,Blue])

    def track_and_average(self, cap):

        color_hex = self.color_hex

        ret, frame = cap.read()

        if ret == 1:

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            rgb_frame = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2RGB)
            

            lower_color = np.array([-50, -50, -50])+self.convert_rgb()
            upper_color = np.array([50, 50, 50])+self.convert_rgb()


            mask = cv2.inRange(rgb_frame, lower_color, upper_color)

            # Find contours of the color object
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            total_cx = 0
            total_cy = 0
            num_objects = 0

            # Iterate through detected contours
            for contour in contours:
                # Get the centroid of the contour
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Draw a circle at the centroid
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                    # Accumulate centroid coordinates
                    total_cx += cx
                    total_cy += cy
                    num_objects += 1

            # Calculate average centroid if objects were detected
            if num_objects > 0:
                average_cx = int(total_cx / num_objects)
                average_cy = int(total_cy / num_objects)

                # Print the average centroid coordinates
                print(f"Average centroid: ({average_cx}, {average_cy})")

                # Draw a circle at the average centroid
                cv2.circle(frame, (average_cx, average_cy), 10, (255, 0, 0), -1)

                cv2.imshow('Frame', frame)

                return str(average_cx)+","+str(average_cy)
            cv2.imshow('Frame', frame)
            return "0,0"
        return "0,0"

    def Track_Frame(self):
        while True:

            self.average_x = self.track_and_average(self.Camera1).split(',')[0]
            self.average_y = self.track_and_average(self.Camera1).split(',')[1]
            #self.average_z = self.track_and_average(self.Camera2).split(',')[0]

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.Close()
                break

            open("Tracks/Session1/0.txt", 'w').write(self.average_x+','+self.average_y+','+self.average_z)

    def Close(self):
        self.Camera1.release()
        #self.Camera2.release()
        cv2.destroyAllWindows()
    
    def Track(self):
        self.Track_Frame()


Object1 = Tracker(input("Input Color Value in Hex:"))
Object1.Track()