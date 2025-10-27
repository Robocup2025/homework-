import os
import random
import string
if not os.path.exists("img"):
    os.makedirs("img")
for _ in range(100):
    filename = "".join(random.choices(string.ascii_uppercase + string.digits, k=4)) + ".png"
    with open(f"img/{filename}", "w") as f:
        pass
print("创建完成")
