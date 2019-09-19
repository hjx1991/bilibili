from flask import Flask , request , sessions , g ,url_for , abort , render_template ,flash,redirect,session,jsonify
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
        user = UserModel.query.filter_by(telephone=telephone).first()
        # username =UserModel.query.filter(UserModel.telephone==telephone).all()
        if user:
            print("数据库用户名存在")
            test=user.check_password(password)
        if user and user.check_password(password):
            session['id'] = user.id
            g.user = user
            session["username"]=telephone
            print("session type:",type(telephone))
            first='ok'
            print(first)
            return redirect(url_for('home',username=user.username,first=first))
        else:
            return u'用户名或密码错误=!'

@app.route('/home/<string:username>',methods=["POST","GET"])
def home(username):
    print(username)
    return render_template('uploading.html',username=username)

@app.route('/ajax/',methods=["POST","GET"])
def ajax():
    if request.method == 'GET':
        print("ajax get")
        return redirect(url_for('home'))
    else:
        print("ajax post")
        hostname = request.form.get("hostname")
        checkbox = request.form.get("checkbox")
        path = request.form.get("path")
        file = request.files['file']
        filename = file.filename
        if not os.path.exists(path):
            os.makedirs(path)
        if file:
            try:
                file_path = os.path.join(path,filename)
                print("file_path:",file_path)
                file.save(file_path)
            except Exception as e:
                print(e,"添加失败")
                result = "flase"
                return jsonify({"success":404})
            print("添加成功")
            result = "ok"
            return jsonify({"success":200})

if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')

