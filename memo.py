
import os
def wmemo(content):
    with open('./memo_history.log', 'a+') as f:
        f.write(content+"\n")

def readlast():
    global index
    global lines
    lines = []
    index=-1
    if not os.path.exists("./memo_history.log"):
        return None
    with open('./memo_history.log', 'r') as f:
        line = f.readline()  # 调用文件的 readline()方法
        while line:
            lines.append(line)
            line = f.readline()
    return lines[index]

def next():
    global index
    global lines
    index+=1
    if index == len(lines):
        index = -1
    return lines[index]
