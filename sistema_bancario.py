"""
Sistema Bancário Modular
Refatorado para usar funções com regras específicas de argumentos
"""


# Sistema Bancário com POO
from poo_banco import PessoaFisica, ContaCorrente, Deposito, Saque

clientes = []
contas = []
AGENCIA_PADRAO = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500.0

def encontrar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def menu_principal():
    print("""
    [u] Criar Usuário
    [c] Criar Conta
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [l] Listar Contas
    [q] Sair
    """)
    return input("=> ").lower()

def main():
    while True:
        opcao = menu_principal()

        if opcao == "u":
            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            cpf = input("CPF (apenas números): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            if encontrar_cliente_por_cpf(cpf):
                print("CPF já cadastrado!")
            else:
                cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
                clientes.append(cliente)
                print("Usuário criado com sucesso!")

        elif opcao == "c":
            cpf = input("CPF do usuário (apenas números): ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if not cliente:
                print("Usuário não encontrado!")
            else:
                numero_conta = len(contas) + 1
                conta = ContaCorrente(numero_conta, AGENCIA_PADRAO, cliente, limite=LIMITE_VALOR_SAQUE, limite_saques=LIMITE_SAQUES)
                contas.append(conta)
                cliente.adicionar_conta(conta)
                print(f"Conta {numero_conta} criada com sucesso!")

        elif opcao == "d":
            cpf = input("CPF do titular da conta: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada!")
                continue
            conta = cliente.contas[-1]
            try:
                valor = float(input("Valor do depósito: ").replace(',', '.'))
                transacao = Deposito(valor)
                if cliente.realizar_transacao(conta, transacao):
                    print("Depósito realizado com sucesso!")
                else:
                    print("Valor inválido!")
            except ValueError:
                print("Valor inválido!")

        elif opcao == "s":
            cpf = input("CPF do titular da conta: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada!")
                continue
            conta = cliente.contas[-1]
            try:
                valor = float(input("Valor do saque: ").replace(',', '.'))
                transacao = Saque(valor)
                if cliente.realizar_transacao(conta, transacao):
                    print("Saque realizado com sucesso!")
                else:
                    print("Saque não realizado! Verifique saldo, limite ou número de saques.")
            except ValueError:
                print("Valor inválido!")

        elif opcao == "e":
            cpf = input("CPF do titular da conta: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada!")
                continue
            conta = cliente.contas[-1]
            print("\n===== EXTRATO =====")
            for t in conta.historico.transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
            print(f"Saldo: R$ {conta.saldo:.2f}")
            print("===================\n")

        elif opcao == "l":
            print("\n--- CONTAS CADASTRADAS ---")
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                for conta in contas:
                    print(f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.cliente.nome} | CPF: {conta.cliente.cpf}")
            print("--------------------------\n")

        elif opcao == "q":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
