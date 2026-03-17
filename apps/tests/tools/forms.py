from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

# 新增表單類別
# IP 表單
class HostForm(FlaskForm):
    # 下拉式選單的選項
    choices = [
        (24, '/24'),
        (25, '/25'),
        (26, '/26'),
        (27, '/27'),
        (28, '/28'),
        (29, '/29'),
        (30, '/30')
    ]

    ips = ['140.116']   # '10.116', '10.117'

    # 設定表單中的標籤和驗證器
    ip_ab = SelectField("IP", choices=ips)
    ip_c = StringField(validators=[DataRequired()], render_kw={'readonly': True})
    ip_d = StringField(validators=[DataRequired()])
    subnet = SelectField("Subnet", choices=choices)
    hostMin = StringField("Host Min", render_kw={'readonly': True})
    hostMax = StringField("Host Max", render_kw={'readonly': True})
    netmask = StringField("Netmask", render_kw={'readonly': True})
    gateway = StringField("Gateway", render_kw={'readonly': True})
    host_deptname = StringField("單位名稱")
    comment = StringField("備註")

    # 設定提交內容
    check = SubmitField("檢查")
    submit = SubmitField("儲存")

# 查詢使用者表單
class SearchUserForm(FlaskForm):
    # 設定表單中的標籤和驗證器
    query = StringField("識別證號")

    # 設定提交內容
    search = SubmitField("查詢")

# 新增管理員表單
class MainManagerForm(FlaskForm):
    # 設定表單中的標籤和驗證器
    main_deptname = StringField("單位名稱", render_kw={'readonly': True})
    main_username = StringField("單位管理員", render_kw={'readonly': True})
    main_ident = StringField("身分", render_kw={'readonly': True})
    main_userid = StringField("識別證號", render_kw={'readonly': True})
    main_officephone = StringField("連絡電話")
    main_email = StringField("信箱")
    main_allocation = StringField("配置地點")

class SubManagerForm(FlaskForm):
    # 設定表單中的標籤和驗證器
    sub_deptname = StringField("單位名稱", render_kw={'readonly': True})
    sub_username = StringField("單位管理員", render_kw={'readonly': True})
    sub_ident = StringField("身分", render_kw={'readonly': True})
    sub_userid = StringField("識別證號", render_kw={'readonly': True})
    sub_officephone = StringField("連絡電話")
    sub_email = StringField("信箱")
    sub_allocation = StringField("配置地點")

# 查詢ip列表
class SearchIpForm(FlaskForm):
    # 設定表單中的標籤和驗證器
    # choices 在 views.py 查詢資料庫並匯入
    type = SelectField("類別", choices=[('全部類別', '全部類別')])
    class_c = SelectField("Class C", choices=[('Class C', 'Class C')])
    deptname = StringField("單位名稱")
    username = StringField("管理員名稱")

    # 設定提交內容
    search = SubmitField("查詢")

# allocation 表單
class AllocationForm(FlaskForm):
    # 下拉式選單的選項
    options = ['請選擇設備', '設備一', '設備二', '設備三']
    choices = [(option, option) for option in options]

    # 設定表單中的標籤和驗證器
    mac = StringField("MAC 位址", render_kw={})
    owner = StringField("人員", render_kw={})
    device = SelectField("設備", choices=choices)
    comment = StringField("備註")

    # 設定提交內容
    save = SubmitField("儲存", render_kw={"type": "button"})