from app import db
from datetime import datetime

# 建立繼承 db.Model 的 User 類別
class User(db.Model):
    # 資料表名稱
    __tablename__ = 'users'

    # 定義欄位內容
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), default="")
    deptname = db.Column(db.String(20), default="")
    ident = db.Column(db.String(20), default="")
    officephone = db.Column(db.String(20), default="")
    email = db.Column(db.String(20), default="")
    allocation = db.Column(db.String(20), default="")
    admin = db.Column(db.Boolean, default=False)

    # 建立資料表關係
    hosts = db.relationship('Host', secondary='hosts_users', back_populates='users')

    # 一對多關係
    host_application = db.relationship('UserApplyHost', backref='users')

    # 設定回傳值
    def __repr__(self):
        return f"<User id: {self.id}, userid: {self.userid}>"
    
class UserApplyHost(db.Model):
    __tablename__ = 'user_apply_hosts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_userid = db.Column(db.String(20), db.ForeignKey('users.userid'))
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    applied = db.Column(db.Boolean, default=False)
    applied_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # 設定回傳值
    def __repr__(self):
        return f"<UserApplyHosts id: {self.id}>"