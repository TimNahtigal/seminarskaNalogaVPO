import cv2
import datetime
import json

filename = 'video.avi'
frames_per_second_string = input("Koliko slik na sekundo (12.0), hočeš snemati? (Več kot jih je hitejši je playback):")

try:
    frames_per_second = int(frames_per_second_string)
except ValueError:
    print("Število more biti intinger")
    frames_per_second_string = input("Koliko slik na sekundo (12.0), hočeš snemati?"
                                     "(Več kot jih je hitejši je playback):")
    frames_per_second = int(frames_per_second_string)
res = input("S katero rezolucijo hočeš snemati? (480p, 720p, 1080p)")
print("Ko se okno odpre, ga lahko zapreš z Q.")


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
}


def get_dims(cap, res="1080p"):  # spremeni rezolucijo, če je vnešena narobna bo rezolucija 480p
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]

    change_res(cap, width, height)
    return width, height


fourcc = cv2.VideoWriter_fourcc(*'MJPG')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# datoteka za zaznavanje človeka: "https://github.com/opencv/opencv/tree/master/data/haarcascades"


cap = cv2.VideoCapture(0)  # kamera 1

out = cv2.VideoWriter(filename, fourcc, frames_per_second, get_dims(cap, res))  # writer za .mp4

pastfacesx = 3
x = 1
cas = datetime.datetime.now()
cas_string = str(datetime.datetime.now())
prejsni_cas = datetime.datetime.now()

casi_json = []

timestampi_frame = [0]
stevilo_frame = 0

while cap.isOpened():

    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

    if x != pastfacesx:

        frame = cv2.putText(frame, cas_string, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2, cv2.LINE_AA)
        stevilo_frame = stevilo_frame + 1
        out.write(frame)
        cv2.imshow('img', frame)

        if cas > prejsni_cas:
            casi_json.append(str(datetime.datetime.now()))
            timestampi_frame.append(stevilo_frame)
            print(cas_string)
            prejsni_cas = cas + datetime.timedelta(seconds=15)

    x = pastfacesx
    cv2.imshow('img', frame)
    cas_string = str(datetime.datetime.now())
    cas = datetime.datetime.now()

    if cv2.waitKey(1) & 0xFF == ord('q'):  # ko pritisneš q se vse zapre
        break

stevilo_json = 0
json_dictionary = {}

for i in casi_json:
    json_dictionary[i] = timestampi_frame[stevilo_json]

    stevilo_json = stevilo_json + 1

json_file = open("Casi.json", "w", encoding="utf-8")
json.dump(json_dictionary, json_file, ensure_ascii=False)

json_file.close()
out.release()  # ugasne vse
cap.release()
cv2.destroyAllWindows()
