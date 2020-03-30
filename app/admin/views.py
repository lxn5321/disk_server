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


@admin.route("/")
def index():
    return render_template("admin/index.html")

@admin.route("/login/", methods=["GET", "POST"])
def login():
    return render_template("admin/login.html")
