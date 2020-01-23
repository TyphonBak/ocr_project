from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.services.imagem_manage import busca_texto_em_imagem

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    CORS(app)

    from os import environ
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

    db.init_app(app)

    from app.services.pessoa_manage import listar as listar_pessoa, mostrar_presentes, marca_presenca
    # Paginas

    @app.route('/')
    def index():
        context = {
            'titulo': 'Entrada'
        }
        return render_template('index.html', context=context)

    @app.route('/presentes')
    def lista_presentes():
        lista_de_presenca = listar_pessoa()
        context = {
            'titulo': 'Lista de Presentes',
            'lista_de_pessoas': lista_de_presenca
        }
        return render_template('lista.html', context=context)

    @app.route('/confirmados')
    def mostra_confirmados():
        lista_de_presentes = mostrar_presentes()
        context = {
            'titulo': 'Lista de Confirmados',
            'lista_de_pessoas': lista_de_presentes
        }
        return render_template('lista.html', context=context)

    # Funções

    @app.route('/salvar-imagem', methods=['POST'])
    def salvar():
        caminho_da_imagem = request.form['link_imagem']
        nome = busca_texto_em_imagem(caminho_da_imagem)
        code, resp = marca_presenca({'nome': nome})
        return jsonify({"mensagem": nome}), 200

    @app.route('/reseta/<segredo>')
    def reseta_presencas(segredo):
        if segredo == 'todos':        
            return redirect(url_for('index'))
        abort(404)

    return app
