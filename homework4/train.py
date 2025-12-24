from ultralytics import YOLO
import os
import warnings
warnings.filterwarnings("ignore") 
DATASET_YAML = r"C:\Users\lamor\Desktop\homework4\dataset.yaml"
PRETRAINED_MODEL = "yolo11n.pt"
EPOCHS = 50            
BATCH_SIZE = 2          
IMG_SIZE = 640            
DEVICE = "cpu"          
CONF_THRESHOLD = 0.5      
if not os.path.exists(DATASET_YAML):
    raise FileNotFoundError(f"找不到dataset.yaml：{DATASET_YAML}")
print(f"配置校验通过")
print(f"数据集配置：{DATASET_YAML}")
print(f"训练参数 - 轮数：{EPOCHS} | 批次：{BATCH_SIZE} | 尺寸：{IMG_SIZE} | 设备：{DEVICE}")
model = YOLO(PRETRAINED_MODEL)
print(f"成功加载预训练模型：{PRETRAINED_MODEL}")
print("\n=== 开始训练YOLO11模型 ===")
results = model.train(
    data=DATASET_YAML,
    epochs=EPOCHS,
    batch=BATCH_SIZE,
    imgsz=IMG_SIZE,
    device=DEVICE,
    conf=CONF_THRESHOLD,
    lr0=0.01,            
    augment=True,         
    patience=10,           
    save=True,              
    project="runs/detect",  
    name="train",           
    exist_ok=True,         
    verbose=True           
)
print("\n=== 开始验证模型 ===")
metrics = model.val()
print(f"训练完成！")
print(f"验证集指标 - mAP@0.5：{metrics.box.map50:.4f} | mAP@0.5:0.95：{metrics.box.map:.4f}")
print(f"最佳模型保存路径：{os.path.join('runs/detect/train/weights/best.pt')}")