import random
import string
lines = int(input("行数："))
with open("test.txt", "w") as f:
    for _ in range(lines):
        line = "".join(random.choices(string.printable.strip(), k=20))
        f.write(line + "\n")
with open("test.txt", "r") as src, open("copy_test.txt", "w") as dst:
    dst.write(src.read())
print("文件复制完成")
