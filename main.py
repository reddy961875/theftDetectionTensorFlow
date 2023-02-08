import tkinter as tk
import cv2
import time
import tkinter.font as font
import numpy as np
import tensorflow as tf

def predict(model, x):

    x = np.expand_dims(x, axis=0)
    x = x.astype("float32") / 255.0
    predictions = model.predict(x)
    predictions = predictions.flatten()
    return predictions

def find_motion():
    motion_detected = False
    is_start_done = False

    cap = cv2.VideoCapture(0)

    check = []
    time.sleep(2)
    frame1 = cap.read()

    _, frm1 = cap.read()
    frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)

    while True:
        _, frm2c = cap.read()
        frm2 = cv2.cvtColor(frm2c, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(frm1, frm2)

        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # look at it
        contours = [c for c in contours if cv2.contourArea(c) > 25]

        if len(contours) > 5:
            cv2.putText(frm2c, "motion detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            motion_detected = True
            is_start_done = False

        elif motion_detected and len(contours) < 3:
            if not is_start_done:
                start = time.time()
                is_start_done = True
                end = time.time()

            end = time.time()

            print(end - start)
            if (end - start) > 4:
                frame2 = cap.read()
                cap.release()
                cv2.destroyAllWindows()
                x = np.abs(frame1, frame2)
                if x == 0:
                    print("running again")
                    return

                else:
                    print("found motion sending mail")
                    return

        else:
            cv2.putText(frm2c, "no motion detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("reddy", frm2c)

        _, frm1 = cap.read()
        frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR)

        _, frm2 = cap.read( )
        frm2 = cv2.cvtColor(frm2, cv2.COLOR_BGR2GRAY)
        frm2 = cv2.GaussianBlur(frm2, (21, 21), 0)

        if frm1 is None:
            frm1 = frm2
            continue

        delta_frame = cv2.absdiff(frm1, frm2)
        threshold_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        threshold_delta = cv2.dilate(threshold_delta, None, iterations=2)

        (cnts, _) = cv2.findContours(threshold_delta.copy( ), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 1000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frm2, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frm2, "motion detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            cv2.putText(frm2, "no motion detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("reddy", frm2)

        frm1 = frm2

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows( )
            break

window =  tk.Tk()
window.title = "find stolen"
window.geometry("450x200")

#label
label = tk.Label(window, text="Welcome")
label.grid(row=0, column=1)
label['font'] = font.Font(size=35, weight='bold',family='Helvetica')

#button font
btn_font = font.Font(size=15, weight='bold',family='Helvetica')

button1 = tk.Button(window, text="spot diff",fg="green", height=3, width=10, command=find_motion)
button1['font'] = btn_font
button1.grid(row=1, pady=(25,10),padx=(10,0), column = 0)

#exit button
button2 = tk.Button(window, text="exit",fg="red", height=3, width=10, command=window.quit)
button2['font'] = btn_font
button2.grid(row=1, pady=(25,10), column=2)

window.mainloop()


