#encoding:utf-8

import config

def obtain_spath():
    inputfile = config.getSpathFile()
    spath = []
    f = open(inputfile, "r")
    lines = f.readlines()  # 读取全部内容
    f.close()
    for line in lines:
        line =line.strip("\n")
        spath.append(line)
    # print"敏感路径总列表",len(spath),spath
    # print len(spath)
    return spath


def build_m():
    spath = obtain_spath()
    numSPcol = len(spath)  # col:the number of sensitive path
    m = [2.0 for i in range(numSPcol)]  # m is one row which constructed of M
    return m




if __name__ == '__main__':
    a=2   #row :the number of test case
    spath=obtain_spath()
    print spath
    print len(spath)
    m=build_m()
    print m