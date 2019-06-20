from flask import Flask , request , sessions , g ,url_for , abort , render_template ,flash
from . import config

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
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
