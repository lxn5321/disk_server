# _*_ coding: utf-8 _*_
from . import home
from app import db
from app.models import User
from flask import render_template, url_for, redirect, flash, session, request, make_response
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
import os

def user_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)

    return decorated_function

@home.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()    # 获取用户信息
        if not user :
            return render_template("home/login.html", tips="用户不存在") # 调回登录页
        if not user.check_pwd(data["password"]):     # 调用check_pwd()方法，检测用户名密码是否匹配
            return render_template("home/login.html", tips="密码错误")  # 调回登录页

        # 只要这里给了session值，session和cookie的配对过程后面自动就会帮我们完成
        session["username"] = user.username              # 将username写入session, 后面用户判断用户是否登录

        return  redirect(url_for('home.index'))
    return render_template("home/login.html", tips="")


@home.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        user_ = User.query.filter_by(username=data['username']).first()  # 获取用户信息

        if not user_:
            user = User(
                username = request.form["username"],            # 用户名
                pwd = request.form["password"],                  # todo 对密码加密
                nickname = request.form["nickname"],            # 昵称
                filelist = '''{
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
            db.session.add(user) # 添加数据
            db.session.commit()  # 提交数据
            return render_template("home/register.html", tips="注册成功")
        return render_template("home/register.html", tips="用户已存在")
    return render_template("home/register.html", tips="")

@home.route("/favicon.ico")
def favicon():
    return ''

@home.route("/logout/")
def logout():
    """
    退出登录
    """
    # 重定向到home模块下的登录。
    session.pop("username", None)
    return redirect(url_for('home.login'))

@home.route("/")
@user_login
def index():
    return render_template("home/main.html", nickname=session['username']) # 渲染模板


@home.route("/filelist/", methods=["GET", "POST"])
@user_login
def list():
    username = session['username']
    user_ = User.query.filter_by(username=username).first()  # 获取用户信息
    return user_.filelist

@home.route("/upload/", methods=["GET", "POST"])
@user_login
def upload():
    return 'upload'

@home.route("/delete/", methods=["GET", "POST"])
@user_login
def delete():
    return 'delete'

# 服务于网页版
@home.route("/download/<path:path>", methods=["GET", "POST"])
@user_login
def download(path):
    data = request.args
    file_path = os.getcwd() + '\\www\\' + data['fileid']
    content = ''
    f = open(file_path, mode='rb')
    content = f.read()
    # todo 检查该用户是否有下载此文件权力
    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(len(content))
    }
    return content , 200, headers