"""Sistema Bancário POO - Menu interativo

Refatorado para:
 - Criar conta automaticamente ao cadastrar usuário (opção 'u')
 - Opção 'c' apenas lista contas existentes
 - Validações de nome, data, CPF (formato ou 11 dígitos) e endereço
 - Operações: depósito, saque, extrato
"""

from poo_banco import PessoaFisica, ContaCorrente, Deposito, Saque
from datetime import datetime
import re

clientes = []  # PessoaFisica
contas = []    # ContaCorrente
AGENCIA_PADRAO = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500.0

def limpar_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)

def formatar_cpf(cpf_digitos: str) -> str:
    return f"{cpf_digitos[:3]}.{cpf_digitos[3:6]}.{cpf_digitos[6:9]}-{cpf_digitos[9:]}"

def encontrar_cliente_por_cpf(cpf: str):
    cpf_num = limpar_cpf(cpf)
    return next((c for c in clientes if c.cpf == cpf_num), None)

def validar_nome(nome: str) -> bool:
    nome = nome.strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return False
    partes = [p for p in nome.split() if p]
    if len(partes) < 2:
        print("Informe nome completo (mínimo 2 palavras).")
        return False
    if any(not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", p) for p in partes):
        print("Nome contém partes inválidas.")
        return False
    return True

def validar_data(data_str: str) -> bool:
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", data_str):
        print("Data deve estar no formato dd/mm/aaaa.")
        return False
    try:
        dt = datetime.strptime(data_str, "%d/%m/%Y")
        ano_atual = datetime.now().year
        if dt.year < 1900 or dt.year > ano_atual:
            print("Ano fora do intervalo válido (1900..ano atual).")
            return False
        return True
    except ValueError:
        print("Data inválida (dia ou mês inexistente).")
        return False

def validar_cpf(cpf: str):
    if re.fullmatch(r"\d{11}", cpf):
        numeros = cpf
    elif re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        numeros = limpar_cpf(cpf)
    else:
        print("CPF deve estar no formato xxx.xxx.xxx-xx ou 11 dígitos.")
        return None
    if numeros == numeros[0] * 11:
        print("CPF inválido (todos dígitos iguais).")
        return None
    def calc(seq, start):
        soma = 0
        fator = start
        for d in seq:
            soma += int(d) * fator
            fator -= 1
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto
    d1 = calc(numeros[:9], 10)
    d2 = calc(numeros[:9] + str(d1), 11)
    if numeros[-2:] != f"{d1}{d2}":
        print("CPF inválido (dígitos verificadores incorretos).")
        return None
    return numeros

def validar_endereco(endereco: str) -> bool:
    end = endereco.strip()
    if len(end) < 12:
        print("Endereço muito curto.")
        return False
    padrao = r"^.+?,\s*\d+\s*-\s*.+?\s*-\s*.+?/[A-Za-z]{2}$"
    if not re.fullmatch(padrao, end):
        print("Use o formato: Rua X, 123 - Bairro - Cidade/UF")
        return False
    return True

def menu_principal():
    print("""
    [u] Usuário (cadastra e cria conta automática)
    [c] Contas (listar)
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    """)
    return input("=> ").lower().strip()

def parse_valor_positivo(texto: str):
    """Converte string em float positivo validando formato (apenas dígitos e opcional , ou . para centavos).
    Formatos aceitos: 100 | 100.5 | 100.50 | 100,5 | 100,50
    Rejeita sinais (+/-), múltiplas vírgulas/pontos ou outros caracteres.
    Retorna float ou None.
    """
    texto = texto.strip()
    padrao = r'^\d+(?:[.,]\d{1,2})?$'
    if not re.fullmatch(padrao, texto):
        return None
    valor = float(texto.replace(',', '.'))
    if valor <= 0:
        return None
    return valor

def main():
    while True:
        opcao = menu_principal()
        if opcao == 'u':
            print("Cadastro de Usuário (Pessoa Física)")
            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            cpf_input = input("CPF (xxx.xxx.xxx-xx ou 11 dígitos): ")
            endereco = input("Endereço (Logradouro, número - Bairro - Cidade/UF): ")
            if not (validar_nome(nome) and validar_data(data_nascimento)):
                continue
            cpf_digitos = validar_cpf(cpf_input)
            if not cpf_digitos:
                continue
            if not validar_endereco(endereco):
                continue
            if encontrar_cliente_por_cpf(cpf_digitos):
                print("CPF já cadastrado!")
                continue
            cliente = PessoaFisica(cpf_digitos, nome.strip(), data_nascimento, endereco.strip())
            clientes.append(cliente)
            numero_conta = len(contas) + 1
            conta = ContaCorrente(numero_conta, AGENCIA_PADRAO, cliente, limite=LIMITE_VALOR_SAQUE, limite_saques=LIMITE_SAQUES)
            contas.append(conta)
            cliente.adicionar_conta(conta)
            print(f"Usuário e conta #{numero_conta} criados com sucesso!")
        elif opcao == 'c':
            print("\n--- CONTAS CADASTRADAS ---")
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                for conta in contas:
                    print(f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.cliente.nome} | CPF: {formatar_cpf(conta.cliente.cpf)}")
            print("--------------------------\n")
        elif opcao == 'd':
            cpf_raw = input("CPF do titular (11 dígitos ou formato): ")
            cliente = encontrar_cliente_por_cpf(cpf_raw)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada!")
                continue
            conta = cliente.contas[-1]
            bruto = input("Valor do depósito: ")
            valor = parse_valor_positivo(bruto)
            if valor is None:
                print("Valor inválido! Use apenas números (ex: 100 ou 100,50).")
                continue
            if cliente.realizar_transacao(conta, Deposito(valor)):
                print("Depósito realizado com sucesso!")
            else:
                print("Depósito não efetuado!")
        elif opcao == 's':
            cpf_raw = input("CPF do titular (11 dígitos ou formato): ")
            cliente = encontrar_cliente_por_cpf(cpf_raw)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada!")
                continue
            conta = cliente.contas[-1]
            bruto = input("Valor do saque: ")
            valor = parse_valor_positivo(bruto)
            if valor is None:
                print("Valor inválido! Use apenas números (ex: 100 ou 100,50).")
                continue
            if cliente.realizar_transacao(conta, Saque(valor)):
                print("Saque realizado com sucesso!")
            else:
                print("Saque não realizado! Verifique saldo/limites.")
        elif opcao == 'e':
            cpf_raw = input("CPF do titular (11 dígitos ou formato): ")
            cliente = encontrar_cliente_por_cpf(cpf_raw)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada!")
                continue
            conta = cliente.contas[-1]
            print("\n===== EXTRATO =====")
            if not conta.historico.transacoes:
                print("Não há movimentações.")
            else:
                for t in conta.historico.transacoes:
                    print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
            print(f"Saldo: R$ {conta.saldo:.2f}")
            print("===================\n")
        elif opcao == 'q':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    main()
