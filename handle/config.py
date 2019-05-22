#encoding:utf-8
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../module")
sys.path.append("../spath")

def getModule():
    modelfiledir = '../module/'
    # modelfile = "schoolmate_Vtest9_addnavigation.txt" #跑测试用例，增加模块间的导航
    # modelfile = "schoolmate_Vtest8_sample.txt"    # 跑测试用例，去除了关于删除的迁移
    # modelfile = "schoolmate_Vtest7.txt"     #跑测试用例生成的
    # modelfile = "FAQfoege.txt"  # 跑测试用例生成的,聚类用的
    modelfile = "webchess - v2.txt"
    # modelfile = "teacher_v3.txt"
    # modelfile = "addressbookv3.txt"
    # modelfile ="phpCSSv3.txt"
    inputfile = modelfiledir + modelfile
    return inputfile


def getUrl():
    # url = "http://127.0.0.1/schoolmate2/"  # schoolmate
    # url = "http://127.0.0.1/2faqforge_{}/"  # faqforge
    url = "http://127.0.0.1/4webchess_{}/"  #webchess
    # url ="http://127.0.0.1/1addressbook_{}/"  # addressbook
    # url="http://127.0.0.1/phpaaCMS_0.5/admin/login.php" #phpCSS
    return url

def getInstrumentFile():
    # 插桩获得的信息文件路径要与插桩路径一致
    # schoolmate
    # file = "D:\\WandS\\Graduation_Project\\webapp instrrument\\schoolmate2\\b.txt"
    # file2 = "D:\\WandS\\Graduation_Project\\webapp instrrument\\schoolmate2\\bbb.txt"
    # faqforg
    # file = "D:\\WandS\\Graduation_Project\\webapp instrrument\\2faqforge_new\\b.txt"
    # file2 = "D:\\WandS\\Graduation_Project\\webapp instrrument\\2faqforge_new\\bbb.txt"
    # redis_path = "2faqforge_{}"
    # webchess
    file = "D:\\WandS\\Graduation_Project\\webapp instrrument\\4webchess\\b.txt"
    file2 = "D:\\WandS\\Graduation_Project\\webapp instrrument\\4webchess\\bbb.txt"
    redis_path = "4webchess_{}"

    # file = "D:\\WandS\\Graduation_Project\\webapp instrrument\\1addressbook\\b.txt"
    # file2 = "D:\\WandS\\Graduation_Project\\webapp instrrument\\1addressbook\\bbb.txt"
    # redis_path = "1addressbook_{}"

    # file = "D:\\WandS\\Graduation_Project\\webapp instrrument\\phpaaCMS_0.5\\admin\\b.txt"
    # file2 = "D:\\WandS\\Graduation_Project\\webapp instrrument\\phpaaCMS_0.5\\admin\\bbb.txt"
    return file, file2, redis_path

def getRecordFundFile():
    filepath = "..\\dataset\\"  # schoolmate的
    return filepath


def getSpathFile():
    modelfiledir = '../spath/'
    # modelfile = "spath_flag_schoolmate_admin.txt"  #schoolmate
    # modelfile = "spath_flag_schoolmate_teacher.txt"
    # modelfile = "spath_flag_faqforg.txt"  # faqfore
    modelfile = "spath_flag_webchess.txt"
    # modelfile = "spath_flag_addressbook.txt"
    # modelfile = "spath_flag_phpcss.txt"
    inputfile = modelfiledir + modelfile
    return inputfile

def getPopParameter():
    # popsize不能为奇数
    # popsize = 22 #schoolmate_teacher  sensitive path has 19
    # popsize = 28 # schoolmate_admin   sensitive path has 24
    popsize = 18 #webchess   sensitive path has 12
    # popsize = 6  #faqforge   sensitive path has 3
    # popsize = 10 # addressbook sensitive path has 5
    # popsize = 26  # phpcss sensitive path has 18
    # multi_process_count 并发数，控制系统占用
    # multi_process_count = 22 #schoolmate_teacher  sensitive path has 19
    # multi_process_count = 28 # schoolmate_admin   sensitive path has 24
    multi_process_count = 6 #webchess   sensitive path has 12
    # multi_process_count = 6  #faqforge   sensitive path has 3
    # multi_process_count = 5 # addressbook sensitive path has 5
    # multi_process_count = 26  # phpcss sensitive path has 18
    pc = 0.8
    pm = 0.9
    Max = 2000
    return popsize,pc,pm,Max,multi_process_count



if __name__ == '__main__':
    getModule()