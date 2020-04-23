# _*_ coding: utf-8 _*_
from app.util import *
from . import home
from app import db
from app.models import User,Upload,Share
from flask import render_template, url_for, redirect, flash, session, request, make_response
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
from shutil import copyfile, copytree
import os
import shutil

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

# 登录
@home.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username'], forbidden=False).first()    # 获取用户信息
        if not user :
            return render_template("home/login.html", tips='''用户不存在''') # 调回登录页
        if not user.check_pwd(data["password"]):     # 调用check_pwd()方法，检测用户名密码是否匹配
            return render_template("home/login.html", tips='''密码错误''')  # 调回登录页

        # 只要这里给了session值，session和cookie的配对过程后面自动就会帮我们完成
        session["username"] = user.username              # 将username写入session, 后面用户判断用户是否登录
        session["user_id"] = user.user_id
        # if 'next_page' in request.form: # 可以主动设置登录后的跳转页面
        #     return redirect(request.form['next_page'])
        if 'share_key' in data and data['share_key'] != '':
            return redirect('/share/'+data['share_key'])

        return  redirect(url_for('home.index'))

    if 'share_key' in request.args:
        share_key = request.args['share_key']
    else:
        share_key = ''
    return render_template("home/login.html", tips="", share_key=share_key)

# 注册
@home.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        user_ = User.query.filter_by(username=data['username']).first()  # 获取用户信息
        username_ = request.form["username"]
        password_ = request.form["password"]
        nickname_ = request.form["nickname"]
        if is_contain_chinese(username_) or is_contain_chinese(password_):
            return render_template("home/register.html", tips="注册失败，包含非法字符")
        if not user_:
            user = User(
                username = username_,            # 用户名
                password = password_,                  # todo 对密码加密
                nickname = nickname_,            # 昵称
                forbidden = 0
            )
            db.session.add(user) # 添加数据
            db.session.commit()  # 提交数据
            root = os.getcwd()

            # 创建用户目录
            user_folder = root + '/user_folder/' + username_
            if os.path.exists(user_folder):
                shutil.rmtree(user_folder)
            os.mkdir(user_folder)

            # 链接初始文件
            # src = root + '/file_data/1' # 要链接的文件
            # dst = user_folder + '/readme.txt'  # 创建好的软链接
            # os.symlink(src, dst)

            return render_template("home/register.html", tips="注册成功")
        return render_template("home/register.html", tips="用户已存在")
    return render_template("home/register.html", tips="")

@home.route("/favicon.ico")
def favicon():
    root = os.getcwd()
    f = open(root + '/app/templates/static/images/favicon.jpg', mode='rb')
    content = f.read()
    # todo 检查该用户是否有下载此文件权力
    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(len(content))
    }

    return content , 200, headers

@home.route("/logout/")
@user_login
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

# 获取目录列表
@home.route("/list/", methods=["GET", "POST"])
@user_login
def list_():
    path = ''
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_folder = user_folder + '/' + path
    if 'only_folder' in request.args:
        only_folder = True
    else:
        only_folder = False
    list_json = generate_folder_list(cur_folder, path, only_folder)
    return list_json

# 目录列表
@home.route("/list/<path:path>", methods=["GET", "POST"])
@user_login
def list(path):
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_folder = user_folder + '/' + path
    if 'only_folder' in request.args:
        only_folder = True
    else:
        only_folder = False
    list_json = generate_folder_list(cur_folder, path, only_folder)
    return list_json

# 上传文件
@home.route("/upload/", methods=["POST", "GET"])
@user_login
def upload_():
    if request.method == "GET":
        return 'please use get method'

    path = ''
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    file = request.files['file']
    if os.path.exists(cur_file_path + file.filename):
        return '2'
    file.save(cur_file_path + file.filename)
    up = Upload(
        user_id=session['user_id'],
        category_id=generate_category_id(file.filename),
        file_path=path + file.filename,
        file_size=str(os.path.getsize(cur_file_path + file.filename)),
        file_name=file.filename
    )
    db.session.add(up)  # 添加数据
    db.session.commit()  # 提交数据


    return '0'

