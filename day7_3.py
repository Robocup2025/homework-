with open("test.txt", "r") as f:
    content = f.read()
new_content = "python" + content + "python"
with open("test_modified.txt", "w") as f:
    f.write(new_content)
print("文件修改完成")
