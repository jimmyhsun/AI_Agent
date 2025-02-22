import cv2
from ultralytics import YOLO
import time
from tts import play_sound

model = YOLO("yolov8n.pt")

def count_people():
    cap = cv2.VideoCapture(0)  # 開啟攝影機
    if not cap.isOpened():
        print("無法開啟攝影機")
        return
    start_time = None  # 記錄偵測開始時間
    detected_people = 0  # 儲存最後偵測到的人數

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取畫面")
            break

        # 進行人數偵測
        results = model(frame)  # 取得 YOLO 偵測結果
        count = 0

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if cls == 0:
                    count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 顯示人數
        cv2.putText(frame, f"People: {count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Camera", frame)

        if count > 0:
            if start_time is None:
                start_time = time.time()  # 記錄開始時間
                detected_people = count  # 儲存人數

            # 若超過 2 秒，則關閉視窗並播報人數
            if time.time() - start_time >= 2:
                print(f"偵測到 {detected_people} 人，關閉攝影機。")
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 手動關閉
            break

    cap.release()
    cv2.destroyAllWindows()

    if detected_people > 0:
        play_sound(f"現場有 {detected_people} 人")

# count_people()