@home.route("/upload/<path:path>", methods=["POST", "GET"])
@user_login
def upload(path):
    if request.method == "GET":
        return 'please use get method'


    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    file = request.files['file']
    if os.path.exists(cur_file_path + file.filename):
        return '2'
    file.save(cur_file_path + file.filename)
    up = Upload(
        user_id=session['user_id'],
        category_id=generate_category_id(file.filename),
        file_path=path + file.filename,
        file_size=str(os.path.getsize(cur_file_path + file.filename)),
        file_name=file.filename
    )
    db.session.add(up)  # 添加数据
    db.session.commit()  # 提交数据

    return  '0'

# 删除文件
@home.route("/delete/<path:path>", methods=["GET", "POST"])
@user_login
def delete(path):
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    sub_path = user_folder + '/'
    cur_file_path = user_folder + '/' + path
    # 递归删除文件，包括递归删除数据库保存的数据
    if os.path.isdir(cur_file_path):
        for root_, dirs, files in os.walk(cur_file_path):
            for file in files:
                file_path = os.path.join(root_, file)
                file_path = file_path.replace(sub_path, '')
                file_path = file_path.replace('\\', '/')
                Upload.query.filter_by(user_id=session['user_id'], file_path=file_path).delete()
                # 如果文件夹内部还有文件被分享，也会一起删除分享记录
                sh = Share.query.filter_by(user_id=session['user_id'], file_path=username + "/" + file_path)
                if sh:
                    sh.delete()
                db.session.commit()
            for dir in dirs:
                file_path = os.path.join(root_, dir)
                file_path = file_path.replace(sub_path, '')
                file_path = file_path.replace('\\', '/')
                sh = Share.query.filter_by(user_id=session['user_id'], file_path=username + "/" + file_path)
                if sh:
                    sh.delete()
        shutil.rmtree(cur_file_path)
    if os.path.isfile(cur_file_path):
        Upload.query.filter_by(user_id=session['user_id'], file_path=path).delete()
        db.session.commit()
        os.remove(cur_file_path)

    sh = Share.query.filter_by(user_id=session['user_id'], file_path=username + "/" + path)
    if sh:
        sh.delete()
    db.session.commit()
    return ''

# 服务于网页版
# 下载文件
@home.route("/download/<path:path>", methods=["GET", "POST"])
@user_login
def download(path):
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    f = open(cur_file_path, mode='rb')
    content = f.read()
    # todo 检查该用户是否有下载此文件权力
    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(len(content))
    }
    return content , 200, headers


@home.route("/preview/<path:path>", methods=["GET", "POST"])
@user_login
def preview(path):
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    f = open(cur_file_path, mode='rb')
    content = f.read()
    # todo 检查该用户是否有下载此文件权力
    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(len(content))
    }

    pos = cur_file_path.rfind('.')
    if pos is not -1:
        suffix = cur_file_path[pos:]
        suffix_handler(headers, suffix)

    return content , 200, headers

# 文件的图标
@home.route("/images/<path:path>", methods=["GET"])
def images(path):
    root = os.getcwd()
    cur_file_path = root + '/app/templates/static/images/' + path
    f = open(cur_file_path, mode='rb')
    content = f.read()
    headers = {
        'Content-Type': 'img',
        'Content-Length': str(len(content))
    }
    return content , 200, headers

@home.route("/create_folder/", methods=["GET"])
@user_login
def create_folder_():
    path = ''
    folder_name = request.args['folder_name']
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    if os.path.exists(cur_file_path + folder_name):
        return '1'
    os.mkdir(cur_file_path + folder_name)

    return '0'

@home.route("/create_folder/<path:path>", methods=["GET"])
@user_login
def create_folder(path):
    folder_name = request.args['folder_name']
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    if os.path.exists(cur_file_path + folder_name):
        return '1'
    os.mkdir(cur_file_path + folder_name)
    return '0'

