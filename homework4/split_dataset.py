import os
import random
import shutil
def split_dataset(img_dir, label_dir, save_root, train_ratio=0.8, val_ratio=0.1):
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(save_root, "images", split), exist_ok=True)
        os.makedirs(os.path.join(save_root, "labels", split), exist_ok=True)
    img_list = [f for f in os.listdir(img_dir) if f.endswith((".jpg", ".png"))]
    random.shuffle(img_list) 
    train_num = int(len(img_list) * train_ratio)
    val_num = int(len(img_list) * val_ratio)
    for i, img_name in enumerate(img_list):
        label_name = img_name.replace(".jpg", ".txt").replace(".png", ".txt")
        if i < train_num:
            split = "train"
        elif i < train_num + val_num:
            split = "val"
        else:
            split = "test"
        shutil.copy(
            os.path.join(img_dir, img_name),
            os.path.join(save_root, "images", split, img_name)
        )
        if os.path.exists(os.path.join(label_dir, label_name)):
            shutil.copy(
                os.path.join(label_dir, label_name),
                os.path.join(save_root, "labels", split, label_name)
            )
if __name__ == "__main__":
    img_dir = os.path.join("dataset", "images")
    label_dir = os.path.join("dataset", "labels")
    save_root = os.path.join("dataset", "yolo_format")
    split_dataset(img_dir, label_dir, save_root)