from . import db
from datetime import datetime

# 会员数据模型
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(100)) # 用户名
    pwd = db.Column(db.String(100))  # 密码
    nickname = db.Column(db.String(100))  # 昵称
    filelist =  db.Column(db.String(1000))  # 文件列表
    # email = db.Column(db.String(100), unique=True)  # 邮箱
    # phone = db.Column(db.String(11), unique=True)  # 手机号
    # info = db.Column(db.Text)  # 个性简介
    # face = db.Column(db.String(255), unique=True)  # 头像

    def __repr__(self):
        return '<User %r>' % self.name

    def check_pwd(self, pwd):
        """
        检测密码是否正确
        :param pwd: 密码
        :return: 返回布尔值
        """
        # from werkzeug.security import check_password_hash
        # return check_password_hash(self.pwd, pwd)
        return self.pwd == pwd

# 文件数据模型
class FileData(db.Model):
    __tablename__ = "filedata"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    usecount = db.Column(db.String(100))  # 文件的引用计数
    filename = db.Column(db.String(100))  # 文件名
    filemd5 = db.Column(db.String(100)) # 文件的md5值
    filesize = db.Column(db.String(100)) # 文件大小

    def __repr__(self):
        return '<FileData %r>' % self.name

# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        """
        检测密码是否正确
        :param pwd: 密码
        :return: 返回布尔值
        """
        # from werkzeug.security import check_password_hash
        # return check_password_hash(self.pwd, pwd)
        return self.pwd == pwd
