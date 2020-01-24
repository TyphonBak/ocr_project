from app.settings import db
from app.pessoa import Pessoa

def cria(dados):
    pessoa = Pessoa.cria(dados)
    if pessoa:
        db.session.add(pessoa)
        db.session.commit()
    
        return 200, pessoa.__serialize__()
    return 400, None

def busca(dados):
    try:
        pessoa = Pessoa.query.filter_by(nome=dados['nome']).first()
        if pessoa:
            return 200, pessoa.__serialize__()
        return 404, None
    except Exception as e:
        print('Erro ao buscar Pessoa: ', e)
        return 400, None

def atualiza(dados):
    try:
        pessoa_query = Pessoa.query.get(dados['id'])
        pessoa_query.atualiza(dados)
        db.session.commit()
        return 200, pessoa_query.__serialize__()
    except Exception as e:
        print("Erro ao atualizar Pessoa: ", e)
        return 400, None

def deleta(id):
    pessoa = Pessoa.query.get(id)
    if pessoa:
        try:
            db.session.delete(pessoa)
            db.session.commit()
            return 204, None
        except Exception as e:
            print('Erro ao deletar Pessoa: ', e)
            return 400, None
    return 404, None

def marca_presenca(dados):
    try:
        code, pessoa = busca(dados)
        if code == 200:
            pessoa['presente'] = 1
            return atualiza(pessoa)
        return code, pessoa
    except Exception as e:
        print('Erro ao marcar presenca: ', e)
        return 400, str(e)

def mostrar_presentes():
    try:
        return [pessoa.nome for pessoa in Pessoa.query.filter_by(presente=True).all()]
    except Exception as e:
        print('Erro ao mostrar presentes. ', e)
        return None

def listar():
    try:
        return [pessoa.nome for pessoa in Pessoa.query.all()]
    except Exception as e:
        print('Erro ao listar Pessoa: ', e)
        return None

def reseta_presentes():
    try:
        Pessoa.query.filter_by(presente=True).update(presente=False)
    except Exception as e:
        print('Erro ao resetar presentes! ', e)
