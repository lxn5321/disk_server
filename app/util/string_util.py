# _*_ coding:utf-8 _*_
import json
import os
import time
import hashlib

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def suffix_handler(headers, suffix):
    if suffix == '.jpg':
        headers['Content-Type'] = 'image/jpeg'
    elif suffix == '.png':
        headers['Content-Type'] = 'image/png'
    elif suffix == '.pdf':
        headers['Content-Type'] = 'application/pdf'
    elif suffix == '.doc' or suffix == '.docx':
        headers['Content-Type'] = 'application/msword'
    else:
        headers['Content-Type'] = 'text/html'

def generate_category_id(file_name):
    id = '5'
    pos = file_name.rfind('.')
    if pos is not -1:
        sf = file_name[pos + 1:]
        if sf == 'png' or sf == 'jpg':
            id = '1'
        elif sf == 'txt' or sf == 'doc' or sf == 'docx' or sf == 'xls' or sf == 'xlsx':
            id = '2'
        elif sf == 'mp4':
            id = '3'
        elif sf == 'mp3':
            id = '4'
        else:
            id = '5'

    return id

def generate_suffix_img(file_name):
    suffix = 'unknow'
    pos = file_name.rfind('.')
    if pos is not -1:
        sf = file_name[pos+1:]
        if sf == 'png' or sf == 'jpg':
            suffix = 'img'
        elif sf == 'mp4':
            suffix = 'video'
        elif sf == 'mp3':
            suffix = 'music'
        elif sf == 'txt' or sf == 'doc' or sf == 'docx':
            suffix = 'txt'
        elif sf == 'xls' or sf == 'xlsx':
            suffix = 'excel'
        elif sf == 'pdf':
            suffix = 'pdf'
        elif sf == 'zip' or sf == 'rar':
            suffix = 'zip'
        else:
            suffix = 'unknow'

    return '/images/' + suffix+'.png'

def generate_file_size_show(file_size):
    suffix = 'B'
    number = '0'
    if file_size < 1024:
        number = str(int(file_size))
        suffix = 'B'
    elif file_size < 1024*1024:
        number = str(int(file_size/1024))
        suffix = 'KB'
    elif file_size < 1024*1024*1024:
        number =  str(int(file_size/1024/1024))
        suffix = 'MB'
    else:
        number =  str(int(file_size/1024/1024/1024))
        suffix = 'GB'
    return number + ' ' + suffix

def generate_folder_list(cur_folder, folder_url, only_folder=False):

    data = {
        "file_count": 0
    }
    file_list = []
    file_names = os.listdir(cur_folder)
    for file_name in file_names:
        data_son = {}
        if os.path.isdir(cur_folder+'/'+file_name):
            data['file_count'] += 1
            data_son['file_name'] = file_name
            data_son['is_folder'] = '1'
            data_son['file_icon'] = '/images/folder.png'
            data_son['folder_url'] = folder_url  + file_name + '/'
            file_list.append(data_son)
        elif os.path.isfile(cur_folder+'/'+file_name) and not only_folder: # 如果是only_folder, 只会返回目录
            data['file_count'] += 1
            data_son['file_name'] = file_name
            data_son['is_folder'] = '0'
            data_son['file_size_show'] = generate_file_size_show(os.path.getsize(cur_folder + '/' + file_name))
            data_son['file_size'] = os.path.getsize(cur_folder + '/' + file_name)
            data_son['file_icon'] = generate_suffix_img(file_name)
            file_list.append(data_son)
        else:
            pass
    data['file_list'] = file_list
    return json.dumps(data)

def generate_category_list(ups):
    data = {
        "file_count": 0
    }
    file_list = []
    for up in ups:
        data_son = {}
        data_son['file_name'] = up.file_name
        data_son['file_size_show'] = generate_file_size_show(int(up.file_size))
        data_son['file_size'] = int(up.file_size)
        data_son['file_icon'] = generate_suffix_img(up.file_name)
        data_son['file_path'] = up.file_path
        data_son['is_folder'] = '0'
        file_list.append(data_son)
    data['file_list'] = file_list
    data['file_count'] = len(ups)
    return json.dumps(data)


def get_last_modified_str(file_path):
    modifiedTime = time.localtime(os.stat(file_path).st_mtime)
    mTime = time.strftime('%a, %d %b %Y %H:%M:%S GMT', modifiedTime)
    return mTime

def generate_md5(file_path):
    return hashlib.md5(file_path.encode('utf-8')).hexdigest()

def generate_share_list(shs):
    data = {
        "file_count": 0
    }
    file_list = []
    for sh in shs:
        data_son = {}
        data_son['file_name'] = sh.file_name
        if sh.is_folder:
            data_son['file_icon'] = 'images/folder.png'
        else:
            data_son['file_icon'] = generate_suffix_img(sh.file_name)
        data_son['share_key'] = sh.share_key
        data_son['is_folder'] = str(sh.is_folder)
        file_list.append(data_son)
    data['file_list'] = file_list
    data['file_count'] = len(shs)
    return json.dumps(data)