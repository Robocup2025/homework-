import random
with open("data.csv", "w") as f:
    for _ in range(10):
        row = [str(random.randint(1, 100)) for _ in range(3)]
        f.write(",".join(row) + "\n")
second_column = []
with open("data.csv", "r") as f:
    for line in f:
        second_column.append(int(line.split(",")[1]))
max_val = max(second_column)
min_val = min(second_column)
avg_val = sum(second_column) / len(second_column)
second_column.sort()
median_val = second_column[len(second_column)//2]
print(f"第二列最大值：{max_val}")
print(f"第二列最小值：{min_val}")
print(f"第二列平均值：{avg_val:.2f}")
print(f"第二列中位数：{median_val}")
