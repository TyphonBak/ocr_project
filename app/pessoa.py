from app import db

class Pessoa(db.Model):
    __tablename__ = "pessoa"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), unique=True, nullable=False)
    presente = db.Column(db.Boolean, nullable=False, default=False)

    def cria(self, dados):
        try:
            return Pessoa(nome=dados['nome'])
        except Exception as e:
            print('Erro ao criar Pessoa: ', e)
            return str(e)

    def atualiza(self, dados):
        for chave, valor in dados.items():
            setattr(self, chave, valor)

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

    def __serialize__(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "presente": "Não" if self.presente == 0 else "sim"
        }
