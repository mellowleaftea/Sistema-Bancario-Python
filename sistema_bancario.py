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
        valor = float(input("Digite o valor a ser depositado:  "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Valor de depósito inválido.")

    elif opcao == "s":
        valor = float(input("Digite o valor a ser sacado: "))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

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
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n--- Extrato ---")
        print("Não foram realizados movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("----------------")

    elif opcao == "q":
        print("Saindo do sistema. Obrigado!")
        break

    else:
        print("Operação invalida, por favor selecione novamente a operação desejada.")
