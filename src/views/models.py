from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.now()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 模拟数据库
users = {}
