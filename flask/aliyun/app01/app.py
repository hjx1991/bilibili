from flask import Flask , request , sessions , g ,url_for , abort , render_template ,flash,redirect
from . import config
import os

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hjx/<id>')
def hjx(id):
    return  render_template('base.html',id = id)

@app.route('/login/')
def login():
    return  render_template('login.html')

@app.route('/pushfile/')
def pushfile():
    return render_template('pushfile.html')

@app.route('/test/',methods=['post'])
def test():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(r'D:\\%s'% f.filename)
        return 'ok'
    else:
        return redirect(request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
