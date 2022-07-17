import sqlite3
import cla
import time

conexao = sqlite3.connect('banco-dados.db')
cursor = conexao.cursor()


def escolher():
    print('''
              [1]   - Cadastrar cliente 
              [2]   - Alterar cliente 
              [3]   - Excluir cliente 
              [4]   - Cadastrar produto 
              [5]   - Alterar produto 
              [6]   - Excluir produto 
              [7]   - Cadastrar venda 
              [8]   - Alterar venda 
              [9]   - Excluir venda 
              [10]  - Listar clientes 
              [11]  - Listar produtos 
              [12]  - Listar vendas 
              [13]  - Sair do programa 
              ''')


def validar_Cpf():
    validaCPF = True
    while validaCPF:
        cpf = input('Digite o CPF do cliente: ')
        if len(cpf) != 11:
            print('CPF inválido!')
            continue
        else:
            cpfReal = cpf
            totala = 0
            totalb = 0
            cont = 0
            b = 10
            a = 0
            cpf = ' '.join(filter(str.isalnum, cpf))
            cpf = cpf.split()

        while cont < 9:
            totala = totala + int(cpf[a]) * b
            a += 1
            b -= 1
            cont += 1
        cont = 0
        b = 11
        a = 0
        while cont < 10:
            totalb = totalb + int(cpf[a]) * b
            a += 1
            b -= 1
            cont += 1
        p1 = (totala * 10) % 11
        p2 = (totalb * 10) % 11
        if p1 == int(cpf[9]) and p2 == int(cpf[10]):
            validaCPF = False
            return cpfReal
        else:
            print("Digite um CPF válido!")


def verificar_cpf_banco(cpf):
    while True:
        conexao = sqlite3.connect('banco-dados.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM Clientes WHERE cpf = ?', (cpf,))
        if cursor.fetchone():
            return True
        else:
            return False


def verificar_codigo(codigo):
    while True:
        conexao = sqlite3.connect('banco-dados.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM Produtos WHERE codigo = ?', (codigo,))
        if cursor.fetchone():
            return True
        else:
            return False


def verificar_id(id):
    while True:
        conexao = sqlite3.connect('banco-dados.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM Vendas WHERE id = ?', (id,))
        if cursor.fetchone():
            return True
        else:
            return False


def ifo_Cliente():
    cpf = validar_Cpf()
    if verificar_cpf_banco(cpf):
        print('CPF já cadastrado!')
        return
    else:
        nome = input('Digite o nome do cliente: ')
        idade = int(input('Digite a idade do cliente: '))
        cep = input('Digite o cep do cliente: ')
        numero = int(input('Digite o numero do cliente: '))
        cliente = cla.Cliente(nome, idade, cpf, cep, numero)
        cliente.Cadastrar_Cliente()


