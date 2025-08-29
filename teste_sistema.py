"""
Teste das funções do sistema bancário
"""

from sistema_bancario import *

def testar_criar_usuario():
    print("=== Teste: Criar Usuário ===")
    usuario = criar_usuario(
        nome="João Silva",
        data_nascimento="01/01/1990",
        cpf="12345678901",
        endereco="Rua A, 123 - Centro - São Paulo/SP"
    )
    print(f"Usuário criado: {usuario}")
    print()

def testar_criar_conta():
    print("=== Teste: Criar Conta ===")
    conta = criar_conta(cpf="12345678901")
    print(f"Conta criada: {conta}")
    print()

def testar_depositar():
    print("=== Teste: Depositar ===")
    saldo = 100.0
    extrato = ["Depósito inicial: R$ 100.00"]
    novo_saldo, novo_extrato = depositar(saldo, 50.0, extrato)
    print(f"Saldo anterior: {saldo}")
    print(f"Novo saldo: {novo_saldo}")
    print(f"Extrato: {novo_extrato}")
    print()

def testar_sacar():
    print("=== Teste: Sacar ===")
    saldo = 200.0
    extrato = ["Depósito: R$ 200.00"]
    novo_saldo, novo_extrato = sacar(
        saldo=saldo,
        valor=50.0,
        extrato=extrato,
        limite=500.0,
        numero_saques=0,
        limite_saques=3
    )
    print(f"Saldo anterior: {saldo}")
    print(f"Novo saldo: {novo_saldo}")
    print(f"Extrato: {novo_extrato}")
    print()

def testar_exibir_extrato():
    print("=== Teste: Exibir Extrato ===")
    saldo = 150.0
    extrato = ["Depósito: R$ 200.00", "Saque: R$ 50.00"]
    exibir_extrato(saldo, extrato=extrato)

if __name__ == "__main__":
    testar_criar_usuario()
    testar_criar_conta()
    testar_depositar()
    testar_sacar()
    testar_exibir_extrato()
