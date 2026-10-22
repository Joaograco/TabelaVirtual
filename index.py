from flask import Flask, render_template, request, session, redirect, make_response, url_for
from libs.schoollib import SchoolData
from libs.encrpytion import Encryption
from html import escape
from DBcm import UseDatabase
import hashlib
from libs.check import loggedin, loggedout
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher
lazy import argon2


app = Flask(__name__, static_folder='static')
load_dotenv()
hasher = PasswordHasher()
Encrypt = Encryption()

if __name__ == '__main__':
    app.config['dbconfig'] = {'host' : 'localhost', 'user' : 'webDB', 'password' : 'DBpasswd', 'database' : 'Tabela', 'auth_plugin' : 'mysql_native_password'}

else:
    app.config['dbconfig'] = {'host' : os.environ['DB_HOST'], 'user' : os.environ['USER_DB'], 'password' : os.environ['PASSWORD_DB'], 'database' : os.environ['NAME_DB'], 'auth_plugin' : 'mysql_native_password'}

mylib = SchoolData(app.config['dbconfig'])

@app.route('/')
def slash():
    cookies = request.cookies
    if 'user' in cookies:
        session['nome'] = cookies.get('nome')
        session['turma'] = cookies.get('turma')
    return redirect('/home')

@app.route('/home')
def home():
    titulo = escape('Página Inicial')
    return render_template('home.html', page_title=titulo), 200

@app.route('/aula')
def aula():
    return redirect('https://espacoestudante.seduc.se.gov.br/')

@app.route('/almoco')
@loggedin
def almoco():
    titulo = 'Fila'
    dados = mylib.almoco(session['sala'])
    ordem = dados['ordem']
    posicao = dados['pos_sala']
    return render_template('almoco.html', page_title=titulo, my=posicao, serie1=ordem[0], serie2=ordem[1], serie3=ordem[2])

@app.route('/login/')
@loggedout
def login():
    titulo = 'Login'
    if 'login_error' in session:
        return redirect('/login/contiune/err')
    return render_template('login.html', page_title=titulo)

@app.route('/login/continue', methods=['POST'])
@loggedout
def login_continue():
    titulo = 'Login'
    temp_email = request.form['email']
    session['temp_mail'] = temp_email
    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = '''select nome from users where email=%s'''
        cursor.execute(sql, (temp_email,))
        resultado = cursor.fetchone()
        if resultado != None:
            session['temp_name'] = resultado[0]
            return render_template('login_part2.html', page_title=titulo, nome=resultado[0])
        return redirect('/login/continue/criar')
    
@app.route('/login/continue/err')
def login_err():
    titulo = 'Login'
    return render_template('login_err.html', page_title=titulo, nome=session['temp_name'])
    
@app.route('/login/enviando/<tipo>', methods=['POST'])
@loggedout
def login_enviando(tipo):
    match tipo:
        case 'login':
            senha = request.form['password']
            email = session['temp_email']
            with UseDatabase(app.config['dbconfig']) as cursor:
                sql = '''select nome, sala, tipo, senha from users where email=%s'''
                cursor.execute(sql, (email,))
                resultado = cursor.fetchone()
                if resultado != None:
                    if Encrypt.verify_from_db(senha, resultado[3]):
                        response = make_response(redirect('/'))
                        nome_cookie = response.set_cookie('nome', resultado[0])
                        session['nome'] = resultado[0]
                        sala_cookie = response.set_cookie('sala', resultado[1])
                        session['sala'] = resultado[1]
                        tipo_cookie = response.set_cookie('tipo', resultado[2])
                        session['tipo'] = resultado[2]
                        session['login'] = True
                        return response
                else:
                    return redirect('/login/contiune/err')
        case 'login_err':
            senha = request.form['password']
            email = request.form['email']
            with UseDatabase(app.config['dbconfig']) as cursor:
                sql = '''select nome, sala, tipo, senha from users where email=%s'''
                cursor.execute(sql, (email,))
                resultado = cursor.fetchone()
                if Encrypt.verify_from_db(senha, resultado[3]):
                    if resultado != None:
                        response = make_response(redirect('/'))
                        nome_cookie = response.set_cookie('nome', resultado[0])
                        session['nome'] = resultado[0]
                        sala_cookie = response.set_cookie('sala', resultado[1])
                        session['sala'] = resultado[1]
                        tipo_cookie = response.set_cookie('tipo', resultado[2])
                        session['tipo'] = resultado[2]
                        session['login'] = True
                        return response
                else:
                    return redirect('/login/contiune/err')
        case 'criar':
            senha = request.form['password']
            senha_hash = Encrypt.hash(str_to_hash=senha)
            email = request.form['email']
            with UseDatabase(app.config['dbconfig']) as cursor:
                sql = '''insert into users
                (user, nome, senha, email, sala, tipo)
                values
                (%s, %s, %s, %s, %s, %s);'''
                cursor.execute(sql, (request.form['user'], request.form['nome'], senha_hash, email, request.form['sala'], 'aluno'))
                resultado = cursor.fetchone()
                response = make_response(redirect('/'))
                nome_cookie = response.set_cookie('nome', request.form['nome'])
                session['nome'] = request.form['nome']
                sala_cookie = response.set_cookie('sala', request.form['sala'])
                session['sala'] = request.form['sala']
                tipo_cookie = response.set_cookie('tipo', 'aluno')
                session['tipo'] = 'aluno'
                session['login'] = True
                return response

@app.route('/logout')
@loggedin
def logout():
    response = make_response('<h1>deslogado</h1>')
    dados = ('nome', 'sala', 'tipo')
    for dado in dados:
        if dado in session:
            session.pop(dado)
        cookie = response.set_cookie(dado, '', max_age=0)
    session.pop('login')
    return response

@app.route('/login/continue/criar', methods=['POST', 'GET'])
def login_criar():
    email = escape(session['temp_email'])
    return render_template('login_criar.html', email=email)

@app.errorhandler(404)
def error(err):
    titulo = escape('Erro 404')
    return render_template('error.html', error_code=err, title=titulo, the_title=titulo)

@app.errorhandler(argon2.exceptions.VerifyMismatchError)
def keyerror(err):
    return redirect('/login/contiune/err')

app.secret_key = 'HatsuneMiku123'
if __name__ == '__main__':
    app.run(debug=True)