def alterar_dados_cliente():
    msg = ['nome', 'idade', 'CPF', 'CEP', 'numero']
    opcoes = ['nome', 'idade', 'cpf', 'cep', 'numero', 'todas', 'voltar']
    cpf_da_alteracao = input('Digite o CPF do cliente que deseja alterar: ')
    verificar_cpf_banco(cpf_da_alteracao)
    if not verificar_cpf_banco(cpf_da_alteracao):
        print('-' * 50)
        print('CPF não cadastrado ou Inválido!')

    else:
        op_menu()
        opcao_selecionada = int(input('Digite qual opcao quer alterar? '))

        if opcao_selecionada == 8:
            print('-' * 50)
            return

        elif opcao_selecionada == 6:
            try:
                nome = input('Digite o novo nome do cliente: ')
                idade = int(input('Digite a nova idade do cliente: '))
                cpf = input('Digite o novo cpf do cliente: ')
                cep = input('Digite o novo cep do cliente: ')
                numero = int(input('Digite o novo numero do cliente: '))
                a = cla.end_user(cep)
                cursor.execute(
                    'UPDATE Clientes SET nome = ?, idade = ?, cpf = ?, cep = ?, estado = ?, cidade = ?, bairro = ?, '
                    'rua = ?, numero = ?  WHERE '
                    'cpf = ?', (nome, idade, cpf, cep, a[0], a[1], a[2], a[3], numero, cpf_da_alteracao))
                conexao.commit()
                print('-' * 50)
                print('Cliente alterado com sucesso!')
            except:
                print('-' * 50)
                print('Erro ao alterar cliente!')

        elif opcao_selecionada == 4:
            while True:
                try:
                    cep1 = input('Digite o novo cep do cliente: ')
                    b = cla.end_user(cep1)
                    cursor.execute('UPDATE Clientes SET cep = ?, estado = ?, cidade = ?, bairro = ?, rua = ? WHERE '
                                   'cpf = ?',
                                   (cep1, b[0], b[1], b[2], b[3], cpf_da_alteracao))
                    conexao.commit()
                    print('-' * 50)
                    print('Cep alterado com sucesso!')
                    break
                except:
                    print('-' * 50)
                    print('CEP inválido!')

        elif opcao_selecionada == 3:
            while True:
                try:
                    cpf = input('Digite o novo cpf do cliente: ')
                    verificar_cpf_banco(cpf)
                    print('-' * 50)
                    if verificar_cpf_banco(cpf):
                        print('CPF já cadastrado!')
                        print('-' * 50)
                    else:
                        validar_Cpf()
                        cursor.execute('UPDATE Clientes SET cpf = ? WHERE cpf = ?', (cpf, cpf_da_alteracao))
                        conexao.commit()
                        print('-' * 50)
                        print('CPF alterado com sucesso!')
                        break
                except:
                    print('-' * 50)
                    print('CPF inválido!')


        else:
            novo_valor = input(f'Digite o novo {msg[opcao_selecionada - 1]} do cliente: ')
            cursor.execute(f'UPDATE Clientes SET {opcoes[opcao_selecionada - 1]} = ? WHERE cpf = ?',
                           (novo_valor, cpf_da_alteracao))
            conexao.commit()
            print('-' * 50)
            print('Cliente alterado com sucesso!')


def excluir_cliente():
    cpf = input('Digite o CPF do cliente que deseja excluir : ')
    verificar_cpf_banco(cpf)
    if not verificar_cpf_banco(cpf):
        print('CPF não cadastrado!')
        excluir_cliente()
    else:
        cursor.execute('SELECT * FROM Clientes WHERE cpf = ?', (cpf,))
        linha = cursor.fetchone()
        print('-' * 50)
        print(f'ID: {linha[0]} \nNome: {linha[1]} \nCPF: {linha[3]}')
        print('-' * 50)
        print('Deseja excluir o cliente? (S/N)')
        opcao = input('>>> ')
        if opcao.upper() == 'S':
            cursor.execute('DELETE FROM Clientes WHERE cpf = ?', (cpf,))
            conexao.commit()
            print('-' * 50)
            print('Cliente excluido com sucesso!')
        else:
            print('-' * 50)
            print('Cliente não excluido!')


def op_menu():
    print('''
    Qual campo deseja alterar?
    [1] - Nome
    [2] - Idade
    [3] - CPF
    [4] - CEP
    [5] - Numero
    [6] - Alterar todos os dados
    [8] - Voltar
    ''')


def op_menu_produto():
    print('''
    Qual campo deseja alterar?
    [1] - Nome
    [2] - Familia do produto
    [3] - Código
    [4] - Alterar todos os dados
    [5] - Voltar
    ''')


def op_menu_venda():
    print('''
    Qual campo deseja alterar?
    [1] - Data da venda
    [2] - Codigo do produto
    [3] - Cliente
    [4] - quantidade
    [5] - Valor Unitário
    [6] - Valor Total da venda
    [7] - Alterar todos os dados
    [8] - Voltar
    ''')


