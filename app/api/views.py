# _*_ coding: utf-8 _*_
from . import api
from app import db
from app.models import User, FileData
from flask import render_template, url_for, redirect, flash, session, request, make_response
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
import os
import json
import base64

@api.route("/favicon.ico")
def favicon():
    return ''

@api.route("/logout/")
def logout():
    return '123'

@api.route("/login/", methods=['GET','POST'])
def login():
    data = None
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    user_ = User.query.filter_by(username=data['username']).first()  # 获取用户信息
    if not user_:
        return '1'
    if not user_.check_pwd(data["password"]):  # 调用check_pwd()方法，检测用户名密码是否匹配
        return '1'
    return '0'

@api.route("/register/", methods=['GET','POST'])
def register():
    data = None
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    user_ = User.query.filter_by(username=data['username']).first()  # 获取用户信息
    if not user_:
        user = User(
            username=data["username"],  # 用户名
            pwd=data["password"],  # todo 对密码加密
            nickname=data["nickname"],  # 昵称
            filelist='''{
  "files":[
    {"filename": "file1.txt",
     "fileid":   "1",
     "filesize": "54",
     "uploadtime": "unknow"
    },
    {"filename": "file2.txt",
     "fileid":   "2",
     "filesize": "54",
     "uploadtime": "unknow"
    },
    {"filename": "file3.txt",
     "fileid":   "3",
     "filesize": "54",
     "uploadtime": "unknow"
    },
    {"filename": "file4.mp4",
     "fileid":   "4",
     "filesize": "10556575",
     "uploadtime": "unknow"
    },
    {"filename": "file5.jpg",
     "fileid":   "5",
     "filesize": "8014454",
     "uploadtime": "unknow"
    }
    ]
}
                '''
        )
        db.session.add(user)  # 添加数据
        db.session.commit()  # 提交数据
        return '0'
    return '1'


@api.route("/filelist/", methods=["GET", "POST"])
def list():
    data = None
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    username = data['username']
    user_ = User.query.filter_by(username=username).first()  # 获取用户信息
    return user_.filelist


@api.route("/download/", methods=["GET", "POST"])
def download():
    data = None
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    start = int(data['start'])
    size = int(data['size'])
    file_path = os.getcwd() + '\\www\\' + data['fileid']
    file_size = os.path.getsize(file_path)
    content = ''
    f = open(file_path, mode='rb')
    f.seek(start)
    if start + size < (file_size - 1):
        content = f.read(size)
    else:
        content = f.read()
    # todo 检查该用户是否有下载此文件权力
    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(len(content))
    }
    return content , 200, headers


@api.route("/checkout/", methods=["GET", "POST"])
def checkout():
    data = ''
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    filemd5_ = data['filemd5']
    file_ = FileData.query.filter_by(filemd5=filemd5_).first()
    resp = {
        "code" : "0",
        "fileid" : ""
    }
    if not file_:
        resp["code"] = "-1"
    else:
        resp["fileid"] = str(file_.id)

    return json.dumps(resp)

# 先为文件在数据库添加表
@api.route("/create/", methods=["GET", "POST"])
def create():
    data = ''
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    filemd5_ = data["filemd5"]
    filename_ = data["filename"]
    filesize_ = data["filesize"]
    resp = {
        "code" : "0",
        "fileid" : ""
    }
    try:
        file_ = FileData(
            filemd5=filemd5_,
            filename=filename_,
            filesize=filesize_,
            usecount='1'
        )
        db.session.add(file_)
        db.session.commit()
        file_q = FileData.query.filter_by(filemd5=filemd5_).first()
        resp['fileid'] = file_q.id
    except Exception as e:
        resp['code'] = "-1"


    return json.dumps(resp)

def open_file(file_path):
    return open(file_path, mode='ab')

# iVBORw0KGgoAAAANSUhEUgAABQ4AAAMSCAIAAACkgc65AAAgAElEQVR4AWT965omW5aeaYW7R6yVu6qSxMUPXUADR9A0EjoXhFr84Bw5LRpVVWauXLHp+3mHuecSWHiYm805Ng==
@api.route("/uploaddata/", methods=["POST"])
def uploaddata():
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    fileid_ = data["fileid"]
    filemd5_ = data["filemd5"]
    filecontent_ = data["data"]
    decoded_data_ = base64.b64decode(filecontent_)
    file_path = os.getcwd() + '\\www\\' + fileid_
    f = open_file(file_path)
    f.write(decoded_data_)
    resp = {
        "code" : "0"
    }
    return json.dumps(resp)

# 为用户添加一个文件名和云文件id的关系
@api.route("/bindfile/", methods=["GET", "POST"])
def bindfile():
    data = None
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    fileid_ = data['fileid']
    filename_ = data['filename']
    username_ = data['username']

    file_path = os.getcwd() + '\\www\\' + fileid_
    filesize_ = os.path.getsize(file_path)
    user_ = User.query.filter_by(username=username_).first()  # 获取用户信息
    if not user_:
        return '1'
    file_list_obj = json.loads(user_.filelist)
    file_obj = {
        "filename" : str(filename_),
        "filesize" : str(filesize_),
        "fileid": str(fileid_),
        "uploadtime": "unknow"
    }
    try:
        file_list_obj['files'].append(file_obj)
        user_.filelist = json.dumps(file_list_obj)
        db.session.commit()  # 提交数据
    except Exception as e:
        return '1'
    return '0'


# 为用户添加一个文件名和云文件id的关系
@api.route("/unbindfile/", methods=["GET", "POST"])
def unbindfile():
    data = None
    if request.method == 'POST':
        data = request.form
    if request.method == 'GET':
        data = request.args
    fileid_ = data['fileid']
    filename_ = data['filename']
    username_ = data['username']

    file_path = os.getcwd() + '\\www\\' + fileid_
    filesize_ = os.path.getsize(file_path)
    user_ = User.query.filter_by(username=username_).first()  # 获取用户信息
    if not user_:
        return '1'
    file_list_obj = json.loads(user_.filelist)

    list_len = len(file_list_obj['files'])
    for file_item in file_list_obj['files']:
        if file_item["fileid"] == fileid_ and file_item["filename"] == filename_:
            file_list_obj['files'].remove(file_item)

    user_.filelist = json.dumps(file_list_obj)
    db.session.commit()  # 提交数据
    return '0'