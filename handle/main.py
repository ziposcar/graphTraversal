#encoding:utf-8
from __future__ import division
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../module")
from datetime import datetime
import obtain_efsm_info2    # 模型处理器
import generate_seq_ga_check  # 序列生成器-----产生覆盖敏感路径的序列
import execute
import local_search_alg
import recordFun
import config
def main():

    SM = obtain_efsm_info2.obtain_efsm()
    popsize,pc,pm,Max,_ = config.getPopParameter()
    startTime = datetime.now()
    pop = generate_seq_ga_check.initialpop_feasible(popsize, SM)
    ''' pop =[['T27', 'T28', 'T29', 'T90', 'T41', 'T42', 'T43', 'T44', 'T45', 'T91', 'T51', 'T52', 'T53', 'T92', 'T82'],
          ['T27', 'T28', 'T29', 'T32', 'T33', 'T34', 'T35', 'T36', 'T79'],
          ['T3', 'T87', 'T16', 'T17', 'T18', 'T14', 'T15', 'T88', 'T22', 'T23', 'T89', 'T28', 'T29', 'T90', 'T80'],
          ['T11', 'T14', 'T15', 'T12', 'T13', 'T16', 'T17', 'T18', 'T77'],
          ['T67', 'T68', 'T69', 'T68', 'T69', 'T72', 'T73', 'T74', 'T85'],
          ['T11', 'T16', 'T17', 'T18', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
          ['T3', 'T87', 'T12', 'T13', 'T77'],
          ['T19', 'T24', 'T25', 'T26'],
          ['T54', 'T55', 'T55', 'T82'],
          ['T3', 'T87', 'T12', 'T13', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
          ['T59', 'T62', 'T63', 'T62', 'T63', 'T64', 'T65', 'T66', 'T84'],
          ['T11', 'T12', 'T13', 'T77'],
          ['T46', 'T47', 'T48', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T81'],
          ['T67', 'T68', 'T69', 'T68', 'T69', 'T72', 'T73', 'T74', 'T85'],
          ['T19', 'T20', 'T21', 'T78'],
          ['T59', 'T60', 'T61', 'T84'],
          ['T38', 'T43', 'T44', 'T45', 'T80'],
          ['T19','T24','T25','T26'],
          ['T27', 'T28', 'T29', 'T28', 'T29', 'T28', 'T29', 'T28', 'T29', 'T79'],
          ['T46', 'T51', 'T52', 'T53', 'T47', 'T48', 'T51', 'T52', 'T53', 'T49', 'T50', 'T92', 'T82'],
          ['T27', 'T28', 'T29', 'T32', 'T33', 'T34', 'T35', 'T36', 'T79'],
          ['T46', 'T47', 'T48', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T81'],
          ['T1', 'T2', 'T75'],
          ['T11', 'T12', 'T13', 'T88', 'T78'],
          ['T11', 'T14', 'T15', 'T12', 'T13', 'T16', 'T17', 'T18', 'T77'],
          ['T59', 'T60', 'T61', 'T84'],
          ['T19', 'T22', 'T23', 'T22', 'T23', 'T89', 'T32', 'T33', 'T37', 'T79'],
          ['T1', 'T2', 'T75'], ['T38', 'T39', 'T40', 'T80'],
          ['T3', 'T4','T5', 'T8','T9', 'T10']]'''
    '''pop = [
           ['T27', 'T28', 'T29', 'T90', 'T41', 'T42', 'T43', 'T44', 'T45', 'T91', 'T51', 'T52', 'T53', 'T92', 'T82'],
           ['T27', 'T28', 'T29', 'T32', 'T33', 'T34', 'T35', 'T36', 'T79'],
           ['T3', 'T87', 'T16', 'T17', 'T18', 'T14', 'T15', 'T88', 'T22', 'T23', 'T89', 'T28', 'T29', 'T90', 'T80'],
           ['T11', 'T14', 'T15', 'T12', 'T13', 'T16', 'T17', 'T18', 'T77'],
           ['T11', 'T16', 'T17', 'T18', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
           ['T3', 'T87', 'T12', 'T13', 'T77'],
           ['T19', 'T24', 'T25', 'T26'],
           ['T54', 'T55', 'T55', 'T82'],
           ['T3', 'T87', 'T12', 'T13', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
           ['T67', 'T68', 'T69', 'T68', 'T69', 'T72', 'T73', 'T74', 'T85'],
           ['T19', 'T20', 'T21', 'T78'],
           ['T59', 'T60', 'T61', 'T84'],
           ['T38', 'T43', 'T44', 'T45', 'T80'],
           ['T46', 'T51', 'T52', 'T53', 'T47', 'T48', 'T51', 'T52', 'T53', 'T49', 'T50', 'T92', 'T82'],
           ['T46', 'T47', 'T48', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T81'],
           ['T1', 'T2', 'T75'],
           ['T11', 'T12', 'T13', 'T88', 'T78'],
           ['T19', 'T22', 'T23', 'T22', 'T23', 'T89', 'T32', 'T33', 'T37', 'T79'],
           ['T38', 'T39', 'T40', 'T80'],
           ['T56', 'T57', 'T58','T94'],
           ['T3', 'T4', 'T5', 'T8', 'T9', 'T10'],
           ['T56','T57','T58'],
           ['T4 6', 'T47', 'T48', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T81'],
          ['T59', 'T62', 'T63', 'T62', 'T63', 'T64', 'T65', 'T66', 'T84'],
          ]'''
    # pop = [
    #        ['T3', 'T27', 'T28', 'T30', 'T31', 'T79'],
    #        ['T5', 'T67', 'T37', 'T38', 'T37', 'T39'],
    #      ]
    strf = " 初始种群"
    recordFun.recordInitalPop(strf,pop)
    print " 种群为： "
    for sub in pop:
        print sub
    with open("d:\\test\\phpaaCMS\\pop.txt") as f:
        popsf = f.read()
    import copy
    pops = [[sub.replace("['", "").replace("']", "").split("', '") for sub in poptext.split("\n")[1:]] for poptext in popsf.split("=====================================\n")[:-1]]
    for pop in pops:
        pop = sorted(pop, key=lambda sub: -len(sub))
        st = datetime.now()
        testdata, M = execute.gdata(pop, copy.deepcopy(SM))
        et = datetime.now()
        with open("d:\\test\\phpaaCMS\\multi_process.dat", "a+") as f:
            f.write("{}\n".format((et-st).total_seconds()))
    return
    pop = sorted(pop, key=lambda sub: -len(sub))
    testdata, M = execute.gdata(pop, SM)  # 为序列产生数据，执行测试用例，获取评估矩阵M
    print " 通过M获得所有敏感路径入口点覆盖标识cover_flag及敏感路径完全覆盖标识flag"
    flag, cover_flag = execute.table_handle(M)
    # print "敏感路径入口点覆盖标识cover_flag = ",cover_flag
    # print "敏感路径完全覆盖标识flag = ", flag
    coverage, Uncover_path_list = execute.table_coverage(M)
    ######################## 以上为评估初始种群############################
    iteration = 0
    while True:
        recordFun.recordPathCover(iteration, coverage, Uncover_path_list)
        recordFun.recordAllM(iteration,M)
        if iteration > Max:
            break
        # 先判断种群是否覆盖所有入口点
        print " 敏感路径入口点覆盖标识cover_flag = ", cover_flag
        print " 敏感路径完全覆盖标识flag = ", flag
        if cover_flag == 1:  # 如果覆盖了所有敏感路径的入口点
            if flag == 1:  # 在判断是否覆盖所有的敏感路径
                testcase = zip(pop, testdata)  # 测试用例等于序列+数据
                print testcase
                break
            else:  # 进行局部搜索
                print " 第",iteration , "代" + "进行局部搜索"
                print " 进入局部搜索的pop", pop
                print " 进入局部搜索的testdata", testdata
                print " 进入局部搜索的M", M
                print " 进入局部搜索的Uncover_path_list", Uncover_path_list
                # 局部算法接口在这调用
                print "Uncover_path_list"
                # overgame,testdata = local_search_alg.Local_search_for_SA(pop,testdata,M,Uncover_path_list,SM)
                # overgame,testdata = local_search_alg.Local_search_for_HC(pop,testdata,M,Uncover_path_list,SM)
                overgame, testdata = local_search_alg.Local_search_for_GA(pop, testdata, M, Uncover_path_list, SM)
                if overgame == 1:
                    testcase = zip(pop, testdata)  # 测试用例等于序列+数据
                    print testcase
                    break # 退出while ，执行下面的时间记录代码
                else:
                    tip = " 搜索失败，结束"
                    print tip
                    return tip  #退出整个程序，不会执行下面的时间记录代码了
        else:
            print " 继续全局GA，搜序列"
            pop,M,testdata,cflag = generate_seq_ga_check.GA(pop, pc, pm, popsize, SM, M,testdata)
            if cflag == 1:
                testcase = zip(pop, testdata)  # 测试用例等于序列+数据
                print testcase
                break
            else:
                flag, cover_flag = execute.table_handle(M)
                coverage, Uncover_path_list  = execute.table_coverage(M)
            iteration += 1
            #得到新的flag, cover_flag后，这里会直接到while True那句话再开始
    endTime = datetime.now()
    usertime = endTime - startTime
    # recordFun.recordAllUserTime(usertime)


if __name__ == '__main__':  # not execute when import as a module
    main()
    # table = []
    # print len(table)
    # t = [ 2, 0.0, 1.004950495049505, 0.0, 0.8544139861204133]
    # for i in range(2):
    #     table.append(t)
    # print table
