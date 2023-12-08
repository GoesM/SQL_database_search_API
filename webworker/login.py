import requests
import random
import string
import json


from config import global_ip, port_num
# 全局会话对象
session = requests.Session()
# user log in by his username and password, 
# it will allow him to access his own data-table
def login(name,mm):
    url = f"http://{global_ip}:{port_num}/login" 
    data = {
        "username": name,
        "password": mm
    }
    response = session.post(url, json=data)
    print(response.json())

if __name__ == '__main__': # launch A
    name = input("your account name:: ")
    mm = input("your key:: ")
    login(name,mm)
