import random
with open("data.txt", "w") as f:
    for _ in range(100000):
        f.write(str(random.randint(1, 100)) + "\n")
print("随机数data.txt创建完成")
