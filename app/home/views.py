# _*_ coding: utf-8 _*_
from . import home
from app import db
from app.models import User
from flask import render_template, url_for, redirect, flash, session, request, make_response
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps

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
        username = request.form['username']
        if username != '1' and username != '2':
            return 'login fail'
        password = request.form['password']
        # 只要这里给了session值，session和cookie的配对过程后面自动就会帮我们完成
        session['username'] = username
        return  redirect(url_for('home.index'))
    return render_template("home/login.html")


@home.route("/register/", methods=["GET", "POST"])
def register():
    return render_template("home/register.html")


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


@home.route("/list/", methods=["GET", "POST"])
@user_login
def list():
    session['username']
    return 'list'

@home.route("/upload/", methods=["GET", "POST"])
@user_login
def upload():
    session['username']
    return 'upload'

@home.route("/delete/", methods=["GET", "POST"])
@user_login
def delete():
    session['username']
    return 'delete'

@home.route("/download/", methods=["GET", "POST"])
@user_login
def download():
    session['username']
    return 'download'