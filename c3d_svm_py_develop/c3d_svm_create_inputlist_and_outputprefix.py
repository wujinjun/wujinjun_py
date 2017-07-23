#此py脚本用于c3d_svm，可以用这个脚本可以得到inputlist.txt, outputprefix.txt
#Usage：“数据集路径”“inputlist文件名”“ outputprefix文件名”，"起始video序号" ,"结束video序号" ，“帧采样间隔”
#Example：create_inputlist_ouputprefix("/home/wjj/HDD/HDD/dataset_pytest/","input_list.txt","output_list_prefix.txt",1,13,8)
#Author：Wu jinjun
import re
def change_to_outputprefix_format(string):    #定义把路径转换为outputprefix格式的函数
    return re.split(r".jpg",string)[0].replace("dataset","output")
def change_to_inputlist_format(string,label):    #定义把路径转换为inputlist格式的函数
    pattern_frame_num = re.compile(r"\d+")    #定义提取路径中所有数字的的正则表达式
    str_num = re.findall(pattern_frame_num,string)[-1]    #取所有数字中的最后一项
    int_num = int(str_num)     #将str型的数字（前面带有0的,比如“000128”）转为int型
    str_num_withoutzero = str(int_num)    #将int型的数字转换为str型，此时去掉了000
    pattern_path = re.compile(r"000*")    #找到000*之前的路径
    str_path = re.split(pattern_path,string)[0]    #按照以上的规则将帧的路径切片，取前面的路径
    inputlist_string = str_path + ' '+ str_num_withoutzero + ' ' + str(label)   #组合形成inputlist格式
    return inputlist_string
def match_item(string,floor,ceiling):    #定义一个匹配item的函数,可以规定上限和下限
    regex = re.compile(r"subject_*")    #匹配subject_后的数字
    int_num=int(re.split(regex,string)[-1])    #将匹配到的str型数字转为int型,即将数据切片得到最后的数字
    if int_num <= ceiling and int_num >= floor:  #如果小于期望值
        return True

import os
def create_inputlist_ouputprefix(basepath,inputlist,outputprefix,floor,ceiling,sample_interval):    #basepath是数据集的路径，inputlist文件名 outputprefix文件名，帧采样间隔
    f_outputfile = open(outputprefix,'w')    #打开文件准备写入
    f_inputfile = open(inputlist,'w')
    classlist =  os.listdir(basepath)    #将basepath下的文件遍历并存入classlist
    label = 0  
    classlist.sort()    #按照类别的首字母排序
    #print classlist
    for classvar in classlist:    #for数据集下的每个类    
        videodir = os.path.join('%s%s' % (basepath,classvar))
        if os.path.isdir(videodir) == True:    #判断该条目是否是文件夹
            videolist = os.listdir(videodir)    #将video条目存入videolist
            #print videodir
            videolist.sort()
            for videovar in  videolist:    #for每个类下的每个video
                clipdir = os.path.join('%s/%s' % (videodir,videovar))
                #print videolist
                if os.path.isdir(clipdir) == True:    #判断该条目是否是文件夹
                    if match_item(clipdir,floor=floor,ceiling=ceiling) == True:
                        #print clipdir
                        framelist = os.listdir(clipdir)
                        framelist.sort()
                        framelist = framelist[::sample_interval]
                        framelist = framelist[:-1]           
                        for framevar in  framelist:
                            framedir = os.path.join('%s/%s/%s' % (videodir,videovar,framevar))
                            #print framedir,label    #打印clip路径以及对应label
                            frameitem_outputfile = change_to_outputprefix_format('%sc3d/%s_%s/%s' % (basepath,classvar,videovar,framevar))
                            frameitem_inputfile = change_to_inputlist_format(framedir,label)
                            f_outputfile.write('%s\n' % (frameitem_outputfile))    #将条目写入文件
                            f_inputfile.write('%s\n' % (frameitem_inputfile))    #将条目写入文件                        
                            #print frameitem_inputfile
                            #print frameitem_outputfile
        label=label+1
    f_outputfile.close()
    f_inputfile.close()
print("Processing...")
#Usage：“数据集路径”“inputlist文件名”“ outputprefix文件名”，"起始video序号" ,"结束video序号" ，“帧采样间隔”
#Example：create_inputlist_ouputprefix("/home/wjj/HDD/HDD/dataset_pytest/","input_list.txt","output_list_prefix.txt",1,13,8)
create_inputlist_ouputprefix("/samba/HDD/dataset_20170117_error/","input_list_ori.txt","output_list_prefix_ori.txt",1,45,8)
print("Done!")
