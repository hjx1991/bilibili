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

@app.route('/')
def index():
    session.permanent = True
    session['username']='hjx'
    print(session)
    return redirect(url_for('home'))

@app.route('/login/',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        print('login get')
        return render_template('login.html')
    else:
        print('login post')
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        print(telephone,'\n',password)
        user = UserModel.query.filter_by(telephone=telephone).first()
        username =UserModel.query.filter(UserModel.telephone==telephone).all()
        print(user,username)
        if user:
            print('true')
            test=user.check_password(password)
            print('password:',test)
        if user and user.check_password(password):
            print('ok')
            session['id'] = user.id
            g.user = user
            return redirect(url_for('index'))
        else:
            return u'用户名或密码错误！'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        form = RegistForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = UserModel(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/test/',methods=['POST'])
def test():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(r'D:\\%s'% f.filename)
        return 'ok'
    else:
        return redirect(request.url)

@app.route('/home/',methods=['GET','POST'])
def home():

    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')
