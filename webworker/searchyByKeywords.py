import requests
import json


from config import global_ip, port_num,default_account,default_key

# 全局会话对象
session = requests.Session()
def login(name,mm):
    url = f"http://{global_ip}:{port_num}/login" 
    data = {
        "username": name,
        "password": mm
    }
    response = session.post(url, json=data)
    print(response.json())
#-------------------------------------------------------#
# user could search by keywords (in any number)
# it could be done only after he login
# if keyword is empty, show all table
def searchBYKeyword(keywords="key1 key2 key3"):
    login(default_account,default_key)
    url = f"http://{global_ip}:{port_num}/search"
    data = {
        "keywords": keywords # many keywords divided by space
    }
    response = session.post(url, json=data)
    formatted_response = json.dumps(response.json(), indent=2, ensure_ascii=False)
    print(formatted_response)


keywords = input("input your keywords: ")
searchBYKeyword(keywords=keywords)

