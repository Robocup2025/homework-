if __name__ == "__main__":
    lst = list(range(1000))
    for idx in range(len(lst)-1, -1, -1):
        if lst[idx] % 2 == 1:
            lst.pop(idx)
#原代码错误原因：正向遍历列表时删除元素会导致索引与元素对应关系错乱
