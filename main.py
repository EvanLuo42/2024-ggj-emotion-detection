import cv2
from fer import FER
from fer.utils import draw_annotations

detector = FER(mtcnn=False)
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FPS, 60)

results = []

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    emotions = detector.detect_emotions(frame)
    frame = draw_annotations(frame, emotions)
    for emotion in emotions:
        happy_confidence = emotion['emotions']['happy']
        if happy_confidence > 0.25:
            file = open('is_smiling', 'w')
            file.write('True')
            file.close()
        else:
            file = open('is_smiling', 'w')
            file.write('False')
            file.close()

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

