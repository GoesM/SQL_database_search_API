import requests
import random
import string
import json
def random_str():
    length = random.randint(1, 5)
    random_string = ''.join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
    return random_string

# 全局会话对象
session = requests.Session()
#-------------------------------------------------------#
# regist a user, 
# it will creat an empty data-table for each new user's count
def register():
    url = "http://127.0.0.1:5000/register" 
    data = {
        "username": "gsm",
        "password": "123456"
    }
    response = session.post(url, json=data)
    print(response.json())
register()

# user log in by his username and password, 
# it will allow him to access his own data-table
def login():
    url = "http://127.0.0.1:5000/login" 
    data = {
        "username": "gsm",
        "password": "123456"
    }
    response = session.post(url, json=data)
    print(response.json())
login()

# user could add his friends' information
# it could be done only after he login
def addFriend(name,rel,id,bir,home,edu,deb,note):
    url = "http://127.0.0.1:5000/addFriend"
    data = {
        "name": name,               # each key
        "relationship": rel,        # could be empty
        "id_card": '',              # like this
        "birth": 'I foget it',      # or like this
        "hometown": home,
        "education": edu,
        "debt": deb,
        "note": note                # anything
    }
    response = session.post(url, json=data)
    formatted_response = json.dumps(response.json(), indent=2, ensure_ascii=False)
    print(formatted_response)
for i in range(5):
    addFriend(f"name{i}",random_str(),f"SY{i}",random_str(),random_str(),random_str(),random_str(),random_str())
for i in range(5):
    addFriend(f"name{i}",f"key{(i-1)}",f"SY{i}",random_str(),random_str(),random_str(),random_str(),random_str())


# user could search by keywords (in any number)
# it could be done only after he login
# if keyword is empty, show all table
def searchBYKeyword(keywords="key1 key2 key3"):
    url = "http://127.0.0.1:5000/search"
    data = {
        "keywords": keywords # many keywords divided by space
    }
    response = session.post(url, json=data)
    formatted_response = json.dumps(response.json(), indent=2, ensure_ascii=False)
    print(formatted_response)
searchBYKeyword()
searchBYKeyword(keywords="")

# user could change value of any column of any id
# it could be done only after he login
def update():
    url = "http://127.0.0.1:5000/update"
    data = {
        "id": "1",   # the CTR in SQL table
        "column": "name",
        "value": "Alice"
    }
    response = session.post(url, json=data)
    formatted_response = json.dumps(response.json(), indent=2, ensure_ascii=False)
    print(formatted_response)
update()


# user could logout
def logout():
    url = "http://127.0.0.1:5000/logout" 
    response = session.post(url)
    formatted_response = json.dumps(response.json(), indent=2, ensure_ascii=False)
    print(formatted_response)
logout()


