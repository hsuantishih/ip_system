from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    jsonify,
    send_from_directory
)
from admin.models import Host
from auth.models import User, UserApplyHost
from admin.forms import AllocationForm
from user.csv_handler import CsvHandler
from app import db
import os

user_bp = Blueprint(
    "user",
    __name__,
    template_folder="templates/user",
    static_folder="static",
    static_url_path="/static/user"
)

csv_handler = CsvHandler()

# 定義 admin_bp 路由
@user_bp.before_request
def check_permissions():
    # 登入且管理員
    permissions = session["login"]

    if not permissions:
        # 使用者沒有權限
        return redirect(url_for("auth.login"))
    
@user_bp.route("/apply", methods=["GET", "POST"])
def apply():
    # 使用 140.116.1.X 測試
    # user_ip = '140.116.7.3'
    user_ip = request.remote_addr
    user_class = user_ip.split(".")
    user_ip_type = ".".join(user_class[:2])
    user_ip_class_c = "." + user_class[2]
    print(user_ip_type, user_ip_class_c)

    match_hosts = Host.query.filter_by(
            host_type= user_ip_type,
            host_class_c= user_ip_class_c,
            deleted= False
        ).all()
    
    print(match_hosts)
    
    userid = session['userid']

    user = User.query.filter_by(userid=userid).first()
    
    # 將沒有刪除過的加入 list
    host_list = []
    for host in match_hosts:

        if not host.user_application:
            host_list.append(host)

        elif host.user_application.user_userid == userid:
            host_list.append(host)
    
    # 有刪除過，但為使用者申請過
    user_application = UserApplyHost.query.filter_by(user_userid = userid).all()

    for application in user_application:

        host = Host.query.filter_by(id=application.host_id).first()

        if host not in host_list:
            host_list.append(host)
    
    sorted_host_list = sorted(
            host_list,
            key=lambda x: (
                int(x.host_class_c[1:]),
                int(x.host_min[1:]),
                -int(x.host_max[1:])

            )
    )

    print(sorted_host_list)

    return render_template(
        'user.html',
        user_ip=user_ip,
        host_list=sorted_host_list,
        user=user
        )


@user_bp.route('/apply/submit', methods=['POST'])
def submit():
    host_list = request.get_json()

    print(host_list)
    for host_id in host_list:
        
        user_apply_host = UserApplyHost(
            host_id=host_id,
            user_userid=session['userid'],
            applied=True
        )
        db.session.add(user_apply_host)
        db.session.commit()

    content = '已提交申請，等待管理員審核'

    response = {
        'title': 'success',
        'content': content
    }

    return response

@user_bp.route('/allocation', methods=['GET', 'POST'])
def allocation():

    userid = session['userid']

    user = User.query.filter_by(userid=userid).first()

    print(user.hosts)

    hosts = []

    for host in user.hosts:
        if not host.deleted:
            hosts.append(host)

    sorted_hosts = sorted(
        hosts,
        key=lambda x: (
            int(x.host_class_c[1:]),
            int(x.host_min[1:]),
            -int(x.host_max[1:])

        )
    )

    return render_template(
        "allocation.html",
        hosts=sorted_hosts,
        user=user
    )


@user_bp.route("/allocation/query", methods=['POST'])
def allocation_query():
    # 由 Ajax 取得前端資訊
    host_id = request.get_json()

    # 查詢資料庫
    host = (
        Host.query
        .filter(Host.id == host_id)
        .first()
    )

    host_json = {}
    for key, value in host.__dict__.items():
        host_json[key] = value

    del host_json["_sa_instance_state"]

    user_json = []
    for user in host.users:
        user_dict = {}
        del user.__dict__["_sa_instance_state"]
        for key, value in user.__dict__.items():
            user_dict[key] = value
        user_json.append(user_dict)

    response = {
        "host": host_json,
        "user": user_json
        }
    
    print(response)

    return jsonify(response)

# 編輯 host_id 對應的 allocation
@user_bp.route("/allocation/<host_id>", methods=['GET', 'POST'])
def allocation_edit(host_id):

    allocationform = AllocationForm()

    host = Host.query.filter_by(id=host_id).first()

    return render_template(
        "allocation_edit.html",
        allocationform=allocationform,
        host=host
        )


@user_bp.route("/allocation/update", methods=['POST'])
def allocation_update():
    # 由 Ajax 取得前端資訊
    # data_list = [hostid, host_allocation]
    data_list = request.get_json()
    print(f"host id: {data_list[0]}; number of host_allocation: {len(data_list[1])}")

    # 取得資料
    host_id = data_list.pop(0)

    # 查詢資料庫
    from admin.host_assign_utils import handle_allocation_form

    host_allocation = handle_allocation_form(host_id)

    # 遞迴更新 host_allocation 資料庫
    for i in range(len(data_list)):
        host_allocation[i].mac = data_list[i]["mac"]
        host_allocation[i].owner = data_list[i]["owner"]
        host_allocation[i].comment = data_list[i]["comment"]
        host_allocation[i].device = data_list[i]["device"]

    db.session.commit()

    response = {"title": "success", "content": "成功更新IP分配"}

    return jsonify(response)

@user_bp.route("/allocation/download", methods=['POST'])
def allocation_file():

    host_id = request.get_json()

    host = Host.query.filter_by(id=host_id).first()

    csv_path_name, csv_file_name = csv_handler.create_initial_data(host=host)

    print(f"csv path name: {csv_path_name}")

    response = {
        'message': 'success',
        'filename': csv_file_name
    }

    return jsonify(response)

@user_bp.route("/allocation/download/<filename>")
def download(filename):
    print(f"file name: {filename}")

    return send_from_directory(
        os.path.join("user", "csv_files"),
        filename
    )

@user_bp.route("/allocation/upload", methods=['POST'])
def upload():
    # file 存在 request.files; string 存在 request.form
    file = request.files['file']
    host_id = request.form.get('host_id')

    status = csv_handler.insert_csv_data(file=file, host_id=host_id)
    
    if status:
        title = "success"
        content = "成功匯入檔案"
    else:
        title = "error"
        content = "檔案有誤"

    response = {
        "title": title,
        "content": content
        }

    return jsonify(response)