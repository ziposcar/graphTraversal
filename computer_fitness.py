# coding=utf-8
from __future__ import division
def handle_txt():
    list = []
    result = []
    f = open("D:\\wamp_php\\wamp\\www\\schoolmate2\\muser_result.txt", "r")
    lines = f.readlines()  # 读取全部内容
    for line in lines:
        line = line.strip()
        line = line.strip("\n")
        list.append(line)
    # 处理txt文本，前三行是arry数组信息，后两行是“）”非正式数据
    del list[0]
    del list[0]
    del list[0]
    list.pop()
    list.pop()
    for v in list:
        v = v.split(" => 1,")
        result.append(v[0])
    return result


def handle_target():
    target = []
    f = open("D:\\pycharm\\graphTraversal\\path_code_line_number\\mangeruser.txt", "r")
    lines = f.readlines()  # 读取全部内容
    for line in lines:
        # print line
        line = line.strip()
        target.append(line)
    # print target
    return target


def fit_individuality(excu, target):
    excu2 = []
    target2 = []
    m = []
    d = []
    mcout = 0
    c = 0
    print excu
    print target
    for i in range(len(target)):
        if target[i] in excu:
            excu2.append(1)
        else:
            excu2.append(0)
        target2.append(1)
    print excu2
    print target2
    for i in range(0,len(target2)):
        if target2[i] == excu2[i]:
            d.append(1)
            mcout = mcout + 1
            m.append(mcout)
        else:
            d.append(0)
            mcout = mcout
            m.append(mcout)
    for j in range(0,len(excu2)):
        if target2[j] == excu2[j]:
            c = c+1
        else:
            c = c
            break
    print 'd:', d
    print 'm:', m
    print 'c', c
    sum = 0
    for i in range(0, len(target2)):
        f = m[i] * d[i]
        sum = sum + f
    F = (c + 1) * sum
    print '测试用例适应度F', F
    return F


def target_fit(target):
    m = []
    d = []
    mcout = 0
    c = 0
    target2 = []
    for i in range(len(target)):
        target2.append(1)
    excu2 = target2
    for i in range(0, len(target2)):
        if target2[i] == excu2[i]:
            d.append(1)
            mcout = mcout + 1
            m.append(mcout)
        else:
            d.append(0)
            mcout = mcout
            m.append(mcout)
    for j in range(0, len(excu2)):
        if target2[j] == excu2[j]:
            c = c + 1
        else:
            c = c
            break
    print 'd:', d
    print 'm:', m
    print 'c', c
    sum = 0
    for i in range(0, len(target2)):
        f = m[i] * d[i]
        sum = sum + f
    TF = (c + 1) * sum
    print '目标适应度TF', TF
    return TF



def multi_target_fit(list_dict_trg, listpcc):#在想想
    sum = 0
    result = []
    n = len(list_dict_trg)
    for i in range(0,len(list_dict_trg)):
        s = fit_individuality(list_dict_trg[i], listpcc[i])
        result.append(s)
    print '个体适应度列表：',result
    for j in result: # 这里还要处理一下多目标路径适应度值的计算，就是怎么把多个个体fit的值传进来
        sum = sum + j
    MF = format(float(sum)/float(n),'.4f')  # 除法，要保留到4小数点位，不能用/ ,需要对数进行浮点数转换
    print '一个测试用例对多个目标的总体适应度MF', MF
    return MF

if __name__ == '__main__':

    # excu = handle_txt()
    # target = handle_target()
    # fit_individuality(excu, target)
    # target_fit(target)
    t = 1/6
    print t
    a = 1
    b = 6
    d = round(a / b, 4)
    print d