# Sistema Bancário em Python (POO)

## Descrição

Projeto desenvolvido por **Leandro da Silva Stampini** para a formação Python DIO. Refatorado para **Programação Orientada a Objetos** seguindo um modelo de classes (UML) que separa responsabilidades entre Cliente, Conta, Transação e Histórico. O sistema simula operações bancárias essenciais de forma modular e extensível.

## Funcionalidades Principais

- Cadastro de cliente (Pessoa Física) com validação de: Nome completo, Data de nascimento, CPF e Endereço
- Criação automática da conta corrente ao cadastrar o cliente (não existe mais opção de "criar conta" separada)
- Listagem de todas as contas cadastradas (opção `c`)
- Depósito e Saque via classes de transação (`Deposito`, `Saque`)
- Limite de valor por saque e limite diário de quantidade de saques
- Extrato detalhado com histórico cronológico das operações
- Histórico armazena tipo, valor e timestamp de cada transação
- Menu interativo simples em loop

## Validações Implementadas

- Nome: mínimo 2 palavras, apenas letras (acentos permitidos)
- Data de nascimento: formato `dd/mm/aaaa`, intervalo de ano válido (>=1900 e <= ano atual)
- CPF: aceita formato `xxx.xxx.xxx-xx` ou somente 11 dígitos; cálculo dos dígitos verificadores; rejeita sequência repetida
- Endereço: formato `Logradouro, número - Bairro - Cidade/UF`
- Valores monetários: apenas números positivos (inteiro ou com 1-2 casas decimais) sem sinal; rejeita `+100`, `-50`, letras ou múltiplos separadores

## Menu Atual

```
[u] Usuário (cadastra e cria conta automática)
[c] Contas (listar)
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
```

## Estrutura de Classes

- `Cliente` – mantém endereço e lista de contas; executa transações
- `PessoaFisica(Cliente)` – acrescenta `cpf`, `nome`, `data_nascimento`
- `Conta` – saldo, número, agência, histórico e operações básicas
- `ContaCorrente(Conta)` – inclui limites de valor e quantidade de saques
- `Historico` – registra transações (`tipo`, `valor`, `data`)
- `Transacao` (abstrata) – interface para registrar (Template Method)
- `Deposito` / `Saque` – implementações concretas de transações

## Como Executar

1. Clonar o repositório:
    ```sh
    git clone https://github.com/stampini81/sistema-bancario-v3.git
    cd sistema-bancario-v3
    python sistema_bancario.py
    ```

## Exemplo de Uso

Durante a execução:
1. Use `u` para cadastrar um cliente (gera conta imediatamente).
2. Use `d` e informe CPF (11 dígitos ou formatado) e o valor (ex: `100`, `250,50`).
3. Use `s` para sacar respeitando limites.
4. Use `e` para ver o extrato e saldo.

Exemplo de entrada válida:
- Nome: Maria Souza Lima
- Data: 10/04/1988
- CPF: 39053344705
- Endereço: Rua das Flores, 123 - Centro - São Paulo/SP

## Melhorias Futuras

- Persistência (arquivo, SQLite ou ORM)
- API (Flask / FastAPI) ou interface web
- Testes automatizados (pytest) cobrindo regras de negócio
- Suporte a múltiplos tipos de contas (poupança, investimento)
- Tratamento de internacionalização / moeda

## Changelog Resumido da Refatoração

- Migração do modelo procedural para POO completa
- Implementação de classes: Cliente, PessoaFisica, Conta, ContaCorrente, Historico, Transacao, Deposito, Saque
- Criação automática de conta ao cadastrar usuário
- Novas validações robustas para CPF, data, nome e endereço
- Padronização de entrada de valores (rejeitando sinais e formatos inválidos)
- Limites de saque aplicados (quantidade e valor)
- Extrato com histórico temporal
- Limpeza de código duplicado e correção de inconsistências

---
**Autor:** Leandro da Silva Stampini
