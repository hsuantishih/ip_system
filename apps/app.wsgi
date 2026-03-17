import sys, os

activate_this = '/var/www/ipsystem/venv/bin/activate_this.py'

with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0, '/var/www/ipsystem')

from app import app
application = app