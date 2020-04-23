# _*_ coding:utf-8 _*_
from . import db
from datetime import datetime

# 会员数据模型
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"useexisting": True}
    user_id = db.Column(db.Integer, primary_key=True)     # 用户编号
    username = db.Column(db.String(100), nullable=False)     # 登录账号
    nickname = db.Column(db.String(100), nullable=False) # 用户名
    password = db.Column(db.String(100), nullable=False)  # 密码
    forbidden = db.Column(db.Boolean, nullable=False)  # 是否禁用

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
        return self.password == pwd

# 文件数据模型
class FileData(db.Model):
    __tablename__ = "filedata"
    __table_args__ = {"useexisting": True}
    src_id = db.Column(db.Integer, primary_key=True)  # 编号
    file_size = db.Column(db.String(100), nullable=False) # 文件大小
    use_count = db.Column(db.String(100), nullable=False)  # 文件的引用计数
    file_md5 = db.Column(db.String(100), nullable=False) # 文件的md5值


    def __repr__(self):
        return '<FileData %r>' % self.name


class Upload(db.Model):
    __tablename__ = "upload"
    __table_args__ = {"useexisting": True}
    upload_id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.String(100), nullable=False)  # 用户id
    category_id = db.Column(db.String(100), nullable=False)  # 文件类型
    file_path = db.Column(db.String(100), nullable=False)  # 文件获取路径
    file_size = db.Column(db.String(100), nullable=False)  # 文件大小
    file_name = db.Column(db.String(100), nullable=False)  # 文件名

    def __repr__(self):
        return '<Upload %r>' % self.name

class Share(db.Model):
    __tablename__ = "share"
    __table_args__ = {"useexisting": True}
    share_id = db.Column(db.Integer, primary_key=True)  # 编号
    share_key = db.Column(db.String(100), nullable=False)  # 分享key
    user_id = db.Column(db.String(100), nullable=False)  # 用户id
    file_path = db.Column(db.String(100), nullable=False)  # 文件获取路径
    file_name = db.Column(db.String(100), nullable=False)  # 文件名
    is_folder = db.Column(db.Boolean, nullable=False)  # 是否是文件夹
    file_size = db.Column(db.String(100), nullable=False)  # 文件大小

    def __repr__(self):
        return '<Share %r>' % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    password = db.Column(db.String(100))  # 管理员密码

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
        return self.password == pwd
