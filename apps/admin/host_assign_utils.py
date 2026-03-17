from admin.ip_calculator import IPCalculator
from app import db
from flask import flash, session
from admin.models import Host, Allocation
from datetime import datetime
from auth.models import User


Calculator = IPCalculator()

def handle_check_host(hostform):
    data = Calculator.check_for_db(
            hostform_type=hostform.ip_ab.data,
            hostform_class_c=hostform.ip_c.data,
            hostform_min=hostform.hostMin.data.split(".")[-1],
            hostform_max=hostform.hostMax.data.split(".")[-1],
        )
    
    return data


def handle_split_host(data, hostform):

    host_db = data["host_list"][0]

    # 先 split 並匯入資料庫，再刪除
    print(f"刪除父節點，此父節點應當只有{data['host_list']}")  # 應該只有一個

    flash("成功分割IP網段", "success")
    print("進行切割並生成allocation")
    host_min = host_db.host_type + host_db.host_class_c + host_db.host_min
    host_max = host_db.host_type + host_db.host_class_c + host_db.host_max
    Calculator.generate_ip_group(
        host_min=host_min,
        host_max=host_max,
        subnet=hostform.subnet.data,
        host_deptname=hostform.host_deptname.data,
        comment=hostform.comment.data,
        host_users=host_db.users
    )

    # 刪除 host_list -> 自動刪除 host_allocation
    host_to_delete = Host.query.filter_by(id=host_db.id).first()
    host_to_delete.deleted = True
    host_to_delete.delete_at = datetime.now()

    db.session.commit()

    # 查詢表單是資料庫新生成的哪個 group
    current_edit_host = Host.query.filter_by(
        host_type=hostform.ip_ab.data,
        host_class_c="." + hostform.ip_c.data,
        host_min="." + hostform.hostMin.data.split(".")[-1],
        host_max="." + hostform.hostMax.data.split(".")[-1],
        deleted=False,
            ).first()
    
    return current_edit_host

def handle_merge_conflict_host(conflict_list_id, main_managerform, sub_managerform, hostform):
    conflict_list_len = len(conflict_list_id)
    flash(f"{conflict_list_len} 筆資料中已分配資料", "alert")
    print(f"{conflict_list_len} 筆資料中已分配資料")

    # 使用 session 儲存 conflict_list
    session["conflict_list_id"] = conflict_list_id

    # 儲存表單資料
    merge_form_data = []
    merge_main_managerform_data = {}
    merge_sub_managerform_data = {}
    merge_hostform_data = {}

    for field in main_managerform:
        merge_main_managerform_data[field.name] = field.data

    for field in sub_managerform:
        merge_sub_managerform_data[field.name] = field.data

    for field in hostform:
        merge_hostform_data[field.name] = field.data

    merge_form_data.append(merge_hostform_data)
    merge_form_data.append(merge_main_managerform_data)
    merge_form_data.append(merge_sub_managerform_data)

    return merge_form_data


def handle_delete_host(host_list_db):
    for host_to_delete in host_list_db:
        # 刪除 host_list -> 自動刪除 host_allocation
        host_to_delete = Host.query.filter_by(id=host_to_delete.id).first()
        host_to_delete.deleted = True
        host_to_delete.delete_at = datetime.now()

    db.session.commit()

def handle_generate_host(hostform, current_edit_host):
    current_edit_host = Host(
                host_type=hostform.ip_ab.data,
                host_class_c="." + hostform.ip_c.data,
                host_min="." + hostform.hostMin.data.split(".")[-1],
                host_max="." + hostform.hostMax.data.split(".")[-1],
                host_len=int(hostform.hostMax.data.split(".")[-1])
                - int(hostform.hostMin.data.split(".")[-1])
                + 1,
                gateway="." + hostform.gateway.data.split(".")[-1],
                subnet=hostform.subnet.data,
                netmask=hostform.netmask.data,
                host_deptname=hostform.host_deptname.data,
                comment=hostform.comment.data,
            )
    
    db.session.add(current_edit_host)
    db.session.commit()

    Calculator.generate_ip_range(
        host_min=hostform.hostMin.data,
        host_max=hostform.hostMax.data,
        host_id=current_edit_host.id
    )

    return current_edit_host


def handle_main_managerform(main_managerform, current_edit_host):
    main_user = User.query.filter_by(userid=main_managerform.main_userid.data).first()
            
    print(f"更新 {main_user} 管理員資料")

    if not main_user:
        main_user = User(
            userid=main_managerform.main_userid.data,
            username=main_managerform.main_username.data,
            deptname=main_managerform.main_deptname.data,
            ident=main_managerform.main_ident.data,
            officephone=main_managerform.main_officephone.data,
            email=main_managerform.main_email.data,
            allocation=main_managerform.main_allocation.data,
        )

        db.session.add(main_user)
        db.session.commit()
    else:
        # 更新使用者資料
        main_user.officephone=main_managerform.main_officephone.data,
        main_user.email=main_managerform.main_email.data,
        main_user.allocation=main_managerform.main_allocation.data,

        db.session.commit()

    current_edit_host.users.append(main_user)
    db.session.commit()

def handle_sub_managerform(sub_managerform, current_edit_host):
    sub_user = User.query.filter_by(userid=sub_managerform.sub_userid.data).first()
    print(f"更新 {sub_user} 管理員資料")

    if not sub_user:
        sub_user = User(
            userid=sub_managerform.sub_userid.data,
            username=sub_managerform.sub_username.data,
            deptname=sub_managerform.sub_deptname.data,
            ident=sub_managerform.sub_ident.data,
            officephone=sub_managerform.sub_officephone.data,
            email=sub_managerform.sub_email.data,
            allocation=sub_managerform.sub_allocation.data,
        )

        db.session.add(sub_user)
        db.session.commit()
    else:
        sub_user.officephone=sub_managerform.sub_officephone.data,
        sub_user.email=sub_managerform.sub_email.data,
        sub_user.allocation=sub_managerform.sub_allocation.data,

        db.session.commit()
    current_edit_host.users.append(sub_user)
    db.session.commit()

def handle_allocation_form(host_id):
    host_allocation = Allocation.query.filter_by(host_id=host_id).all()

    return host_allocation

