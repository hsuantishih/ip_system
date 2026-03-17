from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    session,
    json,
)
from admin.forms import (
    HostForm,
    SearchUserForm,
    MainManagerForm,
    SubManagerForm,
    SearchIpForm,
    AllocationForm,
)
from admin.models import Host
from sqlalchemy import func, Integer
from app import db

# 建立 Blueprint 物件
admin_bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates/admin",
    static_folder="static",
    static_url_path="/static/admin",
)

# 定義 admin_bp 路由
@admin_bp.before_request
def check_permissions():
    # 登入且管理員
    permissions = session["admin"] and session["login"]

    if not permissions:
        # 使用者沒有權限
        return redirect(url_for("auth.login"))


# 顯示 ip 清單
@admin_bp.route("/list", methods=["GET", "POST"])
def list():
    from admin.host_list_utils import query_hosts, query_and_append_choices

    # 查詢條件
    host_condition = Host.host_type
    class_c_condition = func.substring(Host.host_class_c, 2).cast(Integer)
    
    # 建立表單物件
    query_and_append_choices("type", host_condition, lambda x: (x[0], x[0]))
    query_and_append_choices("class_c", class_c_condition, lambda x: ("." + str(x[0]), x[0]))

    # 建立表單物件
    searchIpform = SearchIpForm()

    # 判斷查詢內容
    search_type = searchIpform.type.data
    search_class_c = searchIpform.class_c.data
    search_deptname = searchIpform.deptname.data
    search_username = searchIpform.username.data

    # Main logic
    if searchIpform.validate_on_submit():
        hosts = query_hosts(
            search_username=search_username,
            search_deptname=search_deptname,
            search_type=search_type,
            search_class_c=search_class_c,
        )
        print(f"{len(hosts)} 筆資料符合查詢結果")

        if not hosts:
            flash("查無資料", "alert")

    # Initial page load
    else:
        hosts = (
            Host.query.filter(Host.deleted == False)
            .order_by(
                func.substring(Host.host_class_c, 2).cast(Integer),
                func.substring(Host.host_min, 2).cast(Integer),
            )
            .all()
        )


    return render_template("list.html", hosts=hosts, searchIpform=searchIpform)


# 清空 ip 清單的管理員
@admin_bp.route("/list/remove", methods=["POST"])
def remove():
    # 由 Ajax 取得前端資訊
    host_id_list = request.get_json()

    for host_id in host_id_list:
        # 查詢資料庫
        host = Host.query.filter_by(id=host_id).first()

        # 清空單位&備註
        host.host_deptname = ""
        host.comment = ""

        db.session.commit()

        # 清空管理員，sqlalchemy
        # 只接受remove，提交後會剩下串列的下一個，所以模仿pop
        while host.users:
            host.users.remove(host.users[0])
            db.session.commit()

        print(f"已移除 {host} 的資料，管理員欄位為 {host.users}")

    response = {"title": "success", "content": "成功移除資料"}

    return jsonify(response)


