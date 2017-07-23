import svm
from svmutil import *
import os
import re
import numpy as np
from numpy import linalg as LA

def match_featfile(featfile):    #定义一个判断是否为特征文件的函数
    regex = re.compile(r"fc6-1")    #匹配fc6-1
    if re.search(regex,featfile) == None:    #如果没有匹配到
        return False
#match_featfile('000121.fc6-1')

def select_featfile(feat_files):    #定义一个筛选特征文件的函数
    for item in feat_files:
        if match_featfile(item) == False:
            feat_files.remove(item)           
    return feat_files

def get_label(trainlabel_file):    #定义一个从文件中提取label，生成list的函数
    label_list=[]     #建立一个list，用来存放label
    path_list = readpath_without_enter(trainlabel_file)    #读取到去掉回车符的每行数据
    return path_list
#get_label("trainlabel.txt")

def readpath_without_enter(routefile):    #定义一个读取路径并去掉末尾回车符的函数
    fopen = open(routefile,"r")    #打开路径清单
    path_list =  fopen.readlines()    #将每条路径都读取到一个list中，这里的每条路径字符串最后有一个回车符，需要处理掉
    fopen.close()    #关闭文件
    pathlist=[]    #建立一个空的list，准备用其存储每条路径
    for each in path_list:    #遍历每一个路径字符串，去掉末尾的回车符\n
        pathlist.append(each.replace("\n",""))    #去掉回车符
    return pathlist

def read_binary_bolb(feature_path):    #定义一个读取特征文件的函数，返回特定格式的数据
    fid = open(feature_path,'rb')      #打开特征文件
    s = np.fromfile(fid, np.int32)[0:5]    #用np方式，int32 读取特征文件
    fid.close()     #关闭文件
    m = s[0] * s[1] * s[2] * s[3] * s[4]    #得到前五项的乘积
    fid = open(feature_path,'rb')    #以二进制读取方式打开特征文件
    data = np.fromfile(fid,np.float32)[5:m+5]    #用np方式，float32打开，这里的float与matlab中转换的不同
    data = list(data)    #将数据转换成list格式
    fid.close()
    return data

def create_svm_input_data(trainroute_file):    #定义一个创建svm输入数据矩阵的函数
    dirlist=readpath_without_enter(trainroute_file)    #读取路径
    dim_feat = 4096     #维度
    data_matrix = np.zeros((len(dirlist),dim_feat))    #建立一个全0矩阵
    for item in range(len(dirlist)):     #对于每一条路径中的数据进行遍历
        data = np.load("%s/c3d_fc6.npy" % (dirlist[item]))    #读取到每一个c3d_fc6.npy文件
        normed_data = data / LA.norm(data,2)    #将一个视频提到的多帧的特征（每个帧对应一帧的特征）求二范数，然后归一化
        data_matrix[item,:] = normed_data    #循环将所有的值存入feat中
    return data_matrix     #大小为   视频样本个数 * 4096 ，即每个视频最后有  4096 * 1 的特征 
#create_svm_input_data("trainroute.txt")

def read_c3d_feat(routefile):    #定义一个读取C3D特征的函数
    dirlist=readpath_without_enter(routefile)
    dim_feat = 4096     #维度
    for item in range(len(dirlist)):    #对于每一个路径，其目录下存放了一个视频提帧后每个帧的特征，
                                        #这个循环用来计算每个视频的特征，最后得到一个c3d_fc6.npy文件
        feat_files = os.listdir(dirlist[item])  #讲一个视频的所有特征路径存储到列表
        select_featfile(feat_files)    #筛选出特征文件
        feat_files.sort()    #排序
        num_feat = len(feat_files)    #计算该视频提取到的特征个数
        feat = np.zeros((num_feat,dim_feat))    #建立一个全0矩阵
        i = 0
        for feature in feat_files:    #读取所有的特征文件，将他们的值读取到一个变量“feat”中
            feat_path = os.path.join('%s/%s'%(dirlist[item],feature))
            feat[i,:] = read_binary_bolb(feat_path)     #循环将所有的值存入feat中
            i += 1
        avg_feat = np.mean(feat,axis=0)    #求均值降维，例如   16*4096-->1*4096  18*4096-->1*4096
        avg_feat_float32 = np.float32(avg_feat)    #保证svm的输入为浮点数
        np.save("%s/c3d_fc6.npy" % (dirlist[item]),avg_feat_float32)   #将数据得到特征变量存到c3d_fc6.npy文件中
        #print(avg_feat_float32)
        #print("############################################################################################################")

