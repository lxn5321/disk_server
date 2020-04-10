# _*_ coding:utf-8 _*_
import os
import uuid
from datetime import datetime
from app import db
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, g, abort,make_response,current_app
from app.models import Admin
from werkzeug.utils import secure_filename
from sqlalchemy import or_ , and_
from functools import wraps


# _*_ coding: utf-8 _*_
from . import admin
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

@admin.route("/login/", methods=["GET", "POST"])
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


