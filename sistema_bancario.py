# O sistema deve permitir realizar 3 saques diários com limite máximo de R$ 500 por saque. Caso o usuário não tenha saldo em conta, o sistema deve exibir uma mensagem informando que não será possível sacar o dinheiro por falta de saldo. Todos os saques devem ser armazenados em uma variável e exibidos na operação de extrato.

# Operação de extrato
# Essa operação deve listar todos os depósitos e saques realizados na conta. No fim da lisragem deve ser exibido o saldo atual da conta.
# Os valores devem ser exibidos utilizando o formato R$ xxx.xx

menu = """
Escolha uma opção:
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
"""
saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d":
        print("Deposito")
        valor = float(input("Digite o valor a ser depositado:  "))
        if valor > 0:
            saldo += valor
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso")
        else:
            print("Valor de depósito inválido.")

    elif opcao == "s":
        print("Saque")
        valor = float(input("Digite o valor a ser sacado: "))
        if LIMITE_SAQUES > 0 and valor <= limite:
            if saldo >= valor:
                saldo -= valor
                extrato.append(valor)
                LIMITE_SAQUES -= 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso")
            else:
                print("Saldo insuficiente para o saque.")
        elif LIMITE_SAQUES == 0:
            print("Limite diário de saques atingido.")
        else:
            print("Valor de saque inválido.")

    elif opcao == "e":
        print("--- Extrato ---")
        for saque in extrato:
            print(f"Saque de R$ {saque:.2f}")
        print(f"Saldo atual: R$ {saldo:.2f}")

    elif opcao == "q":
        print("Saindo do sistema. Obrigado!")
        break

    else:
        print("Operação invalida, por favor selecione novamente a operação desejada.")
