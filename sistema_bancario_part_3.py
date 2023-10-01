# Provides a simple way to format and manipulate text
import textwrap
# Is like a rulebook for creating classes
from abc import ABC, abstractclassmethod, abstractproperty
# Module that helps work with dates and times
from datetime import datetime


class Cliente:
    # It is called when you create a new "Cliente" object
    def __init__(self, endereco):
        self.endereco = endereco  # information about the client
        self.contas = []  # to store accounts associated with this client

    # for executing a transaction on a specific bank account
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)  # to record the transaction

    def adicionar_conta(self, conta):
        self.contas.append(conta)  # add to the "contas" list


class PessoaFisica(Cliente):  # is a subclass of "Cliente" and adds speific attributes
    def __init__(self, nome, data_nascimento, cpf, endereco):
        # it passes the parameter of the "Cliente" class, which sets the client's address
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):  # create a new object with 2 parameters
        # attributes
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod  # it can be called on the class itself
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property  # getter methods allow to access the attributes as if tey were regular variables
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n--- Saque realizado com sucesso! ---")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n--- Depósito realizado com sucesso! ---")
        else:
            print("Operação falhou! Valor de depósito inválido.")
            return False

        return True


class ContaCorrente(Conta):  # Is subclass of "Conta"
    # constructor method, object with 4 parameters
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)  # attributes inherited from the parent class
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        # it calculates the number of withdrawals made by counting transactions in the transaction history
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        # if any of these conditions are met, it prints an error message
        if excedeu_limite:
            print("\n Operação falhou! O valor do saque excede o limite!")
        elif excedeu_saques:
            print("\n Operação falhou! Número máximo de saques excedido.")
        # otherwise, it calls the "sacar" method of the parent class
        else:
            return super().sacar(valor)

    # defines how the object should be represented as a string when using "str()" function or printing the object
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """
    # \t - to create horizontal whitespace


class Historico:
    def __init__(self):  # constructor method
        self._transacoes = []  # an empty list, will be used to store transaction data

    @property  # allows to access the "_transacoes" attribute as if it a regular variable
    # when call "historico.transacoes" it returns the list of transactions
    def transacoes(self):
        return self._transacoes

    # used to add a transaction to the history
    def adicionar_transacao(self, transacao):
        # it creates a dictionary containing information about the transaction
        self._transacoes.append({'tipo': transacao.__class__.__name__,
                                'valor': transacao.valor, 'data': datetime.now().strftime("%d %b %Y, %I:%M%p")})


class Transacao(ABC):  # is an abstract base class
    @property  # is a decorator that makes a method as a property getter
    @abstractproperty  # it must be implemented in concrete subclasses
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):  # it is subclass of "Transacao"
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)  # save transaction


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)  # save transaction


# \t - to create horizontal whitespace
def menu():
    menu = """
    ----- MENU -----
    Escolha uma opção:
    [d]\tDepositar 
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não enontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não enontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não enontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n--- Extrato ---")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("----------------")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    # Verificar se existe cliente com CPF
    if cliente:
        print("\nJá existe usuário com esse CPF!")
        return

    # Cadastrando um novo cliente
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    # Armazenando os clientes em uma lista
    clientes.append(cliente)

    print("\n--- Cliente criado com sucesso! ---")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n--- Conta criada com sucesso! ---")


def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação invalida, por favor selecione novamente a operação desejada.")


main()
