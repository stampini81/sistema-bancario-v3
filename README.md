# Sistema Bancário em Python

## Descrição

Projeto desenvolvido por **Leandro da Silva Stampini** para a formação Python DIO. Este sistema bancário simula operações essenciais como depósito, saque e extrato, permitindo ao usuário gerenciar uma conta corrente de forma simples e eficiente.

## Funcionalidades

- Cadastro de usuários com validação de nome, data de nascimento, CPF (formato e dígitos verificadores) e endereço
- Cadastro de contas bancárias vinculadas a usuários
- Depósito em conta (função positional-only)
- Saque com limite diário e por operação (função keyword-only)
- Consulta de extrato detalhado (função positional e keyword-only)
- Validação de todas as operações (saldo, limites, valores, formatos)
- Mensagens de erro detalhadas para cada campo inválido
- Menu interativo para todas as operações

## Especificações Técnicas

- Todas as operações principais são implementadas como funções específicas e reutilizáveis
- Funções seguem regras de passagem de argumentos (positional-only, keyword-only)
- Validações robustas para CPF, data, endereço e duplicidade de usuário
- Código modular e fácil de manter

## Como Executar

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    ```
2. Acesse a pasta do projeto:
    ```sh
    cd sistema-bancario-v2/00 - Fundamentos
    ```
3. Execute o sistema bancário:
    ```sh
    python desafio.py
    ```

## Exemplo de uso

Ao executar o sistema, utilize o menu para cadastrar usuários e contas, realizar depósitos, saques e consultar extratos. Exemplo de dados válidos:

- Nome completo: Leandro da Silva Stampini
- Data de nascimento: 15/08/1990
- CPF: 390.533.447-05
- Endereço: Rua das Flores, 123 - Centro - São Paulo/SP

## Melhorias Futuras

- Persistência de dados em arquivo ou banco de dados
- Interface gráfica ou API
- Testes automatizados
- Suporte a múltiplos tipos de contas

---

**Autor:** Leandro da Silva Stampini
