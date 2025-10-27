import os
import random
files = os.listdir("img")
for filename in random.sample(files, 50):
    if filename.endswith(".png"):
        new_name = filename[:-4] + ".jpg"
        os.rename(f"img/{filename}", f"img/{new_name}")
print("50个文件已改为.jpg结尾")
