import os



# path = os.path.dirname(__file__)
# base = "{}\\resource".format(path)

# files = [os.path.join(base, file) for file in os.listdir(base)]

# # 遍历文件列表，输出文件名
# for file in files:
#     print(file)
#     tmpList = str.split(file, " ")
#     newfile = "{}\\{}".format(base, tmpList[-1])

#     os.rename(file, newfile)

def getFileList(name):
    path = os.path.dirname(__file__)
    base = "{}\\resource".format(path)
    files = [[file,os.path.join(base, file)] for file in os.listdir(base)]
    retnList = []
    for file in files:
        tmpList = str.split(file[0], "-")
        if  tmpList[0] is name:
            retnList.append(file[1])

    return retnList


if __name__ == "__main__":
    getFileList("36")