def inf_produto():
    codigo = int(input('Digite o código do produto: '))
    if not verificar_codigo(codigo):
        nome_produto = input('Digite o nome do produto: ')
        familia_produto = input('Digite a familia do produto: ')
        produto = cla.Produto(nome_produto, familia_produto, codigo)
        produto.Cadastrar_Produto()
    else:
        print('-' * 50)
        print('Código já cadastrado!')


def alterar_dados_produto():
    msg = ['Nome', 'Familia', 'Código de barras']
    opcoes = ['nome_produto', 'familia_produto', 'codigo', 'todas', 'voltar']
    codigo_alteracao = input('Digite o codigo de barras do produto que deseja alterar: ')
    verificar_codigo(codigo_alteracao)
    if not verificar_codigo(codigo_alteracao):
        print('Codigo de barras não cadastrado!')
        alterar_dados_produto()
    else:
        cursor.execute('SELECT * FROM Produtos WHERE codigo = ?', (codigo_alteracao,))
        linha = cursor.fetchone()
        print('-' * 50)
        print(f'ID: {linha[0]} \nNome: {linha[1]} \nFamilia: {linha[2]}  \nCodigo: {linha[3]}')
        print('-' * 50)
        op_menu_produto()
        opcao_selecionada = int(input('Digite qual opcao quer alterar? '))

        if opcao_selecionada == 5:
            return

        elif opcao_selecionada == 4:
            try:
                nome = input('Digite o novo nome do produto: ')
                familia = input('Digite a nova familia do produto: ')
                codigo_barras = input('Digite o novo codigo de barras do produto: ')
                cursor.execute(
                    'UPDATE Produtos SET nome_produto = ?, familia_produto = ?, codigo = ? WHERE codigo '
                    '= ?', (nome, familia, codigo_barras, codigo_alteracao))
                conexao.commit()
                print('-' * 50)
                print('Produto alterado com sucesso!')
            except:
                print('-' * 50)
                print('Erro ao alterar produto!')

        else:
            novo_valor = input(f'Digite o novo {msg[opcao_selecionada - 1]} do produto: ')
            cursor.execute(f'UPDATE Produtos SET {opcoes[opcao_selecionada - 1]} = ? WHERE codigo = ?',
                           (novo_valor, codigo_alteracao))
            conexao.commit()
            print('-' * 50)
            print('Produto alterado com sucesso!')


def excluir_produto():
    codigo_barras = input('Digite o codigo de barras do produto que deseja excluir: ')
    verificar_codigo(codigo_barras)
    if not verificar_codigo(codigo_barras):
        print('Codigo de barras não cadastrado!')

    else:
        cursor.execute('SELECT * FROM Produtos WHERE codigo = ?', (codigo_barras,))
        linha = cursor.fetchone()
        print('-' * 50)
        print(f'ID: {linha[0]} \nNome: {linha[1]} \nFamilia: {linha[2]}  \nCodigo: {linha[3]}')
        print('-' * 50)
        print('Deseja excluir o produto? (S/N)')
        opcao = input('>>> ')
        if opcao.upper() == 'S':
            cursor.execute('DELETE FROM Produtos WHERE codigo = ?', (codigo_barras,))
            conexao.commit()
            print('-' * 50)
            print('Produto excluido com sucesso!')
        else:
            print('-' * 50)
            print('Produto não excluido!')


