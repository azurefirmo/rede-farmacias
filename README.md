# 🏥 Sistema de Gerenciamento de Rede de Farmácias (API)

Esta é uma API robusta desenvolvida com **Django Rest Framework (DRF)** para o gerenciamento centralizado de uma rede de farmácias. O sistema cobre desde o controle de estoque por lotes (normas ANVISA) até a venda final no PDV.

## 🚀 1. Tecnologias Utilizadas
*   **Python 3.10+**
*   **Django 5.0+**
*   **Django Rest Framework**
*   **SimpleJWT** (Autenticação)
*   **SQLite** (Desenvolvimento) / **PostgreSQL** (Produção)
*   **CORS Headers** (Integração Web/Mobile)

---

## 🔐 2. Controle de Acesso (RBAC)
O sistema utiliza permissões baseadas em cargos (**Roles**). Cada cargo tem uma visão restrita dos dados:

| Cargo | Permissões |
| :--- | :--- |
| **ADMIN** | Acesso total a todas as filiais, relatórios e criação de usuários. |
| **MANAGER** | Gere uma filial específica, visualiza vendas e estoque local. |
| **PHARMACIST** | Visualiza estoque e valida produtos controlados. |
| **STOCKER** | Realiza a entrada de novos lotes e conferência de validade. |
| **CASHIER** | Realiza vendas no PDV e consulta preços. |
| **CUSTOMER** | Visualiza histórico de compras e catálogo de produtos. |

---

## 📦 3. Regras de Negócio Implementadas

### 🇧🇷 Localização Brasil
*   Suporte a **CPF/CNPJ**.
*   Campos obrigatórios da ANVISA: **Registro MS**, **Lote** e **Validade**.
*   Identificação tributária por **NCM** nos produtos.

### 📉 Inteligência de Estoque (FEFO)
O sistema implementa a lógica **FEFO** (*First Expired, First Out*). Ao realizar uma venda:
1. O sistema busca automaticamente o lote com a **validade mais próxima**.
2. Bloqueia a venda de produtos com data de validade vencida.
3. Realiza a baixa automática em múltiplos lotes caso a quantidade solicitada seja maior que o saldo de um único lote.

### 💰 Tabela de Preços Dinâmica
*   **Varejo:** Aplicado automaticamente para clientes comuns.
*   **Atacado:** Aplicado se o usuário logado possuir a role `WHOLESALE`.

---

## 📋 4. Principais Endpoints

### Autenticação
*   `POST /api/auth/token/`: Obtém os tokens de acesso e refresh (Login).
*   `POST /api/auth/token/refresh/`: Renova o token de acesso.

### Inventário e Filiais
*   `GET/POST /api/branches/`: Gerenciamento de unidades da rede.
*   `GET/POST /api/products/`: Catálogo unificado de medicamentos e produtos.
*   `GET/POST /api/stock/`: Controle de saldos por filial, lote e validade.

### Vendas (PDV)
*   `POST /api/orders/`: Realiza uma nova venda. 
    *   *Payload esperado:* `{"branch": ID, "payment_method": "PIX", "items": [{"product": ID, "quantity": X}]}`
*   `GET /api/orders/`: Histórico de vendas (filtrado por cargo/filial).

---

## 🛠️ 5. Guia de Instalação e Execução

1. **Clonar o repositório e acessar a pasta:**
   ```bash
   git clone <url-do-repositorio>
   cd farmacia_network
   ```

2. **Criar e ativar o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   ```

3. **Instalar dependências:**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
   ```

4. **Rodar Migrações e Criar Admin:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Iniciar o Servidor:**
   ```bash
   python manage.py runserver
   ```

---

## 🚢 6. Check-list para Deploy (Produção)

Para colocar este sistema em produção (AWS, DigitalOcean, Heroku), siga estes passos:

1.  **Segurança:** Alterar `DEBUG = False` no `settings.py`.
2.  **Variáveis de Ambiente:** Usar `python-dotenv` para esconder a `SECRET_KEY` e dados do Banco.
3.  **Banco de Dados:** Trocar SQLite por **PostgreSQL**.
4.  **Servidor Web:** Utilizar **Gunicorn** ou **Uvicorn** como servidor de aplicação.
5.  **Proxy Reverso:** Utilizar **Nginx** para servir arquivos estáticos e prover HTTPS (SSL).
6.  **CORS:** Configurar `CORS_ALLOWED_ORIGINS` com o domínio real do seu frontend Web/Mobile.

---

## 🧪 7. Exemplo de Teste de Venda (JSON)

Para testar a criação de uma venda no Postman, envie um **POST** para `/api/orders/` com o seguinte corpo:

```json
{
    "branch": 1,
    "payment_method": "PIX",
    "items": [
        {
            "product": 1,
            "quantity": 5
        },
        {
            "product": 2,
            "quantity": 1
        }
    ]
}
```
*O sistema verificará o estoque na Filial 1, dará baixa nos lotes mais próximos do vencimento e retornará o valor total calculado.*

---