#create_libsvm_fotrmat_data， "[label] valuekey1:value valuekey2:value valuekey3:value......"
def create_libsvm_format_data(route_file,label_file,train_or_test_data="data.txt"):    #定义一个将data和label转换为libsvm格式的数据的函数
    data = create_svm_input_data(route_file)    #读取数据，尺寸 =“样本数”* 4096 ，4096是C3D提取到的特征维数
    label = get_label(label_file)     #得到数据的标签
    fopen = open(train_or_test_data,'w')    #打开一个文件，准备写入libsvm格式数据
    charater_size = np.shape(data)[-1]    #求得每个特征的属性个数
    datalist = []
    for item in range(len(label)):     #对于每一个样本编上序号1-len（label）
        datalist.append(label[item])    #记录label
        for charater in range(charater_size):    #对于每一个特征
            datalist.append(" %s:%s" %(charater+1,data[item,charater])) #记录valuekey和value，value从data中读取
        datalist.append("\n")    #每条数据结尾加上回车符
    fopen.writelines(datalist)    #将记录到的每条数据都写入文件
    fopen.close()    #关闭文件
    #print(datalist)
def create_train_data(traindata_file):    #定义一个创建libsvm格式的训练数据
    create_libsvm_format_data("trainroute.txt","trainlabel.txt",traindata_file)
def create_test_data(testdata_file):       #定义一个创建libsvm格式的测试数据
    create_libsvm_format_data("testroute.txt","testlabel.txt",testdata_file)
#定义一个创建libsvm格式的数据，自定义“数据路径文件名”，“数据标签文件名”，“即将生成的libsvm格式数据文件名”
def create_single_test_data(route_file,labelfile,svm_format_data):    #定义一个创建libsvm格式的数据
    create_libsvm_format_data(route_file,labelfile,svm_format_data)  
#create_train_data("traindata.txt")
#create_test_data("testdata.txt")
#create_DIY_test_data("数据路径文件名","数据标签文件名","要生成的libsvm格式数据文件"),默认均为"diy_xxxxx.txt"
#create_DIY_data("testroute.txt","testlabel.txt")

#train_svm
def train_svm():    #定义一个训练SVM的函数
    read_c3d_feat("trainroute.txt")
    create_train_data("traindata.txt")         #创建libsvm格式的训练数据
    y,x = svm_read_problem("traindata.txt")    #调用svm库读取数据
    model = svm_train(y,x,'-c 5')    #训练svm模型
    return model

#test_svm
def single_test_svm(model,route_file="showroute.txt",labelfile="showlabel.txt",svm_format_data="showdata.txt"):    #定义一个用svm_model测试的函数
    #model = train_svm()     #即时训练
    read_c3d_feat(route_file)    #读取测试样本的特征
    create_single_test_data(route_file,labelfile,svm_format_data)    #创建libsvm格式的单个测试数据
    y,x = svm_read_problem(svm_format_data)    #libsvm读取数据
    label,acc,val = svm_predict(y,x,model)    #得到svm预测的结果
    label = int(label[0]) + 1
    print("Classified!")
    print("The video label is:",label)
    return label
#single_test_svm()

def batch_test_svm(model,route_file="testroute.txt",labelfile="testlabel.txt",svm_format_data="testdata.txt"):    #定义一个用svm_model测试的函数
    #model = train_svm()     #即时训练
    read_c3d_feat(route_file)    #读取测试样本的特征
    create_test_data(svm_format_data)    #创建libsvm格式的批量测试数据
    y,x = svm_read_problem(svm_format_data)    #libsvm读取数据
    label,acc,val = svm_predict(y,x,model)    #得到svm预测的结果
    #label = int(label[0]) + 1
    print("Classified!")
    #print("The video label is:",label)
    print("The accracy is:",acc[0])

model = train_svm()     #训练

###单个测试调用此函数，调用前确保testroute.txt 和 testlabel.txt 中内容正确
### batch_test_svm(model,route_file="testroute.txt",labelfile="testlabel.txt",svm_format_data="testdata.txt")，将会返回这批数据的准确率
batch_test_svm(model)

###单个测试调用此函数，调用前确保showroute.txt 和 showlabel.txt 中内容正确
### single_test_svm(model,route_file="showroute.txt",labelfile="showlabel.txt",svm_format_data="showdata.txt")，将会返回预测的类标
#single_test_svm(model)