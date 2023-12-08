import sqlite3



class InfoSQL:
    database = 'default_database_name.db'
    table_name = 'default_table_name'

    def __init__(self, database='default_database_name.db', table_name='default_table_name'):
        self.database = database
        self.table_name = table_name
        self.db_connection = None
        self.cursor = None

    def connect(self):
        self.db_connection = sqlite3.connect(self.database)
        self.cursor = self.db_connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
        
    def create_user_table(self):
        create_user_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                username VARCHAR(255),
                password VARCHAR(64)
            )
        """
        self.cursor.execute(create_user_table_query)
        self.db_connection.commit()

    def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                relationship VARCHAR(255),
                id_card VARCHAR(18),
                birth TEXT,
                hometown VARCHAR(255),
                education VARCHAR(255),
                debt DECIMAL(10, 2) DEFAULT 0.0,
                note VARCHAR(255)
            )
        """
        self.cursor.execute(create_table_query)
        self.db_connection.commit()

    def insert_friend(self, name="", relationship="", id_card="", birth="", hometown="", education="", debt=0.0, note=""):
        insert_query = f"""
            INSERT INTO {self.table_name} (name, relationship, id_card, birth, hometown, education, debt, note) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = (name, relationship, id_card, birth, hometown, education, debt, note)
        self.cursor.execute(insert_query, data)
        self.db_connection.commit()

    def update_value(self, CTR: str, column: str, new_value):
        update_query = f"UPDATE {self.table_name} SET {column} = ? WHERE id = ?"
        data = (new_value, CTR)
        self.cursor.execute(update_query, data)
        self.db_connection.commit()
    
    def result_as_dict(self,result):
        # 获取列信息
        column_names = [description[0] for description in self.cursor.description]
        # 将查询结果转换为字典形式
        result_as_dict = []
        for record in result:
            record_dict = dict(zip(column_names, record))
            result_as_dict.append(record_dict)
        return result_as_dict

    def select_friend(self, name):
        select_query = f"SELECT * FROM {self.table_name} WHERE name = ?"
        self.cursor.execute(select_query, (name,))
        result = self.cursor.fetchall()
        return self.result_as_dict(result)
    
    def findFriendByKeyword(self, keywords_list:list):
        # 构建查询条件
        conditions = []
        values = []
        for keyword in keywords_list:
            for column in ["name", "relationship", "id_card", "birth", "hometown", "education", "debt", "note"]:  
                # 替换为实际的列名
                conditions.append(f"{column} LIKE ?")
                values.append(f"%{keyword}%")

        if not conditions:
            result = self.showALL()
        else:
            where_clause = " OR ".join(conditions)

            # 构建查询语句
            select_query = f"SELECT * FROM {self.table_name} WHERE {where_clause}"

            # 执行查询
            self.cursor.execute(select_query, tuple(values))
            result = self.cursor.fetchall()

        return self.result_as_dict(result)


    def showALL(self):
        # 构建查询语句
        select_all_query = f"SELECT * FROM {self.table_name}"

        # 执行查询
        self.cursor.execute(select_all_query)
        records = self.cursor.fetchall()
        return records



def test():
    info_sql_instance = InfoSQL(table_name='test')

    info_sql_instance.connect()
    info_sql_instance.create_table()

    info_sql_instance.insert_friend("张三", "朋友", "123456789012345678", "1990-01-01", "北京", "本科", 1000.50, "初始数据1")
    info_sql_instance.insert_friend(name="gsm", birth="2001-01-06", education="PD", note="small ugly")

    result = info_sql_instance.select_friend("张三")
    print("张三的信息：\n", result)
    result = info_sql_instance.select_friend("gsm")
    print("gsm的信息：\n", result)

    info_sql_instance.update_value("张三", "欠债", 2000.0)

    result_after_update = info_sql_instance.select_friend("张三")
    print("张三更新后的信息：", result_after_update)
    result = info_sql_instance.findFriendByKeyword(["gsm","1990"])
    print("serach by keywords：", result)

    # 查询包含关键词 "张三" 或 "北京" 的信息
    #result = info_sql_instance.findFriendByKeyword(["张三","gsm"])
    #print("search result::::\n ",result)

    # 查询包含关键词 "gsm" 或 "小学" 的信息
    #result = info_sql_instance.findFriendByKeyword(["gsm", "小学"])
    #print("search result::::\n ",result)


    result = info_sql_instance.showALL()
    print('all table:\n',result)

    info_sql_instance.disconnect()



if __name__ == "__main__":
    test()
