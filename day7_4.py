with open("test.txt", "r") as f1, open("copy_test.txt", "r") as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()
print("不同行的编号：")
for i in range(min(len(lines1), len(lines2))):
    if lines1[i].strip() != lines2[i].strip():
        print(f"第{i+1}行")
