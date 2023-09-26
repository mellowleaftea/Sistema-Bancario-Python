# Separar as funções existentes de saque, depósito e extrato em funções.
# Criar duas novas funções: cadastrar usuário (cliente) e cadastrar conta bancária.
# Saque: deve receber os argumentos apenas por nome (keyword only).
# Sugestão de argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques. Sugestão de retorno: saldo e extrato.
# Depósito: deve receber os argumentos apenas por posição (position only).
# Sugestão de argumentos: saldo, valor, extrato. Sugestão de retorno: saldo e extrato.
# Extrato: deve receber os argumentos por posição e nome (position only e keyword only). Argumentos posicionais: saldo, argumentos nomeados: extrato.

# Novas funções:
# Criar usuário: deve armazenar os usuários em um lista, um usuário é composto por: nome, data de nascimento, cpf e endereço.
# O endereço é uma string com o formato: logradouro, nro - bairro - cidade/sigla estado. Deve ser armazenado somente os números do CPF. Não podemos cadastrar 2 usuários com o mesmo CPF.
# Criar conta corrente: deve armazenar contas em uma lista, uma conta é composta por: agência, número da conta e usuário. O número da conta é sequencial, iniciando em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.

# Provides a simple way to format and manipulate text
import textwrap

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

# Depósito: deve receber os argumentos apenas por posição (position only).
# Sugestão de argumentos: saldo, valor, extrato.
# Sugestão de retorno: saldo e extrato.


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n--- Depósito realizado com sucesso! ---")
    else:
        print("Valor de depósito inválido.")

    return saldo, extrato

# Saque: deve receber os argumentos apenas por nome (keyword only).
# Sugestão de argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques.
# Sugestão de retorno: saldo e extrato.


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n--- Saque realizado com sucesso! ---")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato


# Extrato: deve receber os argumentos por posição e nome (position only e keyword only).
# Argumentos posicionais: saldo.
# Argumentos nomeados: extrato.
def exibir_extrato(saldo, /, *, extrato):
    print("\n--- Extrato ---")
    print("Não foram realizados movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("----------------")


# Criar usuário: deve armazenar os usuários em um lista, um usuário é composto por: nome, data de nascimento, cpf e endereço.
# Deve ser armazenado somente os números do CPF.
# Não podemos cadastrar 2 usuários com o mesmo CPF.
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)  # "filtrar_usuario" next function

    # Verificar se existe usuário com CPF
    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    # Cadastrando um novo usuario
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Armazenando os usuários em uma lista
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                    "cpf": cpf, "endereco": endereco})

    print("--- Usuário criado com sucesso! ---")

# Verificar se existe usuário com CPF


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Criar conta corrente: deve armazenar contas em uma lista.
# Conta é composta por: agência, número da conta e usuário.
# O número da conta é sequencial, iniciando em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n--- Conta criada com sucesso! ---")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta["agencia"]}
            C/C:\t{conta["numero_conta"]}
            Titular:\t{conta["usuario"]["nome"]}
            """
        print("="*100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor a ser depositado:  "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Digite o valor a ser sacado: "))
            saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite,
                                   numero_saques=numero_saques, limite_saques=LIMITE_SAQUES,)

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação invalida, por favor selecione novamente a operação desejada.")


main()
