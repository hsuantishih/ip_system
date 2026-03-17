from app import db
from datetime import datetime

# 多對多資料表
class HostUser(db.Model):
    # 資料表名稱
    __tablename__ = 'hosts_users'

    # 定義欄位內容
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    user_userid = db.Column(db.String(20), db.ForeignKey('users.userid'))

# 建立繼承 db.Model 的 Host 類別
class Host(db.Model):
    # 資料表名稱
    __tablename__ = 'hosts'

    # 定義欄位內容
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host_type = db.Column(db.String(20))
    host_class_c = db.Column(db.String(20))
    host_min = db.Column(db.String(20))
    host_max = db.Column(db.String(20))
    host_len = db.Column(db.Integer)
    gateway = db.Column(db.String(20))
    subnet = db.Column(db.Integer)
    netmask = db.Column(db.String(20))
    deleted = db.Column(db.Boolean, default=False)
    delete_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    create_at = db.Column(db.DateTime, default=datetime.now())
    host_deptname = db.Column(db.String(200), default="")
    comment = db.Column(db.String(2000), default="")

    # 建立資料表關係
    host_allocation = db.relationship('Allocation', backref='hosts', cascade='all, delete, delete-orphan')

    # 多對多關係
    users = db.relationship('User', secondary='hosts_users', back_populates='hosts')

    # 一對一關係
    user_application = db.relationship('UserApplyHost', backref='hosts', uselist=False)

    # 設定回傳值
    def __repr__(self):
        return f"<Host id: {self.id}>"
    
# 建立繼承 db.Model 的 Allocation 類別
class Allocation(db.Model):
    # 資料表名稱
    __tablename__ = "host_allocation"

    # 定義欄位內容
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20))
    mac = db.Column(db.String(20), default="")
    owner = db.Column(db.String(20), default="")
    comment = db.Column(db.String(2000), default="")
    device = db.Column(db.String(20))
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id', ondelete='CASCADE'))
    
    # 設定回傳值
    def __repr__(self):
        return f"<Allocation id: {self.id}, Host id: {self.host_id}>"
    
# 事件監聽器: 更新 Host 時間戳
@db.event.listens_for(Host.users, 'append')
@db.event.listens_for(Host.users, 'remove')
def update_assign_timestamp(target, value, initiator):
    # value 是 users; targer 是 host
    # 更新 Host 的時間戳
    target.update_at = datetime.now()

    db.session.commit()