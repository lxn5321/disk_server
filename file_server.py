# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, render_template,abort
import json
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/get_file_info')
def get_file_info():
    file_name = request.args['file_name']
    current_path = os.getcwd()
    if file_name is None:
        abort(400)
    file_path = current_path + '/www/' +  file_name
    if not os.path.exists(file_path):
        abort(404)
    file_size = os.path.getsize(file_path)
    etag = '1'
    dict = {}
    dict["file_size"] = file_size
    dict["etag"] = etag

    return json.dumps(dict)

@app.route('/download')
def download():
    file_name = request.args['file_name']
    start_index = int(request.args['start_index']) # 文件内容的开始位置
    end_index = int(request.args['end_index'])# 文件内容的结束位置

    if file_name is None or start_index is None or end_index is None:
        abort(400)

    current_path = os.getcwd()
    file_path = current_path + '/www/' +  file_name

    if not os.path.exists(file_path):
        abort(404)
    content = '123'
    file_size = os.path.getsize(file_path)
    f = open(file_path, mode='r')
    f.seek(start_index, 0)

    if end_index >= file_size:
        content = f.read(file_size-start_index)
    else:
        content = f.read(end_index - start_index + 1)

    return content


app.run(host='0.0.0.0', port=8080, debug=True)

