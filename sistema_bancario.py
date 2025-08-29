"""
Sistema Bancário Modular
Refatorado para usar funções com regras específicas de argumentos
"""

# Listas para armazenar usuários e contas
usuarios = []
contas = []

# Constantes
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500
AGENCIA_PADRAO = "0001"

def criar_usuario(*, nome: str, data_nascimento: str, cpf: str, endereco: str) -> dict:
    """
    Cria um novo usuário.
    Argumentos keyword-only.
    CPF deve conter apenas números e ser único.
    """
    # Remove caracteres não numéricos do CPF
    cpf_numerico = ''.join(filter(str.isdigit, cpf))

    # Verifica se CPF já existe
    for usuario in usuarios:
        if usuario['cpf'] == cpf_numerico:
            print("CPF já cadastrado!")
            return None

    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf_numerico,
        'endereco': endereco
    }

    usuarios.append(usuario)
    print("Usuário criado com sucesso!")
    return usuario

def criar_conta(*, cpf: str) -> dict:
    """
    Cria uma nova conta bancária vinculada a um usuário.
    Argumentos keyword-only.
    """
    # Busca usuário pelo CPF
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            usuario_encontrado = usuario
            break

    if not usuario_encontrado:
        print("Usuário não encontrado!")
        return None

    # Gera número da conta sequencial
    numero_conta = len(contas) + 1

    conta = {
        'agencia': AGENCIA_PADRAO,
        'numero_conta': numero_conta,
        'usuario': usuario_encontrado
    }

    contas.append(conta)
    print(f"Conta {numero_conta} criada com sucesso!")
    return conta

def depositar(saldo: float, valor: float, extrato: list, /) -> tuple:
    """
    Realiza depósito na conta.
    Argumentos positional-only.
    Retorna novo saldo e extrato atualizado.
    """
    if valor <= 0:
        print("Valor inválido!")
        return saldo, extrato

    novo_saldo = saldo + valor
    extrato.append(f"Depósito: R$ {valor:.2f}")

    print("Depósito realizado com sucesso!")
    return novo_saldo, extrato

def sacar(*, saldo: float, valor: float, extrato: list, limite: float, numero_saques: int, limite_saques: int) -> tuple:
    """
    Realiza saque da conta.
    Argumentos keyword-only.
    Retorna novo saldo e extrato atualizado.
    """
    if valor <= 0:
        print("Valor inválido!")
        return saldo, extrato

    if valor > saldo:
        print("Saldo insuficiente!")
        return saldo, extrato

    if valor > limite:
        print("Valor excede o limite por saque!")
        return saldo, extrato

    if numero_saques >= limite_saques:
        print("Limite de saques diários atingido!")
        return saldo, extrato

    novo_saldo = saldo - valor
    extrato.append(f"Saque: R$ {valor:.2f}")

    print("Saque realizado com sucesso!")
    return novo_saldo, extrato

def exibir_extrato(saldo: float, /, *, extrato: list) -> None:
    """
    Exibe o extrato da conta.
    saldo: positional-only
    extrato: keyword-only
    """
    print("\n===== EXTRATO =====")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in extrato:
            print(movimento)
    print(f"Saldo: R$ {saldo:.2f}")
    print("===================\n")

def menu_principal():
    """Exibe o menu principal e retorna a opção escolhida."""
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
    """Função principal do sistema bancário."""
    # Dados de exemplo para teste (pode ser removido)
    saldo_atual = 0.0
    extrato_atual = []
    saques_realizados = 0

    while True:
        opcao = menu_principal()

        if opcao == "u":
            # Criar usuário
            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            cpf = input("CPF (apenas números): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            criar_usuario(
                nome=nome,
                data_nascimento=data_nascimento,
                cpf=cpf,
                endereco=endereco
            )

        elif opcao == "c":
            # Criar conta
            cpf = input("CPF do usuário (apenas números): ")
            criar_conta(cpf=cpf)

        elif opcao == "d":
            # Depositar
            try:
                valor = float(input("Valor do depósito: ").replace(',', '.'))
                saldo_atual, extrato_atual = depositar(saldo_atual, valor, extrato_atual)
            except ValueError:
                print("Valor inválido!")

        elif opcao == "s":
            # Sacar
            try:
                valor = float(input("Valor do saque: ").replace(',', '.'))
                saldo_atual, extrato_atual = sacar(
                    saldo=saldo_atual,
                    valor=valor,
                    extrato=extrato_atual,
                    limite=LIMITE_VALOR_SAQUE,
                    numero_saques=saques_realizados,
                    limite_saques=LIMITE_SAQUES
                )
                if saldo_atual < 0:  # Se saque foi realizado, incrementa contador
                    saques_realizados += 1
            except ValueError:
                print("Valor inválido!")

        elif opcao == "e":
            # Extrato
            exibir_extrato(saldo_atual, extrato=extrato_atual)

        elif opcao == "l":
            # Listar contas
            print("\n--- CONTAS CADASTRADAS ---")
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                for conta in contas:
                    usuario = conta['usuario']
                    print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {usuario['nome']} | CPF: {usuario['cpf']}")
            print("--------------------------\n")

        elif opcao == "q":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
