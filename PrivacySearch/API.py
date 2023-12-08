from flask import Flask, request, jsonify, session, redirect, url_for
from UserDB import UserDB
from baseSQL import InfoSQL
app = Flask(__name__)

import os
# 生成随机密钥
app.secret_key = os.urandom(24)


def formatMaker(status:int,data:list,statusText:str):
    result = {
        "status": status,
        "data": data,
        "statusText": statusText
    }
    return result

def errorBack(text:str):
    return formatMaker(
        status=401,
        data=[],
        statusText=text
    )
def dataBack(data:list,log:str):
    return formatMaker(
        status=200,
        data = data,
        statusText=log
    )
def logBack(log:str):
    return formatMaker(
        status=200,
        data = [],
        statusText=log
    )


# 登录页面
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    worker = UserDB()
    # 验证用户名和密码
    if worker.login(username=username,password=password):
        # 登录成功，将用户信息存储在会话中
        session['username'] = username
        del worker
        return jsonify(logBack('Login successful'))
    else:
        del worker
        return jsonify(errorBack('Invalid username or password'))

#---------------------register-------------------------------------------------_#
def register_user(username,password):
    worker = UserDB()
    flag = worker.register_user(username=username,password=password)
    del worker
    return flag
def initTable(username):
    worker = InfoSQL(table_name=username)
    worker.connect()
    worker.create_table() # empty table
    worker.disconnect()
    return
# register页面
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if register_user(username=username,password=password):
        initTable(username=username) # create an empty table for each user
        return jsonify(logBack('register successfully'))
    else:
        return jsonify(errorBack("Username already exists. Please change."))



#-------------------------log out-----------------------------------------#        
# 注销操作
@app.route('/logout', methods=['POST'])
def logout():
    # 清除会话中的用户信息
    session.pop('username', None)
    return jsonify(logBack('Logout successful'))

#---------------------------add data--------------------------------------#
# 保护的资源，只有登录用户才能访问
@app.route('/addFriend', methods=['POST'])
def addFriend():
    # 检查用户是否登录
    if session.get('username')==None:
        return jsonify(errorBack("Unauthorized."))
    else:
        username=session['username']
    # data catch
    data = request.get_json()
    # read
    name = data.get('name')
    relationship = data.get('relationship')
    id_card = data.get('id_card') 
    birth = data.get('birth')
    hometown = data.get('hometown')
    education = data.get('education')
    debt = data.get('debt')
    note = data.get('note')
    
    # add
    myTable = InfoSQL(table_name=username)
    myTable.connect()
    result = myTable.insert_friend(
        name=name,
        relationship=relationship,
        id_card=id_card,
        birth=birth,
        hometown=hometown,
        education=education,
        debt=debt,
        note=note
    )
    myTable.disconnect()
    return jsonify(logBack('add data successfully'))


#--------------------------search by keyword-------------------------------#
import re
def reduce_spaces_and_strip(input_string):
    # 使用正则表达式将连续多个空格替换为一个空格
    processed_string = re.sub(r'\s+', ' ', input_string)
    # 使用strip()函数删除头部和尾部空格
    stripped_string = processed_string.strip()
    return stripped_string
# 保护的资源，只有登录用户才能访问
@app.route('/search', methods=['POST'])
def search():
    # 检查用户是否登录
    if 'username' not in session:
        return jsonify(errorBack("Unauthorized."))
    else:
        username=session['username']
    # 'keywords' list
    data = request.get_json()
    keywords = data.get('keywords')
    keywords = reduce_spaces_and_strip(keywords)
    keyword_list = keywords.split()

    myTable = InfoSQL(table_name=username)
    myTable.connect()
    result = myTable.findFriendByKeyword(keyword_list)
    myTable.disconnect()    
    return jsonify(dataBack(
        data=result,
        log="search successfully"
    ))

       

#------------------------update value--------------------------------------#
# 保护的资源，只有登录用户才能访问
@app.route('/update', methods=['POST'])
def update():
    # 检查用户是否登录
    if 'username' not in session:
        return jsonify(errorBack("Unauthorized."))
    else:
        username=session['username']

    data = request.get_json()
    CTR = data.get('id')
    column = data.get('column')
    value = data.get('value')

    myTable = InfoSQL(table_name=username)
    myTable.connect()
    myTable.update_value(CTR=CTR,column=column,new_value=value)
    myTable.disconnect()
    return jsonify(logBack("update successfully"))
  

if __name__ == '__main__': # launch API
    app.run(host='127.0.0.1', port=5000, debug=True)

