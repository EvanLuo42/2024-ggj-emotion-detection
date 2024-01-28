import asyncio
from multiprocessing import Value, Process

import cv2
import websockets
from fer import FER
from fer.utils import draw_annotations

int_smile = Value('i', 0)


def fer_app(smile):
    detector = FER(mtcnn=False)
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cap.set(cv2.CAP_PROP_FPS, 60)

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
                smile.value = 1
            else:
                smile.value = 0

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


async def is_smiling(websocket):
    while True:
        await websocket.send(str(int_smile.value))


async def main():
    async with websockets.serve(is_smiling, port=8001):
        await asyncio.Future()


if __name__ == '__main__':
    fer_pro = Process(target=fer_app, args=(int_smile,))
    fer_pro.start()
    asyncio.run(main())
