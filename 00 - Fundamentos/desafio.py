# Sistema Bancário Modular
import re
import datetime

# Listas para armazenar usuários e contas
usuarios = []
contas = []
transacoes = {}

# Constantes
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500
AGENCIA_PADRAO = "0001"

def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF tem formato válido e dígitos verificadores corretos"""
    # Remove caracteres não numéricos
    cpf_numerico = ''.join(filter(str.isdigit, cpf))

    # Deve ter exatamente 11 dígitos
    if len(cpf_numerico) != 11:
        return False

    # Verifica se todos os dígitos são iguais (CPFs inválidos como 111.111.111-11)
    if cpf_numerico == cpf_numerico[0] * 11:
        return False

    # Converte para lista de inteiros
    cpf_digitos = list(map(int, cpf_numerico))

    # Calcula primeiro dígito verificador
    soma = sum(cpf_digitos[i] * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito1 = 0 if resto == 10 else resto

    # Verifica primeiro dígito
    if digito1 != cpf_digitos[9]:
        return False

    # Calcula segundo dígito verificador
    soma = sum(cpf_digitos[i] * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito2 = 0 if resto == 10 else resto

    # Verifica segundo dígito
    if digito2 != cpf_digitos[10]:
        return False

    return True

def validar_data(data: str) -> bool:
    """Valida se a data tem formato dd/mm/aaaa e é uma data válida"""
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
        return False

    try:
        dia, mes, ano = map(int, data.split('/'))

        # Validações básicas
        if mes < 1 or mes > 12:
            return False
        if dia < 1 or dia > 31:
            return False
        if ano < 1900 or ano > datetime.datetime.now().year:
            return False

        # Validação específica por mês
        dias_por_mes = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if dia > dias_por_mes[mes - 1]:
            return False

        # Validação de ano bissexto para fevereiro
        if mes == 2 and dia == 29:
            if not (ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)):
                return False

        # Cria a data para validação final
        datetime.datetime(ano, mes, dia)
        return True
    except ValueError:
        return False

def validar_endereco(endereco: str) -> bool:
    """Valida se o endereço segue o formato: logradouro, nro - bairro - cidade/sigla estado"""
    # Formato esperado: "Rua das Flores, 123 - Centro - São Paulo/SP"
    padrao = r'^[^,]+,\s*\d+\s*-\s*[^-]+-\s*[^/]+/[A-Z]{2}$'
    return bool(re.match(padrao, endereco.strip()))

def encontrar_usuario(cpf):
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    for usuario in usuarios:
        if usuario['cpf'] == cpf_numerico:
            return usuario
    return None

def criar_usuario(*, nome: str, data_nascimento: str, cpf: str, endereco: str) -> dict:
    """
    Cria um novo usuário.
    Argumentos keyword-only.
    CPF deve conter apenas números e ser único.
    """
    erros = []
    if not nome.strip():
        erros.append("Nome não pode estar vazio!")
    if not validar_data(data_nascimento):
        erros.append("Data de nascimento inválida! Use o formato dd/mm/aaaa.")
    if not validar_cpf(cpf):
        erros.append("CPF inválido! Verifique se os dígitos estão corretos.")
    if not validar_endereco(endereco):
        erros.append("Endereço inválido! Use o formato: logradouro, nro - bairro - cidade/sigla estado")
    # Remove caracteres não numéricos do CPF
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    if encontrar_usuario(cpf_numerico):
        erros.append("CPF já cadastrado!")
    if erros:
        print("\nErros de validação:")
        for erro in erros:
            print("-", erro)
        return None
    usuario = {
        'nome': nome.strip(),
        'data_nascimento': data_nascimento,
        'cpf': cpf_numerico,
        'endereco': endereco.strip()
    }
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")
    return usuario

def criar_conta(*, cpf: str) -> dict:
    """
    Cria uma nova conta bancária vinculada a um usuário.
    Argumentos keyword-only.
    """
    # Busca usuário pelo CPF numérico
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    usuario = encontrar_usuario(cpf_numerico)
    if not usuario:
        print("Usuário não encontrado!")
        return None

    # Gera número da conta sequencial
    numero_conta = len(contas) + 1

    conta = {
        'agencia': "0001",
        'numero_conta': numero_conta,
        'usuario': usuario
    }

    contas.append(conta)
    # Inicializa dados da conta para transações
    if numero_conta not in transacoes:
        transacoes[numero_conta] = {"saldo": 0, "extrato": [], "saques": 0}

    print(f"Conta {numero_conta} criada para {usuario['nome']}.")
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

def depositar_conta():
    """Função auxiliar para depósito em conta específica"""
    numero_str = input("Número da conta: ")
    if not numero_str.isdigit():
        print("Número da conta inválido! Digite apenas números.")
        return
    numero = int(numero_str)

    if numero not in transacoes:
        print("Conta não encontrada!")
        return

    valor_str = input("Valor do depósito: ").replace(',', '.')
    # Nova validação: não aceita sinais ou espaços
    if not re.match(r'^\d+(\.\d{1,2})?$', valor_str.strip()):
        print("Valor inválido! Digite apenas números positivos.")
        return
    try:
        valor = float(valor_str)
    except ValueError:
        print("Valor inválido! Use apenas números.")
        return
    if valor <= 0:
        print("Valor inválido!")
        return
    saldo_atual = transacoes[numero]["saldo"]
    extrato_atual = transacoes[numero]["extrato"]
    novo_saldo, novo_extrato = depositar(saldo_atual, valor, extrato_atual)
    transacoes[numero]["saldo"] = novo_saldo
    transacoes[numero]["extrato"] = novo_extrato

def sacar_conta():
    """Função auxiliar para saque em conta específica"""
    numero_str = input("Número da conta: ")
    if not numero_str.isdigit():
        print("Número da conta inválido! Digite apenas números.")
        return
    numero = int(numero_str)

    if numero not in transacoes:
        print("Conta não encontrada!")
        return

    valor_str = input("Valor do saque: ").replace(',', '.')
    try:
        valor = float(valor_str)
    except ValueError:
        print("Valor inválido! Use apenas números.")
        return

    saldo_atual = transacoes[numero]["saldo"]
    extrato_atual = transacoes[numero]["extrato"]
    saques_atual = transacoes[numero]["saques"]

    novo_saldo, novo_extrato = sacar(
        saldo=saldo_atual,
        valor=float(valor_str),
        extrato=extrato_atual,
        limite=LIMITE_VALOR_SAQUE,
        numero_saques=saques_atual,
        limite_saques=LIMITE_SAQUES
    )

    if novo_saldo != saldo_atual:  # Se saque foi realizado
        transacoes[numero]["saques"] += 1

    transacoes[numero]["saldo"] = novo_saldo
    transacoes[numero]["extrato"] = novo_extrato

def exibir_extrato_conta():
    """Função auxiliar para exibir extrato de conta específica"""
    numero_str = input("Número da conta: ")
    if not numero_str.isdigit():
        print("Número da conta inválido! Digite apenas números.")
        return
    numero = int(numero_str)

    if numero not in transacoes:
        print("Conta não encontrada!")
        return

    saldo_atual = transacoes[numero]["saldo"]
    extrato_atual = transacoes[numero]["extrato"]

    exibir_extrato(saldo_atual, extrato=extrato_atual)

def listar_contas():
    print("\n--- CONTAS CADASTRADAS ---")
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            usuario = conta['usuario']
            print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {usuario['nome']} | CPF: {usuario['cpf']}")
    print("--------------------------\n")

def menu_principal():
    print("""
    [u] Usuário
    [c] Contas
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
            # Criar usuário com inputs
            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            cpf = input("CPF (formato xxx.xxx.xxx-xx ou apenas números): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            criar_usuario(
                nome=nome,
                data_nascimento=data_nascimento,
                cpf=cpf,
                endereco=endereco
            )
        elif opcao == "c":
            # Criar conta
            cpf = input("CPF do usuário (formato xxx.xxx.xxx-xx ou apenas números): ")
            criar_conta(cpf=cpf)
        elif opcao == "d":
            depositar_conta()
        elif opcao == "s":
            sacar_conta()
        elif opcao == "e":
            exibir_extrato_conta()
        elif opcao == "l":
            listar_contas()
        elif opcao == "q":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

