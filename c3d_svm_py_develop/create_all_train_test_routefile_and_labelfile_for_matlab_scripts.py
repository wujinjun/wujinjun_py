#Usage：“数据集提取出特征的路径”“route.txt” “选取item总数”
#Example：get_routefile('/samba/HDD/output_20170117_error/c3d/','route.txt',10)
#Usage： “route.txt”，"trainroute.txt", "trainlabel.txt"， “item起始序号” “item结束序号”
#Example: train_route_label("route.txt","trainroute.txt","trainlabel.txt",1,7)
#Usage： “route.txt”，"testroute.txt", "testlabel.txt"， “item起始序号” “item结束序号”
#Example: test_route_label("route.txt","testroute.txt","testlabel.txt",8,10)
#Author：Wu jinjun
import re
def recog_class(string):    #定义一个从路径中读取label的函数
    regex1 = re.compile(r"class_\d+")    #定义 提取出类关键字 的正则表达式
    str_num = re.findall(regex1,string)[-1]    #查找string中的 class_* 关键字
    regex2 = re.compile(r"class_*")    #定义 从class_* 中提取数字的正则表达式
    int_num=int(re.split(regex2,str_num)[-1])    #提取出label并转存为int型
    return int_num
def match_subject(string,subject_num):
    regex = re.compile(r"subject_*")    #匹配subject_后的数字
    int_num=int(re.split(regex,string)[-1])    #将匹配到的str型数字转为int型,即将数据切片得到最后的数字
    if int_num <= subject_num:  #如果小于期望值
        return True
    else:
        return False
def match_item(string,floor,ceiling):    #定义一个匹配item的函数,可以规定上限和下限
    regex = re.compile(r"subject_*")    #匹配subject_后的数字
    int_num=int(re.split(regex,string)[-1])    #将匹配到的str型数字转为int型,即将数据切片得到最后的数字
    if int_num <= ceiling and int_num >= floor:  #如果小于期望值
        return True
    else:
        #print("Wrong floor or ceiling number!")
        return False

import os
def get_routefile(basepath,route_filename,subject_number):    #basepath是数据集的路径，filename是目标存储文件名
    fopen = open(route_filename,'w')    #打开文件准备写入
    classlist =  os.listdir(basepath)    #将basepath下的文件遍历并存入classlist
    label = 0  
    classlist.sort()    #按照类别的首字母排序
    for classvar in classlist:    #for数据集下的每个类    
        videodir = os.path.join('%s%s' % (basepath,classvar))
        if os.path.isdir(videodir) == True:    #判断该条目是否是文件夹
            if match_subject(videodir,subject_number)==True:   #判断条目是否符合筛选条件             
                videolist = os.listdir(videodir)    #将video条目存入videolist
                fopen.write('%s\n' % (videodir))    #将条目写入文件
                #print(videodir)
        else:
            #print(videodir,"is not a directory, skiped!")
            continue
        label=label+1
    fopen.close()

def train_route_label(route,trainroute,trainlabel,floor,ceiling):    #定义一个生成trainroute和trainlabel的函数，可以设定subject的个数
    fopen = open(route,"r")    #以只读方式打开route.txt，用来读取全部item的路径
    route_list = fopen.readlines()    #读取所有行存入route_list
    fopen.close()    #关闭route.txt文件
    f_route = open(trainroute,"w")    #以write方式打开trainroute.txt文件
    f_label = open(trainlabel,"w")    #以write方式打开trainlabel.txt文件
    for subject_item in route_list:     #对于route_list中的每个元素
        if match_item(subject_item,floor=floor,ceiling=ceiling) == True:    #如果符合item筛选原则，就执行以下操作
            class_label = recog_class(subject_item)-1   
            f_route.write('%s' % (subject_item))    #将符合条件的item写入文件
            f_label.write('%s\n' % (class_label))   #将符合条件的item的label也写入文件
            #print(subject_item)   #打印item
            #print(class_label)    #打印label
    f_route.close()    #关闭route文件
    f_label.close()    #关闭label文件

def test_route_label(route,testroute,testlabel,floor,ceiling):    #定义一个生成testroute和testlabel的函数，可以设定subject的个数
    fopen = open(route,"r")    #以只读方式打开route.txt，用来读取全部item的路径
    route_list = fopen.readlines()    #读取所有行存入route_list
    fopen.close()    #关闭route.txt文件
    f_route = open(testroute,"w")    #以write方式打开testroute.txt文件
    f_label = open(testlabel,"w")    #以write方式打开testlabel.txt文件
    for subject_item in route_list:     #对于route_list中的每个元素
        if match_item(subject_item,floor=floor,ceiling=ceiling) == True:    #如果符合item筛选原则，就执行以下操作
            class_label = recog_class(subject_item)-1   
            f_route.write('%s' % (subject_item))    #将符合条件的item写入文件
            f_label.write('%s\n' % (class_label))   #将符合条件的item的label也写入文件
            #print(subject_item)    #打印item
            #print(class_label)    #打印label
    f_route.close()    #关闭route文件
    f_label.close()    #关闭label文件

print("Creating all items routepath...")
get_routefile('/samba/HDD/output_20170117_error/c3d/','route.txt',40)
print("Creating 'trainroute.txt' and 'trainlabel.txt'...")
train_route_label("route.txt","trainroute.txt","trainlabel.txt",1,5)
print("Creating 'testroute.txt' and 'testlabel.txt'...")
test_route_label("route.txt","testroute.txt","testlabel.txt",6,40)
print("Done!")
