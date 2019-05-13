#encoding:utf-8
import GAalgor
from SAalgor import SA
from HCalgor import HC
from GAalgor import GA
import GreedyAlgor
import generate_data_ga
from datetime import datetime
import recordFun
from random import choice

def selectCandidate(pop,testdata,M,p):
    CandidataSet_seq = {}
    CandidataSet_date = {}
    for i in range(len(M)):
        if M[i][p] > 0.0 and M[i][p] < 2:
            CandidataSet_seq[i] = pop[i]
            CandidataSet_date[i] = testdata[i]
            #少了排序
    print" CandidataSet_seq", CandidataSet_seq
    print " CandidataSet_data",CandidataSet_date
    return CandidataSet_seq,CandidataSet_date


def Local_search_for_SA(pop,testdata,M,Uncover_path_list,SM):
    startTime = datetime.now()
    # Uncover_path_list存放的是敏感路径对应的index编号,p=7,对应spath中索引为7的路径user1
    # 本文方法SA
    afterLocalUnCoverPath = []
    overgame = 0
    for p in Uncover_path_list:
        p_solve = 0 # 经过局部搜索是否找到覆盖路径P的测试数据
        # CandidataSet_seq, CandidataSet_date = selectCandidate(pop, testdata, M, p)
        CandidataSet_seq={0:['T56', 'T94', 'T60', 'T61', 'T84'],1:['T56', 'T94', 'T60', 'T61', 'T84']}
        CandidataSet_date = {0:['nZ6k7s', 'f6MC6f', 'bmeL24', '0V2g3N'],1:['nE48Rm', 'q5A6Ur', 'NYUo1U', 'Wv3S36', 'Qbxkl6', 'x63KD2', 'U9mX9v']}
        for key,value in CandidataSet_seq.items():
            #value就是个体，key是个体在pop中的index
            print"value", value
            varname, pathVarType = generate_data_ga.obtain_var_from_path(SM,value)
            saSample = SA(pathVarType, value, SM.TEvent,CandidataSet_date[key],p)  # 初始化SA类为实例saSample
            searchFlag,data = saSample.SAOptimize()
            # 置标识searchFlag ，searchFlag = 1搜到，=0，没搜索到
            if searchFlag == 1:   #  更新pop,序列seq不变，对应的testdata更新
                testdata[key] =data
                p_solve = 1
        if p_solve == 0:
            afterLocalUnCoverPath.append(p)
    endTime = datetime.now()
    usertime = endTime - startTime
    print "局部搜索用时：",usertime
    recordFun.recordLocalUserTime(usertime)
    if len(afterLocalUnCoverPath)==0:
        overgame = 1
    else:
        recordFun.recordLocalUnCoverPath(afterLocalUnCoverPath)
    return overgame,testdata


