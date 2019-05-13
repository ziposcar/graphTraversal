#encoding:utf-8
import config
filepath =config.getRecordFundFile()



def recordPathCover(iteration,coverage,uncoverlist):
    name = "pathCover.txt"
    file = filepath + name
    f = open(file, "a+")
    f.writelines("第" + str(iteration) + "代 ")
    f.writelines("种群的路径覆盖率: "+str(coverage) + "\n")
    f.writelines("未覆盖的路径： "+str(uncoverlist) + "\n")
    f.write("=====================================\n")
    f.close()


def recordAllM(iteration,M):
    name = "M.txt"
    file = filepath + name
    f = open(file, "a+")
    f.writelines("第" + str(iteration) + "代 " + "\n")
    for l in M:
        f.write(str(l) + "\n")
    f.write("=====================================\n")
    f.close()




def recordLocalUserTime(usertime):
    name = "LocalUserTime.txt"
    file = filepath + name
    f = open(file, "a+")
    f.writelines("总用时" + str(usertime) + "\n")
    f.write("=====================================\n")
    f.close()


def recordLocalUnCoverPath(ucp):
    name = "UncoverPafterLocal.txt"
    file = filepath + name
    f = open(file, "a+")
    for p in ucp:
        f.writelines( str(p) +"\n")
    f.write("=====================================\n")
    f.close()


def recordTestCase(i,path,test_fit,coverage):
    name = "RunningTestCase.txt"
    file = filepath + name
    f = open(file, "a+")
    f.write("第"+str(i)+"个测试用例"+str(path) + "\n")
    f.write("个体覆盖路径情况："+str(test_fit) + "\n")
    f.write("个体覆盖率：" + str(coverage) + "\n")
    f.write("================================================" + "\n")
    f.close()


def recordTestCaseRunTime(time):
    name = "TestCaseRunTime.txt"
    file = filepath + name
    f = open(file, "a+")
    f.write(str(time) + "\n")
    f.write("================================================" + "\n")
    f.close()


def recordCoverPath(pathlist):
    name = "SpathCover.txt"
    file = filepath + name
    f = open(file, "a+")
    f.write(str(pathlist) + "\n")
    f.write("================================================" + "\n")
    f.close()


def recordInitalPop(strf,pop):
    name = "pop.txt"
    file = filepath + name
    f = open(file, "a+")
    f.writelines(strf + "\n")
    for op in pop:
        f.write(str(op) + "\n")
    f.write("=====================================\n")
    f.close()
if __name__ == '__main__':
    pathindex = 1
    count = 9
    # recordSAcount(pathindex,count)