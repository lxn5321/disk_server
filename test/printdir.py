import os
import re
#遍历文件夹
def iter_files(rootDir):
    #遍历根目录
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            file_path = os.path.join(root,file)
            file_path = file_path.replace(rootDir, '')
            print(file_path)

path = ''
username = '1'
root = r"D:\apythoncode\disk_server"
user_folder = root + '/user_folder/' + username
cur_file_path = user_folder + '/' + path
iter_files(cur_file_path)