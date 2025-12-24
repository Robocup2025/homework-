import cv2
from ultralytics import YOLO
import os
import numpy as np
MODEL_PATH = r"C:\Users\lamor\Desktop\homework4\runs\detect\train\weights\best.pt"
VIDEO_PATH = r"C:\Users\lamor\Desktop\homework4\VID_20251224_174320.mp4"
OUTPUT_VIDEO_PATH = r"C:\Users\lamor\Desktop\detection_demo.mp4"
CLASS_NAMES = [
    "binghongcha",    
    "sprite" 
]
CONF_THRESHOLD = 0.5
model = YOLO(MODEL_PATH)
print(f"成功加载模型：{MODEL_PATH}")
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise ValueError(f"无法打开视频文件：{VIDEO_PATH}，请检查路径是否正确")
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"成功加载视频：{VIDEO_PATH}")
print(f"视频参数 - 分辨率：{width}x{height} | 帧率：{fps} | 总帧数：{total_frames}")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (width, height))
cv2.namedWindow("YOLO11 矿泉水瓶检测（视频版）", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLO11 矿泉水瓶检测（视频版）", width, height)
print("\n开始检测视频，按Q键可提前退出")
frame_idx = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break 
    results = model(frame, conf=CONF_THRESHOLD)
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                cls_name = CLASS_NAMES[cls_id]
                conf = float(box.conf[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{cls_name} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                print(f"【帧{frame_idx}】{cls_name} | 置信度：{conf:.2f} | 检测框：({x1},{y1})-({x2},{y2}) | 中心坐标：({center_x},{center_y})")
    out.write(frame)
    cv2.imshow("YOLO11 矿泉水瓶检测（视频版）", frame)
    frame_idx += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n  按Q键提前退出检测")
        break
cap.release()
out.release()
cv2.destroyAllWindows()
print(f"检测帧数：{frame_idx}/{total_frames}")
print(f"结果视频保存至：{OUTPUT_VIDEO_PATH}")