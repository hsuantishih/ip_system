from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from auth.models import User
from auth.forms import LoginForm
from nckuccapi import NckuCcApi
from app import db

# 建立 Blueprint 物件
auth_bp = Blueprint('auth', __name__, template_folder='templates/auth', static_folder='static', static_url_path='/static/auth')

# 建立 nckuccapi 物件
SoapClient = NckuCcApi()

@auth_bp.before_request
def check_permissions():

    service = session['service']
    
    if not service:
        return redirect(url_for("index"))

# 定義 login_bp 路由
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 建立 Form 物件
    loginform = LoginForm()

    # 初始權限
    session['admin'] = False
    session['login'] = False

    # 驗證表單內容
    if loginform.validate_on_submit():
        # 成功入口驗證
        result = SoapClient.Authenticate(loginform.account.data, loginform.password.data)
        print(result)
        
        # 查詢使用者: 測試
        user = User.query.filter_by(userid=loginform.account.data).first()
        print(user)
        
        # 成功入口使用者 or 測試使用者
        if result['status'] == 'OK' or user:
            session['login'] = True

            if not user:
                # 串接api新增進資料庫
                user_info = SoapClient.GetUserInfo(userid=loginform.account.data)
                
                if 'ident' not in user_info:
                    user_info['ident'] = None
                    
                if 'officephone' not in user_info:
                    user_info['officephone'] = None

                user = User(
                    userid=user_info['userid'],
                    username=user_info['username'],
                    deptname=user_info['deptname'],
                    ident=user_info['ident'],
                    officephone=user_info['officephone']
                )

                db.session.add(user)
                db.session.commit()

            session['userid'] = user.userid              

            if user.admin:
                flash("登入成功", "success")
                session['admin'] = True

                return redirect(url_for('admin.list'))
            else:
                flash("登入成功", "success")

                # 轉址到 user
                return redirect(url_for('user.allocation'))
            
        else:   # 非成功入口使用者
            
            flash("輸入正確帳號與密碼", "alert")

            return redirect(url_for('auth.login'))
        
    return render_template('login.html', loginform=loginform)

@auth_bp.route('/logout')
def logout():

    session['login'] = False
    session['admin'] = False
    session['userid'] = False

    flash("成功登出", "success")
    
    return redirect(url_for('auth.login'))