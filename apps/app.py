from flask import Flask, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 建立 app 物件
app = Flask(__name__)
# 建立資料庫物件
db = SQLAlchemy()
# 設定 app 配置
app.config.from_pyfile('config.py')
# 連結 SQLAlchemy 和應用程式
db.init_app(app)
# 連結 Migrate 和應用程式
Migrate(app, db)

# Import Blueprint
from admin.views import admin_bp
from auth.views import auth_bp
from user.views import user_bp
# 註冊 Blueprint
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

@app.route('/')
def index():
    user_ip_class_c = str(request.remote_addr).split(".")

    session['service'] = True

    return redirect(url_for('auth.login'))
    
    if user_ip_class_c[0] == "140" and user_ip_class_c[1] == "116" and user_ip_class_c[2] == "2":
        session['service'] = True

        return redirect(url_for('auth.login'))
    
    else:
        session['service'] = False

        return ""
    
if __name__ == '__main__':
    app.run()