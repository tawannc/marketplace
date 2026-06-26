Este projeto consiste no desenvolvimento de um Marketplace completo, onde vendedores podem cadastrar produtos e compradores podem navegar, adicionar itens ao carrinho, finalizar pedidos e avaliar vendedores e produtos.
O sistema foi construído ao longo de 12 sprints, evoluindo desde a configuração inicial até funcionalidades avançadas como avaliações, gestão de pedidos e páginas públicas.

O objetivo principal é simular um ambiente real de comércio eletrônico, permitindo que alunos pratiquem conceitos fundamentais de desenvolvimento web com Django, arquitetura de software, modelagem de dados e boas práticas de versionamento.

# Tecnologias Utilizadas
Python 3.x

Django 4.x

SQLite / PostgreSQL (dependendo do ambiente)

HTML5, CSS3, Bootstrap

JavaScript (básico)

Git e GitHub para versionamento

venv para isolamento do ambiente

# Instalação, Configuração e Execução
1️⃣ Clonar o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
2️⃣ Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
3️⃣ Instalar dependências
pip install -r requirements.txt
4️⃣ Aplicar migrações
python manage.py migrate
5️⃣ Criar superusuário
python manage.py createsuperuser
6️⃣ Executar o servidor
python manage.py runserver
Acesse em:
http://127.0.0.1:8000/

# Principais Decisões Técnicas da Equipe
Separação clara entre perfis de usuário: BuyerProfile e SellerProfile para garantir regras de negócio distintas.

Modelagem modular: apps separados (accounts, products, orders, reviews, core) para facilitar manutenção.

Uso de OneToOne e ForeignKey para garantir integridade entre pedidos, itens e avaliações.

Criação de páginas públicas para produtos e vendedores, permitindo navegação sem login.

Sistema de avaliações dividido em duas partes:
Review (produto)
ReviewVendedor (vendedor)

Carrinho baseado em sessão, evitando necessidade de login para adicionar itens.

Fluxo de pedido simplificado, permitindo evolução futura para integrações reais de pagamento.

Templates organizados por app, seguindo boas práticas do Django.

# Integrantes
Jennifer Costa
