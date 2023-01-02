from flask import Flask
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail
from itsdangerous import URLSafeSerializer



app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.debug = True

####################################
# Initiate Mail-Sending / Validation
####################################

mail = Mail(app)
email_confirmation_Serializer = URLSafeSerializer(app.config['SECRET_KEY'])


####################################
# Create db
####################################
""" app.config['SECRET_KEY'] = 'ezriteXic62N9l2F1qzTA1hUKdUrBR1e'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database/clueful.db' """

csrf = CSRFProtect()
csrf.init_app(app)
db = SQLAlchemy(app)


bcrypt = Bcrypt(app)

####################################
# Create Socket
####################################
socket = SocketIO(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "id=user_login_required User needs to be logged in to enter this page"
login_manager.login_message_category = "warning"

from clueful import routes, sockets
####################################
# Reload when files get updated
####################################
assets = Environment(app)
assets.url = app.static_url_path

scss = Bundle(
    'sass/main.scss',
    filters='pyscss',
    depends=('sass/**/*.scss'),
    output='gen/all.css')
assets.register('scss_all', scss)

