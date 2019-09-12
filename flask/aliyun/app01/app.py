from flask import Flask , request , sessions , g ,url_for , abort , render_template ,flash,redirect,session
import config
import os
from forms import RegistForm
from flask_sqlalchemy import SQLAlchemy
from decorator import login_required
from models import UserModel
# from flask_login import LoginManager


# login_manager = LoginManager()
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
db.create_all()
# login_manager.init_app(app)

@app.route('/',methods=["GET"])
def index():
    if session.get("username"):
        print("session.get[username]:"+session.get("username"))
        return redirect(url_for('home'))
    else:
        return  redirect(url_for('login'))

@app.route('/check_login',methods=["GET","POST"])
def check_login():
    session_log=session.get('username')
    if session_log:
        return "logined"
    else:
        return "false"

@app.route('/login/',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        print('login get')
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        print(telephone,password)
        user = UserModel.query.filter_by(telephone=telephone).first()
        username =UserModel.query.filter(UserModel.telephone==telephone).all()
        print(username)
        if user:
            print("数据库用户名存在")
            test=user.check_password(password)
        if user and user.check_password(password):
            session['id'] = user.id
            g.user = user
            session["username"]=telephone
            print("session:",telephone)
            return redirect(url_for('index',username=username))
        else:
            return u'用户名或密码错误！'

@app.route('/home/',methods=["POST","GET"])
def home():
    try:
        if session.get('username'):
            return  render_template('images.html')
    except KeyError as e:
        print(e)
        return render_template('login.html')

@app.route('/images/',methods=["GET"])
def images():
    if request.method == 'GET':
        pritn('跳转iamges.html')
        return render_template('images.html')
# @app.route('/regist/',methods=['GET','POST'])
# def regist():
#     if request.method == 'GET':
#         return render_template('regist.html')
#     else:
#         form = RegistForm(request.form)
#         if form.validate():
#             telephone = form.telephone.data
#             username = form.username.data
#             password = form.password1.data
#             user = UserModel(telephone=telephone,username=username,password=password)
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('login'))
#
# @app.route('/test/',methods=['POST'])
# def test():
#     if request.method == 'POST':
#         f = request.files['file']
#         # f.save(r'D:\\%s'% f.filename)
#         return 'ok'
#     else:
#         return redirect(request.url)
#
# @app.route('/home/',methods=['GET','POST'])
# def home():
#     return render_template('images.html')

if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')
