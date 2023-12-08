from baseSQL import InfoSQL
from hashlib import sha256

class UserDB(InfoSQL):
    def __init__(self):
        super().__init__(database='UserDB.db')
        self.connect()
        self.create_user_table()

    def __del__(self):
        self.disconnect()

    def register_user(self, username, password):
        
        # Check if the username already exists
        check_user_query = f"SELECT id FROM {self.table_name} WHERE username = ?"
        self.cursor.execute(check_user_query, (username,))
        existing_user = self.cursor.fetchone()
        if existing_user:
            # Username already exists, handle this situation (raise an exception, return an error code, etc.)
            raise False

        # Hash the password before storing it
        hashed_password = sha256(password.encode()).hexdigest()

        insert_user_query = f"""
            INSERT INTO {self.table_name} (username, password) VALUES
            (?, ?)
        """
        data = (username, hashed_password)
        self.cursor.execute(insert_user_query, data)
        self.db_connection.commit()
        return True

    def authenticate_user(self, username, password):
        # Hash the provided password for comparison
        hashed_password = sha256(password.encode()).hexdigest()

        select_user_query = f"SELECT * FROM {self.table_name} WHERE username = ? AND password = ?"
        self.cursor.execute(select_user_query, (username, hashed_password))
        result = self.cursor.fetchone()
        return result

    def login(self,username,password):
         # 认证用户
        user_credentials = self.authenticate_user(username, password)
        if user_credentials:
            # 如果用户认证成功，将用户的数据库表名设置为当前实例的表名
            return True
        else:
            return False
        
def test():
    worker = UserDB()
    worker.register_user('GSM','123456')
    print("register successfully!")
    if worker.login('GSM','123456'):
        print("log in successfully!")

 

if __name__ == "__main__":
    test()  