def cadastrar_vendaa():
    cpf = input('Digite o cpf do cliente: ')
    verificar_cpf_banco(cpf)
    if not verificar_cpf_banco(cpf):
        print('CPF não cadastrado!')
        cadastrar_vendaa()
    else:
        cursor.execute('SELECT * FROM Clientes WHERE cpf = ?', (cpf,))
        linha = cursor.fetchone()
        print('-' * 50)
        print(f'ID: {linha[0]} \nNome: {linha[1]} \nIdade: {linha[2]}  \nCPF: {linha[3]}')
        print('-' * 50)
        print('Deseja continuar? (S/N)')
        opcao = input('>>> ')
        while True:
            if opcao.upper() == 'S':
                codigo = input('Digite o codigo de barras do produto: ')
                verificar_codigo(codigo)
                if not verificar_codigo(codigo):
                    print('Codigo de barras não cadastrado!')
                else:
                    cursor.execute('SELECT * FROM Produtos WHERE codigo = ?', (codigo,))
                    linha = cursor.fetchone()
                    print('-' * 50)
                    print(f'ID: {linha[0]} \nProduto: {linha[1]}')
                    print('-' * 50)
                    data_venda = input('Digite a data da venda: ')
                    quantidade = int(input('Digite a quantidade do produto: '))
                    valor_unitario = float(input('Digite o valor unitario do produto: '))
                    valor_total = float(input('Digite o valor total da venda: '))
                    venda = cla.Venda(data_venda, codigo, cpf, quantidade, valor_unitario, valor_total)
                    venda.cadastrar_venda()
                    print('-' * 50)
                    print('Venda cadastrada com sucesso!')
                    break
            else:
                print('-' * 50)
                print('Venda não cadastrada!')


def alterar_vendas():
    msg = ['Data', 'Codigo', 'CPF', 'Quantidade', 'Valor unitario', 'Valor total']
    opcoes = ['data_venda', 'codigo', 'cpf', 'quantidade', 'valor_unitario', 'valor_total']
    id = int(input('Digite o id da venda que deseja alterar: '))
    verificar_id(id)
    if not verificar_id(id):
        print('ID não cadastrado!')
        alterar_vendas()
    else:
        cursor.execute('SELECT * FROM Vendas WHERE id = ?', (id,))
        linha = cursor.fetchone()
        print('-' * 50)
        print(f'ID: {linha[0]} \nData: {linha[1]} \nCodigo: {linha[2]}  \nCliente: {linha[3]} \nQuantidade: {linha[4]} \nValor unitario: {linha[5]} \nValor total da venda: {linha[6]}')
        print('-' * 50)
        op_menu_venda()
        opcao_selecionada = int(input('Digite qual opcao quer alterar? '))

        if opcao_selecionada == 8:
            return

        elif opcao_selecionada == 7:
            while True:
                try:
                    codigo = input('Digite o novo codigo do produto: ')
                    cpf = input('Digite o novo cpf do cliente: ')
                    verificar_codigo(codigo)
                    verificar_cpf_banco(cpf)
                    if not verificar_codigo(codigo):
                        print('Codigo de barras não cadastrado!')
                    elif not verificar_cpf_banco(cpf):
                        print('CPF não cadastrado!')
                    else:
                        data_venda = input('Digite a nova data da venda: ')
                        quantidade = int(input('Digite a nova quantidade do produto: '))
                        valor_unitario = float(input('Digite o novo valor unitario do produto: '))
                        valor_total = float(input('Digite o novo valor total da venda: '))
                        cursor.execute(
                            'UPDATE Vendas SET data_venda = ?, codigo = ?, cpf = ?, quantidade = ?, '
                            'valor_unitario = ?, valor_total = ? WHERE id = ?',
                            (data_venda, codigo, cpf, quantidade, valor_unitario, valor_total, id))
                        conexao.commit()
                        print('-' * 50)
                        print('Venda alterada com sucesso!')
                        break
                except:
                    print('-' * 50)
                    print('Erro ao alterar venda!')

        elif opcao_selecionada == 3:
            while True:
                cpf = input('Digite o novo cpf do cliente: ')
                verificar_cpf_banco(cpf)
                if not verificar_cpf_banco(cpf):
                    print('CPF não cadastrado!')
                else:
                    cursor.execute('UPDATE Vendas SET cpf = ? WHERE id = ?', (cpf, id))
                    conexao.commit()
                    print('-' * 50)
                    print('Cliente alterado com sucesso!')
                    break

        elif opcao_selecionada == 2:
            while True:
                codigo = input('Digite o novo codigo do produto: ')
                verificar_codigo(codigo)
                if not verificar_codigo(codigo):
                    print('Codigo de barras não cadastrado!')
                    print('-' * 50)
                else:
                    cursor.execute('UPDATE Vendas SET codigo = ? WHERE id = ?', (codigo, id))
                    conexao.commit()
                    print('-' * 50)
                    print('Codigo alterado com sucesso!')
                    break

        else:
            novo_valor = input(f'Digite o novo {msg[opcao_selecionada - 1]} da venda: ')
            cursor.execute(f'UPDATE Vendas SET {opcoes[opcao_selecionada - 1]} = ? WHERE id = ?', (novo_valor, id))
            conexao.commit()
            print('-' * 50)
            print('Venda alterada com sucesso!')


