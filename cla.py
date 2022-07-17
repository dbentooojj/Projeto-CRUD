import sqlite3
import requests

import a

conexao = sqlite3.connect('banco-dados.db')
cursor = conexao.cursor()


def end_user(cep):
    response = requests.get(f'https://cep.awesomeapi.com.br/json/{cep}')
    response_json = response.json()
    return response_json['state'], response_json['city'], response_json['district'], response_json['address']


class Cliente:
    def __init__(self, nome, idade, cpf, cep, numero):
        self.nome = nome
        self.idade = idade
        self.cpf = cpf
        self.cep = cep
        self.numero = numero

    def Cadastrar_Cliente(self):
        try:
            end_user(self.cep)
            cursor.execute('INSERT INTO Clientes (nome, idade, cpf, cep, rua, estado, cidade, bairro, numero) VALUES '
                           '(?, '
                           '?, ?, ?, ?, ?, ?, ?, ?)',
                           (self.nome, self.idade, self.cpf, self.cep, end_user(self.cep)[3], end_user(self.cep)[0],
                            end_user(self.cep)[1], end_user(self.cep)[2], self.numero))
            conexao.commit()
            print('-' * 50)
            print('Cliente cadastrado com sucesso!')
        except:
            print('-' * 50)
            print('Erro ao cadastrar cliente!')


class Produto:
    def __init__(self, nome_produto, familia_produto, codigo):
        self.nome_produto = nome_produto
        self.familia_produto = familia_produto
        self.codigo = codigo

    def Cadastrar_Produto(self):
        try:
            a.verificar_codigo(self.codigo)
            cursor.execute('INSERT INTO Produtos (nome_produto, familia_produto, codigo) VALUES (?, ?, ?)',
                           (self.nome_produto, self.familia_produto, self.codigo))
            conexao.commit()
            print('-' * 50)
            print('Produto cadastrado com sucesso!')
        except:
            print('-' * 50)
            print('Erro ao cadastrar produto!')


class Venda:
    def __init__(self, data_venda, codigo, cpf, quantidade, valor_unitario, valor_total):
        self.data_venda = data_venda
        self.codigo = codigo
        self.cpf = cpf
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total

    def cadastrar_venda(self):
        try:
            cursor.execute('INSERT INTO Vendas (data_venda, codigo, cpf, quantidade, valor_unitario, valor_total) '
                           'VALUES (?, ?, ?, ?, ?, ?)',
                           (self.data_venda, self.codigo, self.cpf, self.quantidade, self.valor_unitario, self.valor_total))
            conexao.commit()
            print('-' * 50)
            print('Venda cadastrada com sucesso!')
        except:
            print('-' * 50)
            print('Erro ao cadastrar venda!')

