# Sistema de Controle de Estoque

Este projeto é uma API para controle de estoque, permitindo realizar operações de entrada, saída, devolução, extrato e resumo. O objetivo é fornecer um sistema simples para gerenciamento de produtos e movimentações.

## 🚀 Como executar a aplicação
Clone o repositório, entre na pasta do projeto, crie e ative um ambiente virtual (opcional), instale as dependências e execute a aplicação com:
uvicorn app.main:app --reload
A API ficará disponível em: http://127.0.0.1:8000

## 📌 Rotas disponíveis

### ➕ Entrada de estoque
POST /estoque/entrada
Exemplo de corpo da requisição:
{ "produto_id": 1, "quantidade": 10 }

### ➖ Saída de estoque (venda)
POST /estoque/saida
Exemplo:
{ "produto_id": 1, "quantidade": 5 }

### 🔄 Devolução
POST /estoque/devolucao
Exemplo:
{ "produto_id": 1, "quantidade": 2 }

### 📜 Extrato de movimentações
GET /estoque/extrato/{produto_id}
Exemplo de resposta:
[ { "tipo": "entrada", "quantidade": 10, "data": "2025-10-06T10:00:00" }, { "tipo": "saida", "quantidade": 5, "data": "2025-10-06T11:00:00" }, { "tipo": "devolucao", "quantidade": 2, "data": "2025-10-06T12:00:00" } ]

### 📊 Resumo do estoque
GET /estoque/resumo
Exemplo de resposta:
[ { "produto_id": 1, "quantidade": 7 }, { "produto_id": 2, "quantidade": 15 } ]

## ⚖️ Decisão sobre saldo negativo
Neste sistema, o saldo NÃO permite valores negativos. Se o usuário tentar realizar uma saída maior do que o estoque disponível, a operação será bloqueada e a API retornará um erro.
Exemplo de erro:
{ "detail": "Estoque insuficiente para realizar a operação." }

## 🛠 Tecnologias utilizadas
- Python 3.10+
- FastAPI
- Uvicorn


