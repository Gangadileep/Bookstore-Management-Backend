from app import app
from flaskext.mysql import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
mydb = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bookstore'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['JWT_SECRET_KEY'] = 'c7e1d425acdf4bdda494a214ddf69d9f'
mydb.init_app(app)
jwt = JWTManager(app)