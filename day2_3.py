num = int(input())
temp = num
count = 0
digits = []
while temp > 0:
    digits.append(temp % 10)
    temp //= 10
    count += 1
print(f"位数：{count}")
print("逆序数字：", end="")
for d in digits:
    print(d, end="")
print()