def excluir_vendas():
    while True:
        id = int(input('Digite o id da venda que deseja excluir: '))
        verificar_id(id)
        if not verificar_id(id):
            print('ID não cadastrado!')
            print('-' * 50)
        else:
            cursor.execute('SELECT * FROM Vendas WHERE id = ?', (id,))
            linha = cursor.fetchone()
            print('-' * 50)
            print(f'ID: {linha[0]} \nData: {linha[1]} \nCodigo: {linha[2]}  \nCliente: {linha[3]} \nQuantidade: {linha[4]} \nValor unitario: {linha[5]} \nValor total da venda: {linha[6]}')
            print('-' * 50)
            print('Deseja realmente excluir esta venda? (S/N)')
            op = input('>>> ')
            if op.upper() == 'S':
                cursor.execute('DELETE FROM Vendas WHERE id = ?', (id,))
                conexao.commit()
                print('-' * 50)
                print('Venda excluida com sucesso!')
                break
            elif op.upper() == 'N':
                break


def listar_clientes():
    cursor.execute('SELECT * FROM Clientes')
    linhas = cursor.fetchall()
    print('-' * 60)
    print('ID\tNome\t\t\tIdade\t\tCPF\t\t\t\t\tCEP')
    print('-' * 60)
    for linha in linhas:
        print(f'{linha[0]:<3} {linha[1]:<15} {linha[2]:<11} {linha[3]:<19} {linha[4]:<15}')
    print('-' * 60)
    print('Total de clientes: ', len(linhas))
    print('-' * 60)
    print('Pressione ENTER para voltar ao menu principal')
    input()


def listar_vendas():
    cursor.execute('SELECT * FROM Vendas')
    linhas = cursor.fetchall()
    print('-' * 130)
    print('ID\tData\t\tCodigo\t\tCliente\t\t\tQuantidade\t\tValor unitario\tValor total')
    print('-' * 130)
    for linha in linhas:
        print(f'{linha[0]:<3} {linha[1]:<11} {linha[2]:<11} {linha[3]:<15} {linha[4]:<15} {linha[5]:<15} {linha[6]}')
    print('-' * 130)
    print('Total de vendas: ', len(linhas))
    print('-' * 130)
    print('Pressione ENTER para voltar ao menu principal')
    input()


def listar_produtos():
    cursor.execute('SELECT * FROM Produtos')
    linhas = cursor.fetchall()
    print('-' * 60)
    print('ID\tProduto\t\t\tFamilia\t\t\tCodigo')
    print('-' * 60)
    for linha in linhas:
        print(f'{linha[0]:<4}{linha[1]:<15} {linha[2]:<15} {linha[3]:>9}')
    print('-' * 60)
    print('Total de produtos: ', len(linhas))
    print('-' * 60)
    print('Pressione ENTER para voltar ao menu principal')
    input()


def sair():
    print('-' * 100)
    print('Saindo do sistema...')
    print('-' * 100)
    conexao.close()
    exit()


dic = {
        '1': ifo_Cliente, '2': alterar_dados_cliente, '3': excluir_cliente,
        '4': inf_produto, '5': alterar_dados_produto, '6': excluir_produto,
        '7': cadastrar_vendaa, '8': alterar_vendas, '9': excluir_vendas,
        '10': listar_clientes, '11': listar_produtos, '12': listar_vendas, '13': sair
       }

while True:
    escolher()
    opcao = input('Digite a opção desejada: ')
    dic[opcao]()
