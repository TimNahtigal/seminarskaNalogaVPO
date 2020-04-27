import cv2
import time
import PySimpleGUI as sg
import json

jonny_file = open("Casi.json")

casi = json.load(jonny_file)

jonny_file.close()

sg.theme('DarkAmber')

layout = [[sg.Button('Framestep')]]

for cas in casi:
    if cas != 0:
        dodaj = [sg.Button(cas)]
        layout.append(dodaj)

window = sg.Window('json', layout)


def nothing(x):
    pass


cv2.namedWindow("Ultra mega camera")
# create switch for ON/OFF functionality

cv2.createTrackbar("hitrost/fps", 'Ultra mega camera', 12, 60, nothing)

cap = cv2.VideoCapture("video.avi")

nr_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cv2.createTrackbar("Video", "Ultra mega camera", 0, nr_of_frames, nothing)

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'Ultra mega camera', 0, 1, nothing)

while cap.isOpened():

    fps = cv2.getTrackbarPos("hitrost/fps", "Ultra mega camera")

    if fps != 0:

        rez, frame = cap.read()

        if rez:
            cv2.imshow('Ultra mega camera', frame)
            cv2.setTrackbarPos("Video", "Ultra mega camera", int(cap.get(cv2.CAP_PROP_POS_FRAMES)))

            time.sleep(1 / fps)
        else:
            break

    if cv2.waitKey(1) & 0xFF == ord(" "):
        while cv2.waitKey(1) & 0xFF == ord("d"):
            pass
        while True:
            if cv2.waitKeyEx(1) & 0xFF == ord("d"):

                rez, frame = cap.read()

                if rez:
                    cv2.imshow('Ultra mega camera', frame)

                else:
                    cv2.destroyAllWindows()
                    quit()
                while cv2.waitKey(1) & 0xFF == ord("d"):
                    pass
            if cv2.waitKey(1) & 0xFF == ord(" "):
                break

    while cv2.getTrackbarPos(switch, 'Ultra mega camera'):

        event, values = window.read()

        if event in (None, "Framestep"):  # if user closes window or clicks cancel
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(casi.get(event)))
        _, frame = cap.read()
        cv2.imshow("Ultra mega camera", frame)
        cv2.setTrackbarPos("Video", "Ultra mega camera", int(cap.get(cv2.CAP_PROP_POS_FRAMES)))

window.close()
cv2.destroyAllWindows()

