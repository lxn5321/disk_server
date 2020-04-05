import os

def open_file(file_path):
    return open(file_path, mode='ab')


f = open_file("C:/Users/ljh/Desktop/disk_server_file/t.txt")
f.write('123'.encode("utf-8"))