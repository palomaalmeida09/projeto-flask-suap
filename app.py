from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

with open("config.json") as json_file:
    config = json.load(json_file)

oauth.register(
    name='suap',
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    api_base_url='https://suap.ifrn.edu.br/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://suap.ifrn.edu.br/o/token/',
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    fetch_token=lambda: session.get('suap_token')
)


@app.route('/')
def index():
    if 'suap_token' in session:
        meus_dados = oauth.suap.get('v2/minhas-informacoes/meus-dados')
        return render_template('user.html', user_data=meus_dados.json())
    else:
        return render_template('index.html')

@app.route('/boletim')
def boletim():
    if 'suap_token' in session:
        boletim = oauth.suap.post('v2/minhas-informacoes/boletim/2023/1')
        return render_template('boletim.html', user_data=boletim.json())
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.suap.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    session.pop('suap_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def auth():
    token = oauth.suap.authorize_access_token()
    session['suap_token'] = token
    return redirect(url_for('index'))