# 创建文件
@home.route("/create_file/", methods=["GET"])
@user_login
def create_file_():
    path = ''
    file_name = request.args['file_name']
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    if os.path.exists(cur_file_path + file_name):
        return '1'
    f = open(cur_file_path + file_name, 'w')
    f.close()
    up = Upload(
        user_id=session['user_id'],
        category_id=generate_category_id(file_name),
        file_path=path + file_name,
        file_size=str(0),
        file_name=file_name
    )
    db.session.add(up)
    db.session.commit()
    return '0'

# 创建文件
@home.route("/create_file/<path:path>", methods=["GET"])
@user_login
def create_file(path):
    file_name = request.args['file_name']
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path
    if os.path.exists(cur_file_path + file_name):
        return '1'
    f = open(cur_file_path + file_name, 'w')
    f.close()
    up = Upload(
        user_id=session['user_id'],
        category_id=generate_category_id(file_name),
        file_path=path + file_name,
        file_size=str(0),
        file_name=file_name
    )
    db.session.add(up)
    db.session.commit()
    return '0'

@home.route("/category/<string:id>", methods=["GET"])
@user_login
def category(id):
    user_id =  session['user_id']
    res = {
        "file_list": [],
        "file_count": 0
    }
    ups = Upload.query.filter_by(user_id=user_id, category_id=id).all()
    list_json = generate_category_list(ups)
    return list_json

# 创建分享
@home.route("/create_share/<path:path>", methods=["GET"])
@user_login
def create_share(path):
    file_name = request.args['file_name']
    username = session['username']
    user_id = session['user_id']
    root = os.getcwd()
    file_size = ''

    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path

    sh_ = Share.query.filter_by(user_id=user_id, file_path=path).first()
    if sh_:
        return sh_.share_key

    share_key = generate_md5(username+path)

    if not os.path.exists(cur_file_path):
        return '1'

    is_folder = False
    if os.path.isdir(cur_file_path):
        is_folder = True
    else:
        file_size = os.path.getsize(cur_file_path)

    s = Share(
        user_id=user_id,
        file_path=path,
        file_name=file_name,
        is_folder=is_folder,
        share_key=share_key,
        file_size=file_size
    )

    db.session.add(s)
    db.session.commit()

    return share_key

@home.route("/cancel_share/<string:share_key>", methods=["GET"])
@user_login
def cancel_share(share_key):
    user_id = session['user_id']
    sh = Share.query.filter_by(user_id=user_id, share_key=share_key)
    if not sh:
        return '1'
    sh.delete()
    db.session.commit()
    return '0'

@home.route("/share_list/", methods=["GET"])
@user_login
def share_list():
    user_id =  session['user_id']
    shs = Share.query.filter_by(user_id=user_id).all()
    list_json = generate_share_list(shs)
    return list_json

# get获取分享链接的页面
# post 分享文件到自己的目录下（必须登录后才可以）
@home.route("/share/<string:share_key>", methods=["GET", "POST"])
def share(share_key):
    if (request.method == "GET"):
        sh = Share.query.filter_by(share_key=share_key).first()
        if not sh:
            return '没有对应的资源, 该分享链接可能被删除'

        user =  User.query.filter_by(user_id=sh.user_id).first()

        file_icon = generate_suffix_img(sh.file_name)
        if sh.is_folder:
            file_icon = '/images/folder.png'
            btn_download_display = 'none'
            file_size_show = '-'
        else:
            btn_download_display = 'block'
            file_size_show = generate_file_size_show(int(sh.file_size))


        if "username" in session:
            cur_username = session['username']
        else:
            cur_username = '未登录'

        # 保存到我的网盘按钮是否显示
        if ('user_id' not in session) or str(session['user_id']) != sh.user_id:
            btn_add_display = 'block'
        else:
            btn_add_display = 'none'


        return render_template("home/share.html", file_icon=file_icon, file_name=sh.file_name, file_size=sh.file_size, file_size_show=file_size_show,
                               is_folder=sh.is_folder, share_key=share_key, btn_add_display=btn_add_display, username=cur_username, btn_download_display=btn_download_display, share_username=user.username)
    else:
        return 'not support post'

