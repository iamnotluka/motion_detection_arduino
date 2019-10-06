import cv2 # import cv2 for conmputer vision functions
import serial # import serial for connection between arduino and python

# declare video module
video = cv2.VideoCapture(0)

# declare static background as None initially
static_back = None
# no motion count is variable used to reset time for movement detection
no_motion_count = 0

# boolean that desribes if something is in the frame [0 for False 1 for True]
in_frame = 0

# window display key
order = 1

# declare serial connection between arduino and python
arduino_serial = serial.Serial('com5', 9600)
# print message from arduino to confirm connection
print(arduino_serial.readline())

while True:
    # set motion boolean to 0
    motion = 0

    # read the frame from the video capture
    check, frame = video.read()

    # change frame to gray and resize
    frame = cv2.resize(frame, (960, 720), interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # initialize static_background
    if static_back is None:
        static_back = gray
        # set new frame to be gray frame
        new_frame = gray
    
    # if nothing has changed after 300 frames, there is no motion, therefor reset previous image
    if no_motion_count > 300:
        # print("RESET")
        new_frame = gray
        # reset count as well
        no_motion_count = 0
    
    # calculate diff_frame for new_frame and gray area
    diff_frame = cv2.absdiff(new_frame, gray)
    # calculate difference frame for static_frame
    diff_frame_static = cv2.absdiff(static_back, gray)

    # threshold_frame calclated to check if object is moving
    thresh_frame = cv2.threshold(diff_frame, 35, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 

    # threshold_frame calculated to chack if object is in the screen
    thresh_frame_static = cv2.threshold(diff_frame_static, 35, 255, cv2.THRESH_BINARY)[1]
    thresh_frame_static = cv2.dilate(thresh_frame_static, None, iterations = 2)

    # find contours for diff that checks if object is moving
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # find contours for diff that checks if object is present
    (cnts_static, _) = cv2.findContours(thresh_frame_static.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # for every contour found, if area is less then threshold value, just continue
    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            no_motion_count += 1
        # else set motion to one
        else:
            motion = 1
    
    in_frame = 0
    for contour in cnts_static:
        if cv2.contourArea(contour) < 1000:
            if in_frame != 1:
                in_frame = 0
            continue
        in_frame = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
    
    # send signal to the arduino
    if in_frame == 0:
        # print("_ ")
        arduino_serial.write(b'3')
    if in_frame == 1:
        if motion == 0:
            # print("X ")
            arduino_serial.write(b'1')
        else:
            # print("X", "M")
            arduino_serial.write(b'2')

    # display threshold frame
    if order == 2:
        cv2.imshow("Threshold Frame", thresh_frame)
    # display normal frame
    if order == 1:
        cv2.imshow("Normal Frame", frame)
    # display diff frame
    if order == 3:
        cv2.imshow("Diff Frame", diff_frame_static)

    # ket the key
    key = cv2.waitKey(20)

    # perform depending on the key
    if key == ord('q'):
        break
    if key == ord('1'):
        order = 1
        cv2.destroyAllWindows()  
    if key == ord('2'):
        order = 2
        cv2.destroyAllWindows()  
    if key == ord('3'):
        order = 3
        cv2.destroyAllWindows()  

# turn off LEDs by writing function 3
arduino_serial.write(b'3')

# close serial connection
arduino_serial.close()
# close video capture
video.release()

# destroy all windows
cv2.destroyAllWindows()  