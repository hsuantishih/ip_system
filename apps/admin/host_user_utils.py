from auth.models import User, UserApplyHost

def handle_user_query(user_id):
    user = User.query.filter_by(id=user_id).first()

    return user

def handle_user_apply_host():

    return UserApplyHost.query.all()