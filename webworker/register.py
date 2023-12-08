import requests
import random
import string
import json


from config import global_ip, port_num
# 全局会话对象
session = requests.Session()
#-------------------------------------------------------#
# regist a user, 
# it will creat an empty data-table for each new user's count
def register(name,mm):
    url = f"http://{global_ip}:{port_num}/register" 
    data = {
        "username": name,
        "password": mm
    }
    response = session.post(url, json=data)
    print(response.json())
name = input("your account name:: ")
mm = input("your key:: ")
register(name,mm)