# 已分享文件下载
@home.route("/share_download/<string:file_name>", methods=["GET"])
def share_download(file_name):
    share_key = request.args['share_key']
    if (request.method == "GET"):

        sh = Share.query.filter_by(share_key=share_key).first()
        if not sh:
            return '没有对应的资源, 该分享链接可能被删除'

        user = User.query.filter_by(user_id=sh.user_id).first()

        root = os.getcwd()
        cur_file_path = root + '/user_folder/' + user.username +'/'+ sh.file_path;
        f = open(cur_file_path, mode='rb')
        content = f.read()
        # todo 检查该用户是否有下载此文件权力
        headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(len(content))
        }
        return content, 200, headers
    else:
        return 'not support post'

# 保存文件到自己的网盘
@home.route("/save_in_mydisk/", methods=["GET"])
@user_login
def save_in_mydisk_():
    path = ''
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path # 用户的某一个目录

    share_key = request.args['share_key']
    sh = Share.query.filter_by(share_key=share_key).first()
    if not sh:
        return '1' # 保存失败

    user = User.query.filter_by(user_id=sh.user_id).first()

    share_file_path =  root + '/user_folder/' + user.username + '/' + sh.file_path


    pre = ''
    count = 1
    # 如果已经存在了这个名字就需要添加字符防止重名
    if os.path.exists(cur_file_path + sh.file_name):
        pre = pre + '(' + str(count) + ')'
        count = count + 1



    if not sh.is_folder:
        copyfile(share_file_path, cur_file_path + pre+ sh.file_name)
        # up = Upload(
        #     user_id=session['user_id'],
        #     category_id=generate_category_id(sh.file_name),
        #     file_path=path + file.filename,
        #     file_size=str(os.path.getsize(cur_file_path + file.filename)),
        #     file_name=file.filename
        # )
        #todo 分享的文件不会归类
    else:
        copytree(share_file_path, cur_file_path + pre + sh.file_name)

    # 找到key对应的文件路径，然后复制到自己的目录中
    return '0'

# 保存文件到自己的网盘 同时要更新Upload表
@home.route("/save_in_mydisk/<path:path>", methods=["GET"])
@user_login
def save_in_mydisk(path):
    root = os.getcwd()
    username = session['username']
    user_folder = root + '/user_folder/' + username
    cur_file_path = user_folder + '/' + path # 用户的某一个目录

    if cur_file_path[:-1] != '/':
        cur_file_path = cur_file_path + '/'

    share_key = request.args['share_key']
    sh = Share.query.filter_by(share_key=share_key).first()
    if not sh:
        return '1' # 保存失败

    user = User.query.filter_by(user_id=sh.user_id).first()

    share_file_path =  root + '/user_folder/' + user.username + '/' + sh.file_path


    pre = ''
    count = 1
    # 如果已经存在了这个名字就需要添加字符防止重名
    if os.path.exists(cur_file_path + sh.file_name):
        pre = pre + str(count)
        count = count + 1

    if not sh.is_folder:
        copyfile(share_file_path, cur_file_path + pre+ sh.file_name)
        # up = Upload(
        #     user_id=session['user_id'],
        #     category_id=generate_category_id(sh.file_name),
        #     file_path=path + file.filename,
        #     file_size=str(os.path.getsize(cur_file_path + file.filename)),
        #     file_name=file.filename
        # )
        #todo 分享的文件不会归类
    else:
        copytree(share_file_path, cur_file_path + pre + sh.file_name)
    # 找到key对应的文件路径，然后复制到自己的目录中
    return '0'