@admin_bp.route("/list/query", methods=["POST"])
def query():
    # 由 Ajax 取得前端資訊
    host_id = request.get_json()

    # 查詢資料庫
    host = (
        Host.query
        .filter(Host.deleted == False, Host.id == host_id)
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

    return jsonify(response)


@admin_bp.route("/assign/<host_id>", methods=["GET", "POST"])
def assign(host_id):
    # 建立表單物件
    hostform = HostForm()
    main_managerform = MainManagerForm()
    sub_managerform = SubManagerForm()
    searchform = SearchUserForm()
    allocationform = AllocationForm()

    # 需先經過檢查才能提交表單
    if hostform.validate_on_submit():
        print("---IP 表單資料---")
        for field in hostform:
            print(f"{field.name}: {field.data}")

        print("---Main User 表單資料---")
        for field in main_managerform:
            print(f"{field.name}: {field.data}")

        print("---Sub User 表單資料---")
        for field in sub_managerform:
            print(f"{field.name}: {field.data}")
        print("--------------------")

        # 儲存 conflict_data 的 host_id
        conflict_list_id = []
        conflict = False

        # 向資料庫檢查資料
        from admin.host_assign_utils import handle_check_host

        data = handle_check_host(hostform)

        print(data)
        status = data["status"]
        print(status)

        if status == "exist":
            flash("成功更新IP網段", "success")

            # 代表要更新現有資料
            current_edit_host = data["host_list"][0]

        elif status == "split":

            from admin.host_assign_utils import handle_split_host

            current_edit_host = handle_split_host(data, hostform)

        elif status == "merge":
            # 檢查有無管理者
            host_list_db = data["host_list"]

            # 查詢當前資料的 host
            current_edit_host = Host.query.filter_by(id=host_id).first()

            for host in host_list_db:
                # 儲存 conflict_data 的 host_id
                if current_edit_host.id != host.id:
                    conflict_list_id.append(host.id)

                    if host.users or host.host_deptname or host.comment:
                        conflict = True

            if conflict:

                from admin.host_assign_utils import handle_merge_conflict_host

                merge_form_data = handle_merge_conflict_host(conflict_list_id, main_managerform, sub_managerform, hostform)

                session["merge_form_data"] = json.dumps(merge_form_data)

                return redirect(url_for("admin.assign", host_id=host_id))

            # 提示訊息
            flash("成功合併IP網段", "success")

            from admin.host_assign_utils import handle_delete_host, handle_generate_host

            handle_delete_host(host_list_db)
            
            current_edit_host = handle_generate_host(hostform, current_edit_host)



        # 更新當前的 host 資料
        current_edit_host.host_deptname = hostform.host_deptname.data
        current_edit_host.comment = hostform.comment.data

        db.session.commit()

        # 初始 host.users
        while current_edit_host.users:
            current_edit_host.users.remove(current_edit_host.users[0])
            db.session.commit()

        # 判斷是否提交管理員
        if main_managerform.main_userid.data:

            from admin.host_assign_utils import handle_main_managerform

            handle_main_managerform(main_managerform, current_edit_host)
            
        
        if sub_managerform.sub_userid.data:
            from admin.host_assign_utils import handle_sub_managerform

            handle_sub_managerform(sub_managerform, current_edit_host)


        # 更新當前 host_id
        host_id = current_edit_host.id

        return redirect(url_for("admin.assign", host_id=host_id))

    # 查詢 join 資料表
    current_host = (
            Host.query.filter(
                Host.deleted == False,
                Host.id == host_id
                ).first()
        )
    

    
    from admin.host_assign_utils import handle_allocation_form

    host_allocation = handle_allocation_form(host_id)

    # 透過 redirect 進入頁面
    hosts = []
    # 取得 conflict_list_id
    conflict_list_id = session.get("conflict_list_id")
    print(f"conflict list id: {conflict_list_id}")
    session.pop("conflict_list_id", default=None)

    # 收集衝突資料
    if conflict_list_id:
        for id in conflict_list_id:
            conflict_data = (
                Host.query.filter(
                    Host.deleted == False,
                    Host.id == id
                ).first()
            )
            
            hosts.append(conflict_data)

        print(f"從資料庫取得的 conflict data {hosts}")

    print("-----當前資料-----")
    print(f"host_id: {host_id:>5}")
    print(f"users: {current_host.users}")
    print(f"allocation: {len(host_allocation):>5} 筆")
    print("------------------")

    # merge form data
    merge_form_data = []
    merge_form_data_json = session.get("merge_form_data")
    if merge_form_data_json:
        merge_form_data = json.loads(merge_form_data_json)
        print(merge_form_data)

        session.pop("merge_form_data", default=None)

    return render_template(
        "assign.html",
        hostform=hostform,
        searchform=searchform,
        main_managerform=main_managerform,
        sub_managerform=sub_managerform,
        allocationform=allocationform,
        hosts=hosts,
        host_allocation=host_allocation,
        current_host=current_host,
        merge_form_data=merge_form_data,
    )


# 查詢結果
@admin_bp.route("/assign/search", methods=["POST"])
def search():
    # 由 Ajax 取得前端資訊
    query = request.get_json()
    print(f"人員證號 {query}")

    from admin.host_search_utils import handle_user_info

    result = handle_user_info(query)

    if result:
        # 回傳結果
        response = {
            "title": "success",
            "content": "查詢成功",
            "result": result,
            "message": True,
        }
    else:
        response = {"title": "alert", "content": "請填寫正確識別證號", "message": False}

    return jsonify(response)


# 更新 allocation 清單
@admin_bp.route("/assign/allocation", methods=["POST"])
def edit():
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


# 編輯 UserApplyHosts
@admin_bp.route("/manage", methods=["POST", "GET"])
def manage():
    from admin.host_user_utils import handle_user_query, handle_user_apply_host

    user_apply_hosts = handle_user_apply_host()

    user_applications = []
    for application in user_apply_hosts:

        host = Host.query.filter_by(id=application.host_id).first()

        user = handle_user_query(application.user_userid)

        application_tuple = (host, user)
        user_applications.append(application_tuple)

    sorted_user_applications = sorted(
        user_applications,
        key=lambda x: (
            int(x[0].host_class_c[1:]),
            int(x[0].host_min[1:]),
            -int(x[0].host_max[1:])

        )
    )

    print(sorted_user_applications)

    return render_template(
        "manage.html",
        user_applications=sorted_user_applications
        )

@admin_bp.route('/manage/update', methods=['POST'])
def update():
    data_list = request.get_json()
    print(data_list)

    host = Host.query.filter_by(id=data_list['host_id']).first()

    from admin.host_user_utils import handle_user_query

    user = handle_user_query(userid=data_list['user_userid'])

    if user not in host.users:
        host.users.append(user)
        title = "success"
        content = "成功指派管理員"

        db.session.commit()
    else:
        title = "alert"
        content = "此申請者已為管理員"


    print(f"Host.users {host.users}")

    response = {
        "title": title, 
        "content": content
        }

    return jsonify(response)