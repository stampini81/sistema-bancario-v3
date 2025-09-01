# Sistema Bancário em Python

## Descrição

Projeto desenvolvido por **Leandro da Silva Stampini** para a formação Python DIO. Agora refatorado para utilizar Programação Orientada a Objetos (POO) seguindo o modelo UML, este sistema bancário simula operações essenciais como depósito, saque e extrato, permitindo ao usuário gerenciar contas correntes de forma eficiente e modular.

## Funcionalidades


## Funcionalidades

- Cadastro de clientes (Pessoa Física) com nome, data de nascimento, CPF e endereço
- Cadastro de contas correntes vinculadas a clientes
- Depósito e saque utilizando classes e métodos orientados a objetos
- Limite de valor e quantidade de saques por conta
- Consulta de extrato detalhado por conta
- Histórico de transações (Depósito e Saque) por conta
- Menu interativo para todas as operações

## Especificações Técnicas


## Estrutura de Classes (POO)

- `Cliente`: endereço, contas, métodos para transação e adicionar conta
- `PessoaFisica`: herda de Cliente, adiciona cpf, nome, data_nascimento
- `Conta`: saldo, número, agência, cliente, histórico, métodos para saque, depósito e saldo
- `ContaCorrente`: herda de Conta, adiciona limite e limite_saques
- `Historico`: lista de transações, método para adicionar transação
- `Transacao` (abstrata): método registrar
- `Deposito` e `Saque`: herdam de Transacao, registram operações

## Como Executar


1. Clone o repositório:
    ```sh
    git clone https://github.com/stampini81/sistema-bancario-v3.git
    ```
2. Acesse a pasta do projeto:
    ```sh
    cd sistema-bancario-v3
    ```
3. Execute o sistema bancário:
    ```sh
    python sistema_bancario.py
    ```

## Exemplo de uso


Ao executar o sistema, utilize o menu para cadastrar clientes e contas, realizar depósitos, saques e consultar extratos. Exemplo de dados válidos:

- Nome completo: Leandro da Silva Stampini
- Data de nascimento: 15/08/1990
- CPF: 39053344705
- Endereço: Rua das Flores, 123 - Centro - São Paulo/SP

## Melhorias Futuras


## Melhorias Futuras

- Persistência de dados em arquivo ou banco de dados
- Interface gráfica ou API
- Testes automatizados
- Suporte a múltiplos tipos de contas

---

**Autor:** Leandro da Silva Stampini