#爬山，对未被覆盖的敏感路径，随机选择一个个体，进行测试数据的生成
def Local_search_for_HC(pop,testdata,M,Uncover_path_list,SM):
    startTime = datetime.now()
    afterLocalUnCoverPath = []
    overgame = 0
    for p in Uncover_path_list:
        p_solve = 0 # 经过局部搜索是否找到覆盖路径P的测试数据
        # seq = choice(pop) #随机选择一个个体
        seq=['T46', 'T47', 'T48', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T81']
        index = pop.index(seq)
        p_fit_current = M[index][p]
        print "p_fit_current",p_fit_current
        varname, pathVarType = generate_data_ga.obtain_var_from_path(SM, seq)
        hcSample = HC(pathVarType, seq, SM.TEvent, testdata[index],p,p_fit_current)  # 初始化SA类为实例saSample
        searchFlag, data = hcSample.HCOptimize()
        # 置标识searchFlag ，searchFlag = 1搜到，=0，没搜索到
        if searchFlag == 1:  # 更新pop,序列seq不变，对应的testdata更新
            testdata[index] = data
            p_solve = 1
        if p_solve == 0:
            afterLocalUnCoverPath.append(p)
    endTime = datetime.now()
    usertime = endTime - startTime
    print "局部搜索用时：",usertime
    recordFun.recordLocalUserTime(usertime)
    if len(afterLocalUnCoverPath)==0:
        overgame = 1
    else:
        recordFun.recordLocalUnCoverPath(afterLocalUnCoverPath)
    return overgame,testdata

#遗传，对未被覆盖的敏感路径，随机选择一个个体，生成一个测试数据的子种群
def Local_search_for_GA(pop,testdata,M,Uncover_path_list,SM):
    startTime = datetime.now()
    afterLocalUnCoverPath = []
    overgame = 0
    for p in Uncover_path_list:
        p_solve = 0  # 经过局部搜索是否找到覆盖路径P的测试数据
        seq = choice(pop) #随机选择一个个体
        # seq = ['T46', 'T47', 'T48', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T81']
        index = pop.index(seq)
        p_fit_current = M[index][p]
        print "p_fit_current", p_fit_current
        varname, pathVarType = generate_data_ga.obtain_var_from_path(SM, seq)
        gaSample = GA(pathVarType, seq, SM.TEvent, p, p_fit_current)  # 初始化GA类为实例gaSample
        searchFlag, data = gaSample.geneticoptimize()
        # 置标识searchFlag ，searchFlag = 1搜到，=0，没搜索到
        if searchFlag == 1:  # 更新pop,序列seq不变，对应的testdata更新
            testdata[index] = data
            p_solve = 1
        if p_solve == 0:
            afterLocalUnCoverPath.append(p)
    endTime = datetime.now()
    usertime = endTime - startTime
    print "局部搜索用时：", usertime
    recordFun.recordLocalUserTime(usertime)
    if len(afterLocalUnCoverPath) == 0:
        overgame = 1
    else:
        recordFun.recordLocalUnCoverPath(afterLocalUnCoverPath)
    return overgame, testdata



if __name__ == '__main__':
    import obtain_efsm_info2
    SM = obtain_efsm_info2.obtain_efsm()
    SM.allPathNum()
    pop = [['T27', 'T28', 'T29', 'T90', 'T41', 'T42', 'T43', 'T44', 'T45', 'T91', 'T51', 'T52', 'T53', 'T92', 'T82'],
           ['T27', 'T28', 'T29', 'T32', 'T33', 'T34', 'T35', 'T36', 'T79'],
           ['T3', 'T87', 'T16', 'T17', 'T18', 'T14', 'T15', 'T88', 'T22', 'T23', 'T89', 'T28', 'T29', 'T90', 'T80'],
           ['T11', 'T14', 'T15', 'T12', 'T13', 'T16', 'T17', 'T18', 'T77'],
           ['T11', 'T16', 'T17', 'T18', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
           ['T3', 'T87', 'T12', 'T13', 'T77'],
           ['T19', 'T24', 'T25', 'T26'],
           ['T54', 'T55', 'T55', 'T82'],
           ['T3', 'T87', 'T12', 'T13', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
           ['T59', 'T62', 'T63', 'T62', 'T63', 'T64', 'T65', 'T66', 'T84'],
           ['T46', 'T47', 'T48', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T81'],
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
           ['T3', 'T4', 'T5', 'T8', 'T9', 'T10']]
    M =[[2, 2, 2, 2, 2, 2, 0.0, 0.0, 2, 2, 0.0, 2, 0.0, 2, 2, 2, 2, 0.0, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 0.0, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 0.0, 2, 2, 0.0, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 0.0, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2, 2, 0.0, 0.0, 2],
        [2, 2, 0.0, 0.0, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 0.0, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1.004950495049505, 0.0, 0.0, 2],
        [2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1.004950495049505, 0.0, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 0.0, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 0.0, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1.00990099009901, 0.0, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.504950495049505, 0.0, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 0.0],
        [2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 0.0, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 0.0, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 0.0],
        [2, 2, 2, 2, 2, 2, 0.0, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2],
        [0.0, 0.0, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2]]
    popp=[['T56', 'T94', 'T60', 'T61', 'T84'],['T56', 'T94', 'T60', 'T61', 'T84']]
    testdata = [['cqmh9B', 'nFwSr2', 'mA42cl', '8JE1Sr', 'N8vv5G', 'Afy6lz', '6WpWWQ', 'F7Oq72', '6u7cII', 'YiTrNI', 'FVuc65'],
                ['vOIsrG', 'TbYzOS', 'A0h9yk', 'IGv0uR', 'cHOaEr', 'PZ3ybp', 'RoBJ0L', '4xljm2'],
                ['DkLC36', 'VW3qBm', 'Da7yrc', '2h8rh0', 'mGtWk6', 'YhMzFA', 'zNs2v0', 'j5j85e', 'm54xBB', '8OG2wn'],
                ['z581lZ', '0u341D', '152YFl', 'R46d07', 'k8t0Wv', 'lgk1gq', 'S38WG3', 'HlURvz', 'TvFfqp', 'Na8rh8', 'ZToErZ', '59jAih'],
                ['ZEELgQ', 'zj2Azi', '4hI8cz', '5X63oR', '8r784B', 'TzQlI6'],
                ['99s30n', 'jA3a20', '8T72G2', 'm0RHpZ', '6F1038', 'w75gVs', 'ox07CX', 'by6636', 'Q3O93o', 'LkuL68', '070q9S', 'ECCC43'],
                ['3Yfg0o', 's8YVev', '03xdOY', 'uxHZKW', '0G3bh1', 'E34914'],
                ['6Wv0Mp', '9g6akD', 'viOxYw', 'f6lNDB', '6M07Uy', '81qW2F', 'y6w766'],
                ['8FSG3T', 'C7iwB7', 'W17131', '77UT4i', '691p4N', 'g6IHrt'],
                ['cJ6SzC', 'DZVl1R', 'I6d30Z', '992cfC', 'f9T51j', '72NC68', '0QN6VC', 'Nfgc0L', 'dJ625U', 'OTSg54', 'hJTW2g', '2x3bKP'],
                ['0in7Zq', '089Ovq', 'mgL0L4', 'JAgolr'],
                ['KygMj7', 'mBghB9', 'pGHWs8', 'NDQC3c', 'S1sLcO', '69BbG8'],
                ['f83YY1', '9xdi5O', '74x02T', 'G4TR7B', 'OlvHct', '19oTXc', '2sEU26', 'ivL3x5', 'PnHzo6', 'z1Orq5', '57jK2Y', '8R2bO2'],
                ['5yCV8v', '7r4vaj', 'w6279r', '9q6f2Z', 'k7Y8y8', 'gbqR92'],
                ['24s4QZ', 'O8YCy9', 'hll20B', 'W4YKV7', 'C9qEcE', '8PTVO5', 'p84Wq6'],
                ['0w1p58', '01nxCE', 'a5t3pF', '4QR826'], ['36qyCg', 'KS54Qg', '6JTa2M'],
                ['8q0r36', '0bk8h4', '702iz6', 'mHGre7', 'jXcJkT', 'jGYU0l', '9BiXE8'],
                ['9Ae404', 'U46Aq0', 'HyM10S', 'T73623', '06TV4K', '3G7l29', 't75Yip', 'Dym11w', '6uE3Wy', '5qQ28Y', '86VBou', 'h781yU', 'e53B77', 'JOkpD4', 'eJU719', 'fBD77F'],
                ['M69431', 'u3fQ8c', 'V2618d', '8VlRLU', '52s5A6', 'g8p8HE', '33BEDz', 'YNMSUb', '0y6NMq', '368j1h', 'i8p5Gs', 'gGGf3f'],
                ['TbthsR', 'vQ8twF', 'xF6nGL', 'sS22Tn', 'YRMkCw', '600LdJ', 'cTf1UZ', '42PqNS'],
                ['okUJID', 'OZrVDP', '4y1D5v', 'aS7Ap4', 'a9s2XK', '330hQT', 'qWmZ36', 'Bop68b', '6B0412', 'am4g7h', '8z8F17', 'o1WzvA'],
                ['4648nf', 'hhYhvH', '1mt0Tn', 'kc099l', '3V0F8s', '1jU6ZS', 'Ck3749', '53r7b5', 'B08OV4', '07ug8m', 'wsKlD8', '0KLZ6j'],
                ['zaizJz', 'zT6FJ7', 'o50CeK', '9eP66d', 'AxNt42', 'D6q4w8'],
                ['WH00NA', 'Yp3sTx', 'nypRCd', '9kz6kn', 'n74CmY', 'W39091', 'DKUh14', '8Bmt1y', '9r23nu', 'LMOF75', '4Hr18u', '6Lm7G1'],
                ['db8ntJ', 'sf9P37', 'pzdHa2', 'sXXSaJ'],
                ['YENBVh', 'fDx19u', 'S8jRjN', '2xNn0l'],
                ['xlZxTd', '2XyFkw', 'Q2TS2u', 'ley17u', 'aso02v', 'CgMJP2', 'JouQ10', '6aGHfT', 'S2RQU6', 'QWnTid', 'GdJt2B', '3qNKaS'],
                ['8x7bRk', '6tWgBL', 'r45rau'],
                ['0i6k5j', '4uF866', 'jX4Gb4', '8lvXTx', '7wMGj8', 'YO8ToL']]
    Uncover_path_list =[11, 18]
     # Local_search_for_SA(popp,testdata,M,Uncover_path_list,SM)
    # Local_search_for_HC(pop,testdata,M,Uncover_path_list,SM)
    Local_search_for_GA(pop,testdata,M,Uncover_path_list,SM)