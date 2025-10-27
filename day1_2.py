x = int(input("x: "))
y = int(input("y: "))
z = int(input("z: "))
if x > y:
    x, y = y, x
if x > z:
    x, z = z, x
if y > z:
    y, z = z, y
print(f"从小到大排序：{x}, {y}, {z}")
