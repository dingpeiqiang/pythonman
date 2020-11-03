#1.先找到所有指定日期最近更新的文件

#2.判断目标目录是否存在，如果存在建立目录

#3.使用copyfile复制到指定目录（和原始目录结构保持一致）

import os
import sys
import datetime, time
import shutil
import logger
dateFormat = '%Y-%m-%d %H:%M:%S'
all_files = [] #源目录下的所有的文件
log = logger.Logger()

#=============获取指定目录下包含的所有文件列表==========================
def get_all_file(rawdir):
    global  all_files
    all_file_list = os.listdir(rawdir)
    for f in all_file_list:
        if f =='.git' or f == 'target' or f.endswith(".iml") or f == '.idea':
            continue
        filepath = os.path.join(rawdir, f)
        if os.path.isdir(filepath):
            get_all_file(filepath)
        if not os.path.isdir(filepath):
            all_files.append(filepath)

#============获取指定目录下的文件更新时间  大于 开始时间  的文件================
def get_new_file(path_src_web,time_modify):
    #初始化变量
    all_new_files = []  # 更新时间到当前时间
    global all_files
    all_files = []

    get_all_file(path_src_web)
    for f in all_files:
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime(dateFormat)
        if file_time >= time_modify:
            all_new_files.append(f)
            #print cmd_xcopy
    return all_new_files


#===========将满足条件的文件 复制到 目标文件目录的同级目录下==========
def copy_web_files(path_src_web,path_dst_web,time_modify):
    new_files = get_new_file(path_src_web,time_modify)
    copy_source_to_target(path_src_web,path_dst_web,new_files)

def copy_source_to_target(path_src_web,path_dst_web,new_files):
    for f in new_files:
        target_file = f.replace(path_src_web, path_dst_web)  # 获取目标文件全路径文件名
        # print target_file
        head, tail = os.path.split(target_file)  # 拆分文件目录和文件名
        # print(head)
        if not os.path.exists(head):  # 目录不存在则创建目录
            os.makedirs(head)
        log.logger.debug(f + '----->>' + target_file)
        shutil.copyfile(f, target_file)  # 复制文件到到目标文件
    file_size = len(new_files)
    if (file_size > 0):
        print("copy_web_files success! count: %s  target:%s." % (file_size, path_dst_web))
    else:
        print("copy_web_files error , no files for copy...")


if __name__ == '__main__':
    copy_web_files()
