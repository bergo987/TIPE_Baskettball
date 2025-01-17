import cv2
import numpy as np

# Set up the video capture

# Define the lower and upper HSV color range of the basketball
lower_ball = np.array([8, 160, 100])
upper_ball = np.array([10, 200, 255])

lower_bu = np.array([0, 50, 50])
upper_bu = np.array([49, 237, 191])
# Initialize variables for tracking
prev_ball_count = 0
ball_count = 0

prev_bu_count = 0 
bu_count = 0

loop_count = 0 

while True:
    # Capture frame from the video
    isclosed = 0
    cap = cv2.VideoCapture('/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Baskettball/script/IA_assistef/01.mp4')
    
    while True:

        ret, frame = cap.read()
        if not ret:
            isclosed
            break

        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask to isolate the basketball
        ball_mask = cv2.inRange(hsv, lower_ball, upper_ball)
        bu_mask = cv2.inRange(hsv, lower_bu, upper_bu)

        # Apply morphological transformations to the mask
        kernel = np.ones((5,5), np.uint8)
        opening_ball = cv2.morphologyEx(ball_mask, cv2.MORPH_OPEN, kernel)
        closing_ball = cv2.morphologyEx(opening_ball, cv2.MORPH_CLOSE, kernel)

        opening_bu = cv2.morphologyEx(bu_mask, cv2.MORPH_OPEN, kernel)
        closing_bu = cv2.morphologyEx(opening_bu, cv2.MORPH_CLOSE, kernel)
        # Find contours of the basketball
        contours_ball, hierarchy_ball = cv2.findContours(closing_ball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_bu , hierarchy_bu = cv2.findContours(closing_bu,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Draw bounding boxes around the basketball and count them
        ball_count = 0
        bu_count = 0 
        for element in contours_ball:
            area = cv2.contourArea(element)
            if area < 2000 and area > 500: #permet de s'assurer que les petites taches ne sont pas prises en compte 
                x, y, w, h = cv2.boundingRect(element)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                ball_count += 1

        for countour in contours_bu : 
            area = cv2.contourArea(countour)
            if area > 1000 :
                x,y,w,h = cv2.boundingRect(countour)
                #cv2.rectangle(frame, (x,y),(x+w,y+h), (255,0,0),2)
                bu_count += 1

        # Display the tracking result on the screen
        cv2.putText(frame, "nb balles: " + str(ball_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, "nb panier: " + str(bu_count), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        
        cv2.imshow("Basketball Tracker", frame)
        cv2.imshow("Ball Mask",ball_mask)
        #cv2.imshow("BU Mask",bu_mask)
        # Exit the program if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            isclosed= 1
            break

        # Update the previous count
        prev_ball_count = ball_count
        prev_bu_count = bu_count
    loop_count += 1
    if isclosed or loop_count > 0 : 
        break
print("nombre de boucle ", loop_count)
# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
