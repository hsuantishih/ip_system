from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, event
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

# 建立資料庫連線
engine = create_engine('mysql+pymysql://root:password@localhost:3306/testdb')

# 建立 Session；Session 適用於對資料表的操作 CRUD
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# 多對多資料表
class HostUser(Base):
    __tablename__ = 'hosts_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    user_userid = Column(String(20), ForeignKey('users.userid'))

# 建立繼承 Base 的 Host 類別
class Host(Base):
    # 資料表名稱
    __tablename__ = 'hosts'

    # 定義欄位內容
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_type = Column(String(20))
    host_class_c = Column(String(20))
    host_min = Column(String(20))
    host_max = Column(String(20))
    host_len = Column(Integer)
    gateway = Column(String(20))
    subnet = Column(Integer)
    netmask = Column(String(20))
    deleted = Column(Boolean, default=False)
    delete_at = Column(DateTime)
    update_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    create_at = Column(DateTime, default=datetime.now())
    host_deptname = Column(String(200), default="")
    comment = Column(String(2000), default="")

    # 建立資料表關係
    host_allocation = relationship('Allocation', backref='hosts', cascade="all, delete, delete-orphan")

    # 多對多關係
    users = relationship('User', secondary='hosts_users', back_populates='hosts')

    # 一對一關係
    user_application = relationship('UserApplyHost', backref='hosts', uselist=False)

    # 設定回傳值
    def __repr__(self):
        return f"<Host id: {self.id}>"
    
# 建立繼承 Base 的 Allocation 類別
class Allocation(Base):
    # 資料表名稱
    __tablename__ = "host_allocation"

    # 定義欄位內容
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20))
    mac = Column(String(20), default="")
    owner = Column(String(20), default="")
    comment = Column(String(2000), default="")
    device = Column(String(20))
    host_id = Column(Integer, ForeignKey('hosts.id', ondelete='CASCADE'))

    # 設定回傳值
    def __repr__(self):
        return f"<Allocation id: {self.id}, host_id: {self.host_id}>"

# 建立繼承 Base 的 User 類別
class User(Base):
    # 資料表名稱
    __tablename__ = 'users'

    # 定義欄位內容
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(20), unique=True, nullable=False)
    username = Column(String(20), default="")
    deptname = Column(String(20), default="")
    ident = Column(String(20), default="")
    officephone = Column(String(20), default="")
    email = Column(String(20), default="")
    allocation = Column(String(20), default="")
    admin = Column(Boolean, default=False)

    # 建立資料表關係: 多對多
    hosts = relationship('Host', secondary='hosts_users', back_populates='users')

    # 一對多關係
    host_application = relationship('UserApplyHost', backref='users')
    
    # 設定回傳值
    def __repr__(self):
        return f"<User id: {self.id}, userid: {self.userid}>"

class UserApplyHost(Base):
    __tablename__ = 'user_apply_hosts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_userid = Column(String(20), ForeignKey('users.userid'))
    host_id = Column(Integer, ForeignKey('hosts.id'))
    applied = Column(Boolean, default=False)
    applied_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    # 設定回傳值
    def __repr__(self):
        return f"<User userid: {self.user_userid}, Host id: {self.host_id}>"

# 事件監聽器: 更新 Host 時間戳
@event.listens_for(Host.users, 'append')
@event.listens_for(Host.users, 'remove')
def update_assign_timestamp(target, value, initiator):
    # value 是 users; targer 是 host
    # 更新 Host 的時間戳
    target.update_at = datetime.now()

    session.commit()