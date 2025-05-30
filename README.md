
# 🛒 Sistema de Gerenciamento de Vendas

## 📌 Descrição

Este é um **Sistema de Gerenciamento de Vendas** desenvolvido com **Django**, utilizando **HTML/CSS** no frontend e **PostgreSQL** como banco de dados (via conexão ODBC). O sistema permite o cadastro de clientes, produtos, fornecedores e pedidos, com funcionalidade para finalizar compras e registrar pagamentos.

## 🚀 Funcionalidades

- ✅ Cadastro de clientes
- ✅ Cadastro de produtos e fornecedores
- ✅ Criação e gerenciamento de pedidos
- ✅ Adicionar múltiplos produtos a um pedido
- ✅ Exibição dos itens do pedido em tela
- ✅ Finalização do pedido com redirecionamento para pagamento
- ✅ Registro do método de pagamento, valor total e status
- ✅ Integração com banco de dados PostgreSQL via ODBC

## 🧱 Tecnologias Utilizadas

| Tecnologia      | Descrição                                |
|----------------|-------------------------------------------|
| Django          | Framework backend em Python              |
| HTML/CSS        | Interface do usuário                     |
| PostgreSQL      | Banco de dados relacional                |
| pyodbc          | Driver para conexão com o PostgreSQL via ODBC |

## 🖥️ Estrutura do Projeto

```
sistema-vendas/
│
├── manage.py
├── requirements.txt
├── db_config/
│   └── settings.py  # Configuração do banco de dados via ODBC
│
├── vendas/
│   ├── models.py       # Modelos: Cliente, Produto, Pedido, Fornecedor, Pagamento
│   ├── views.py        # Lógica de negócio e visualizações
│   ├── urls.py         # Rotas do app
│   ├── templates/
│   │   └── Arquivos HTML (cadastro, pedido, pagamento, etc.)
│   └── static/
│       └── css/
│           └── styles.css
│
└── main_project/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 🛠️ Como Executar Localmente

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/seunome/sistema-vendas.git
   cd sistema-vendas
   ```

2. **Crie um ambiente virtual e ative-o**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure a conexão com o PostgreSQL (ODBC)**  
   No `settings.py`, adicione:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'sql_server.pyodbc',
           'NAME': 'nome_do_banco',
           'USER': 'postgres',
           'PASSWORD': 'sua_senha',
           'HOST': 'localhost',
           'PORT': '',
           'OPTIONS': {
               'driver': 'ODBC Driver 17 for PostgreSQL',
               'dsn': 'matheus',
           },
       }
   }
   ```

5. **Execute as migrações**  
   ```bash
   python manage.py migrate
   ```

6. **Inicie o servidor**  
   ```bash
   python manage.py runserver
   ```

## 📸 Capturas de Tela

> _(Menu Principal)_
> ![image](https://github.com/user-attachments/assets/278d9293-e295-444b-8c23-4f23ade26853)
>  _(Cadastro de Cliente)_
> ![image](https://github.com/user-attachments/assets/17487c09-b8be-4a36-9062-f6327e4a364b)
>  _(Cadastro de Fornecedor)_
> ![image](https://github.com/user-attachments/assets/cd51d4ea-58f0-48ac-8da9-e6ba0a664f47)
>  _(Registro de Produtos)_
> ![image](https://github.com/user-attachments/assets/003a1cff-7c50-453d-8fd2-c34c33a8a8a1)
>  _(Consulta de Tabelas)_
> ![image](https://github.com/user-attachments/assets/56dab313-2196-491d-a6d6-f466eadd98d6)
>  _(Adicionando Produtos no pedido)_
> ![image](https://github.com/user-attachments/assets/3edb52bf-67e5-4046-af7f-41dc5e7d1b0f)
>  _(Registrando pagamento do pedido)_
> ![image](https://github.com/user-attachments/assets/910e8b06-4c34-42ac-b3a7-13ca25ed2269)
>  _(Tabela de Clientes)_
> ![image](https://github.com/user-attachments/assets/0fbf2c48-8536-4fbc-bab7-dd83032aa059)
>  _(Tabela de Pedidos)_
> ![image](https://github.com/user-attachments/assets/9cd98b1f-cfc7-411c-a3e3-1614f1ec30eb)
>  _(Lista de Fornecedores)_
> ![image](https://github.com/user-attachments/assets/944bdfa1-3552-4538-805d-db127d94f13b)
>  _(Lista de Produtos)_
> ![image](https://github.com/user-attachments/assets/23069a52-2bf3-4003-abc9-0355e6296565)
>  _(Lista de Pagamentos)_
> ![image](https://github.com/user-attachments/assets/6fff0ea2-b81a-433d-b2ef-6a06834b0dfe)


## 📌 Melhorias Futuras

- [ ] Autenticação de usuários (admin e padrão)
- [ ] Acompanhamento do status do pedido
- [ ] Dashboard com indicadores (ex: total vendido, produto mais vendido)
- [ ] Exportação de relatórios em PDF ou Excel
- [ ] Integração com gateway de pagamento externo

## 👨‍💻 Autor

- **Matheus Pontes**  
  📧 matheus.pontes@mail.uft.edu.br
- **Lucas Monteiro**  
  📧 lucas.monteiro@mail.uft.edu.br
