import cv2
import os

def video2images(video_path, save_dir, frame_interval=5):
    os.makedirs(save_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    save_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            save_path = os.path.join(save_dir, f"{save_idx:06d}.jpg")
            cv2.imwrite(save_path, frame)
            save_idx += 1
        frame_idx += 1
    cap.release()
if __name__ == "__main__":
    video_path = "C:/Users/lamor/Desktop/homework4/VID_20251224_174320.mp4"
    save_dir = os.path.join("dataset", "images")
    video2images(video_path, save_dir, frame_interval=5)