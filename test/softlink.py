import os
import shutil
#
# src = r"D:\apythoncode\disk_server\test\test.py"                     #要链接的文件
# dst = r"D:\apythoncode\disk_server\test\1"  #创建好的软链接
# os.symlink(src, dst)

# src = r"D:\apythoncode\disk_server\test\1"                     #要链接的文件
# dst = r"D:\apythoncode\disk_server\test\2"  #创建好的软链接
# os.symlink(src, dst)
# #
#
# f = open(r"D:\apythoncode\disk_server\User\1.txt", mode='rb')
# print(f.read().decode('utf-8'))
# f.close()
#
# print(os.path.getsize(r"D:\apythoncode\disk_server\User\1.txt"))
#
# os.remove(r"D:\apythoncode\disk_server\User\1.txt")

# 删除目录
# os.rmdir(path)

# 删除文件夹
#
# 1、os.path.exists(path) 判断一个目录是否存在
#
# 2、os.makedirs(path) 多层创建目录
#
# 3、os.mkdir(path) 创建目录
# src = r"D:\apythoncode\disk_server\user_folder\1\readme.txt"
# os.remove(src)
from shutil import copyfile,copytree
#
# copyfile(r'D:\apythoncode\disk_server\user_folder\1\新建文件.txt', r'D:\apythoncode\disk_server\user_folder\2\新建文件.txt')
# # 找到key对应的文件路径，然后复制到自己的目录中

shutil.copytree(r'D:\apythoncode\disk_server\user_folder\1', r'D:\apythoncode\disk_server\user_folder\2\1')
