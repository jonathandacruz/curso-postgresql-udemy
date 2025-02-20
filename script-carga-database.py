from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from faker import Faker
import random
from datetime import datetime, timedelta

# URL de conexão com o banco de dados PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mecanica_curso"

# Criar o motor e a sessão para interagir com o banco
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()

# Definição das tabelas

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    data_nascimento = Column(Date, nullable=False)  # Nova coluna
    documento = Column(String(20), unique=True, nullable=False)  # Nova coluna

class OrdemServico(Base):
    __tablename__ = "ordens_servico"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_abertura = Column(Date, nullable=False)
    data_fechamento = Column(Date, nullable=True)
    veiculo_modelo = Column(String(100), nullable=False)
    veiculo_placa = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  # Aberta, Concluída, Cancelada
    cliente = relationship("Cliente")

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)  # Valor do serviço

class OrdemServicoServico(Base):
    __tablename__ = "ordem_servico_servico"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    ordem_servico = relationship("OrdemServico")
    servico = relationship("Servico")

class ContaReceber(Base):
    __tablename__ = "contas_receber"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    vencimento = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # Pendente, Pago
    ordem_servico = relationship("OrdemServico")

class ContaPagar(Base):
    __tablename__ = "contas_pagar"
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    vencimento = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # Pendente, Pago

# Nova tabela de Estoque
class Estoque(Base):
    __tablename__ = "estoque"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_produto = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

# Tabela intermediária entre Ordem de Serviço e Estoque (ItemOrdemServico)
class ItemOrdemServico(Base):
    __tablename__ = "itens_ordem_servico"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    estoque_id = Column(Integer, ForeignKey("estoque.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)  # Quantidade do item utilizada na ordem
    preco_total = Column(Numeric(10, 2), nullable=False)  # Preço total do item utilizado (quantidade * preco_unitario)
    ordem_servico = relationship("OrdemServico")
    estoque = relationship("Estoque")

# Criar as tabelas no banco
Base.metadata.create_all(engine)

# Gerar dados falsos usando o Faker
fake = Faker('pt_BR')

def gerar_cliente():
    nome = fake.name()
    telefone = fake.phone_number()
    data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=70)

    # Gerar um CPF único
    while True:
        documento = fake.cpf()
        existe = session.query(Cliente).filter_by(documento=documento).first()  # Verifica se já existe no banco
        if not existe:
            break  # Se não existir, sai do loop e usa esse CPF
    
    cliente = Cliente(
        nome=nome, 
        telefone=telefone, 
        data_nascimento=data_nascimento, 
        documento=documento
    )

    session.add(cliente)
    session.commit()
    return cliente

  
from datetime import timedelta

def gerar_ordem_servico(cliente):
    veiculos = [
    "Fiat Uno", "Honda Civic", "Toyota Corolla", "Volkswagen Gol", "Chevrolet Onix",
    "Ford Ka", "Hyundai HB20", "Renault Sandero", "Volkswagen Polo", "Nissan March",
    "Chevrolet Corsa", "Peugeot 208", "Citroën C3", "Toyota Etios", "Honda Fit",
    "Fiat Palio", "Volkswagen Voyage", "Renault Logan", "Hyundai Creta", "Jeep Renegade",
    "Ford EcoSport", "Chevrolet Tracker", "Honda HR-V", "Toyota Hilux", "Fiat Strada",
    "Volkswagen Saveiro", "Ford Ranger", "Chevrolet S10", "Mitsubishi L200", "Nissan Frontier",
    "Jeep Compass", "Hyundai Tucson", "Kia Sportage", "Volkswagen T-Cross", "Renault Duster",
    "Chevrolet Spin", "Fiat Toro", "Honda WR-V", "Toyota SW4", "Peugeot 2008",
    "Mercedes-Benz Classe A", "BMW Série 3", "Audi A3", "Volvo XC40", "Land Rover Evoque"
    ]

    def gerar_placa():
        while True:
            placa = f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}" \
                    f"{random.randint(0, 9)}{fake.random_uppercase_letter()}{random.randint(0, 9)}{random.randint(0, 9)}"
            if not session.query(OrdemServico).filter_by(veiculo_placa=placa).first():
                return placa  # Retorna a placa se ainda não existir no banco

    data_abertura = fake.date_this_year()
    status = random.choice(["Aberta", "Concluída", "Cancelada"])
    data_fechamento = None if status == "Aberta" else data_abertura + timedelta(days=random.randint(1, 5))

    ordem_servico = OrdemServico(
        cliente_id=cliente.id,
        veiculo_modelo=random.choice(veiculos),
        veiculo_placa=gerar_placa(),
        data_abertura=data_abertura,
        data_fechamento=data_fechamento,
        status=status
    )

    session.add(ordem_servico)
    session.commit()
    return ordem_servico


def gerar_conta_receber(ordem_servico):
    valor = round(random.uniform(100, 1000), 2)
    vencimento = fake.date_between(start_date="today", end_date="+30d")
    status = random.choice(["Pendente", "Pago"])
    conta_receber = ContaReceber(ordem_servico_id=ordem_servico.id, valor=valor, vencimento=vencimento, status=status)
    session.add(conta_receber)
    session.commit()

DESCRICOES_CONTAS = [
    "Compra de peças automotivas",
    "Pagamento de aluguel da oficina",
    "Conta de energia elétrica",
    "Conta de água",
    "Compra de óleo lubrificante",
    "Compra de pneus",
    "Pagamento de salário dos funcionários",
    "Manutenção de equipamentos",
    "Compra de ferramentas",
    "Licenciamento e taxas do CNPJ",
    "Internet e telefone da oficina",
    "Seguro do estabelecimento",
    "Compra de baterias automotivas",
    "Pagamento de fornecedores",
    "Compra de fluidos de freio",
    "Materiais de limpeza para a oficina",
    "Gastos com publicidade e marketing",
    "Compra de estopa e panos de limpeza",
    "Pagamento de impostos e tributos",
    "Compra de tinta e materiais para pintura automotiva",
    "Compra de cabos de vela",
    "Compra de pastilhas de freio",
    "Compra de discos de freio",
    "Compra de amortecedores",
    "Compra de molas e suspensão",
    "Compra de kits de embreagem",
    "Compra de sensores automotivos",
    "Compra de velas de ignição",
    "Compra de correias dentadas",
    "Compra de filtros de óleo",
    "Compra de filtros de ar",
    "Compra de filtros de combustível",
    "Compra de fluidos para direção hidráulica",
    "Compra de aditivos para radiador",
    "Compra de lâmpadas automotivas",
    "Compra de chicotes elétricos",
    "Compra de parafusos e fixadores",
    "Compra de escapamentos e catalisadores",
    "Compra de kits de retífica de motor",
    "Compra de anéis de segmento",
    "Compra de bronzinas",
    "Compra de pistões e bielas",
    "Compra de juntas para motores",
    "Compra de sensores de oxigênio",
    "Compra de módulos eletrônicos",
    "Compra de cabos de bateria",
    "Compra de terminais elétricos",
    "Compra de alternadores e motores de partida",
    "Compra de correias auxiliares",
    "Compra de óleos para transmissão",
    "Compra de fluido para arrefecimento",
    "Compra de palhetas do limpador",
    "Compra de buchas e coxins",
    "Compra de embreagens hidráulicas",
    "Compra de bombas de combustível",
    "Compra de sensores de temperatura",
    "Compra de kits de sincronização de motor",
    "Compra de volantes de motor",
    "Compra de engrenagens e rolamentos",
    "Compra de para-lamas e para-choques",
    "Compra de capôs e portas automotivas",
    "Compra de vidros e espelhos retrovisores",
    "Compra de tapetes e forrações internas",
    "Compra de bancos e estofamentos",
    "Compra de tintas e vernizes automotivos",
    "Compra de lixas e massas para funilaria",
    "Compra de adesivos e fitas automotivas",
    "Compra de compressores de ar",
    "Compra de elevadores automotivos",
    "Compra de macacos hidráulicos",
    "Compra de pistolas de pintura",
    "Compra de medidores e scanners automotivos",
    "Compra de chaves de impacto",
    "Compra de torquímetros",
    "Compra de extratores de rolamentos",
    "Compra de alinhadores de direção",
    "Compra de balanceadoras de rodas",
    "Compra de desmontadoras de pneus",
    "Compra de máquinas de solda",
    "Compra de cilindros pneumáticos",
    "Compra de equipamentos de proteção individual (EPI)",
    "Compra de uniformes e aventais para funcionários",
    "Pagamento de treinamentos técnicos",
    "Compra de materiais de escritório",
    "Compra de software para gestão da oficina",
    "Manutenção do sistema de exaustão",
    "Reparo do sistema de ar condicionado",
    "Gastos com transporte de peças",
    "Despesa com serviços terceirizados",
    "Investimento em equipamentos novos",
    "Atualização de ferramentas e diagnósticos",
    "Compra de estantes e organizadores para estoque",
    "Troca de lâmpadas e manutenção elétrica",
    "Reforma da estrutura da oficina",
    "Compra de etiquetas e identificação de peças",
    "Compra de sensores de pressão de pneus",
    "Compra de rastreadores veiculares",
    "Compra de alarmes automotivos",
    "Compra de kits de faróis de LED",
    "Compra de películas de proteção solar",
    "Compra de suportes e racks automotivos"
]

def gerar_contas_pagar(qtd=100000000, batch_size=5000):
    contas = []
    
    for _ in range(qtd):
        conta = ContaPagar(
            descricao=random.choice(DESCRICOES_CONTAS),
            valor=round(random.uniform(100, 1000), 2),
            vencimento=fake.date_between(start_date="today", end_date="+30d"),
            status=random.choice(["Pendente", "Pago"])
        )
        contas.append(conta)

        # Inserir em lotes para evitar sobrecarga de memória
        if len(contas) >= batch_size:
            session.add_all(contas)
            session.commit()
            contas = []  # Limpa a lista para o próximo lote

    # Inserir o restante (caso não tenha atingido batch_size no final)
    if contas:
        session.add_all(contas)
        session.commit()


def inicializar_estoque():
    produtos_estoque = [
    ("Óleo lubrificante", 50, 35.90),
    ("Pneu aro 15", 20, 289.99),
    ("Filtro de ar", 30, 45.50),
    ("Pastilha de freio", 40, 120.00),
    ("Bateria 60Ah", 15, 450.00),
    ("Amortecedor dianteiro", 25, 320.00),
    ("Correia dentada", 35, 85.00),
    ("Velas de ignição", 50, 22.90),
    ("Fluido de freio", 20, 39.90),
    ("Palhetas do limpador", 30, 25.00),
    ("Radiador", 10, 550.00),
    ("Bomba de combustível", 12, 290.00),
    ("Sensor de temperatura", 18, 75.00),
    ("Coxim do motor", 25, 180.00),
    ("Filtro de combustível", 35, 48.90),
    ("Óleo de câmbio", 40, 95.00),
    ("Disco de freio", 30, 180.00),
    ("Kit de embreagem", 20, 780.00),
    ("Jogo de pneus aro 16", 8, 1200.00),
    ("Aditivo para radiador", 50, 32.90),
    ("Cabo de vela", 30, 110.00),
    ("Kit suspensão", 15, 890.00),
    ("Sensor de rotação", 20, 135.00),
    ("Rolamento de roda", 25, 210.00),
    ("Alternador", 10, 850.00),
    ("Motor de partida", 8, 920.00),
    ("Chave de roda", 50, 45.00),
    ("Macaco hidráulico", 15, 199.00),
    ("Extintor de incêndio", 30, 65.00),
    ("Câmera de ré", 12, 350.00),
    ("Farol dianteiro", 20, 480.00),
    ("Lanterna traseira", 18, 270.00),
    ("Para-choque dianteiro", 10, 680.00),
    ("Jogo de tapetes automotivos", 25, 90.00),
    ("Calotas aro 14", 30, 150.00),
    ("Par de retrovisores", 20, 230.00),
    ("Cinto de segurança", 15, 120.00),
    ("Escapamento esportivo", 10, 750.00),
    ("Módulo de injeção eletrônica", 8, 1350.00),
    ("Kit vidro elétrico", 12, 950.00),
    ("Parafuso de roda antifurto", 40, 85.00),
    ("Par de molas esportivas", 15, 490.00),
    ("Junta do cabeçote", 25, 310.00),
    ("Buzina automotiva", 30, 95.00),
    ("Capa para banco de couro", 20, 520.00),
    ("Sensor de estacionamento", 18, 420.00),
    ("Volante esportivo", 10, 680.00),
    ("Filtro do ar-condicionado", 25, 80.00),
    ("Câmbio automático recondicionado", 5, 3500.00)
    ]


    for nome_produto, quantidade, preco_unitario in produtos_estoque:
        estoque = Estoque(
            nome_produto=nome_produto, 
            quantidade=quantidade, 
            preco_unitario=preco_unitario
        )
        session.add(estoque)

    session.commit()


def gerar_item_ordem_servico(ordem_servico, estoque):
    quantidade = random.randint(1, 5)  # Quantidade do item usado
    preco_total = estoque.preco_unitario * quantidade  # Preço total
    item = ItemOrdemServico(ordem_servico_id=ordem_servico.id, estoque_id=estoque.id, quantidade=quantidade, preco_total=preco_total)
    session.add(item)
    session.commit()

def inicializar_servicos():
    servicos_mecanica = [
        "Troca de óleo",
        "Alinhamento e balanceamento",
        "Troca de pastilhas de freio",
        "Revisão geral",
    "Troca de pneus",
    "Limpeza de bicos injetores",
    "Troca de embreagem",
    "Reparo no sistema de ar-condicionado",
    "Diagnóstico eletrônico",
    "Troca de bateria",
    "Suspensão e amortecedores",
    "Troca de filtro de ar",
    "Reparo no sistema de escapamento",
    "Troca de velas de ignição",
    "Higienização do sistema de ar-condicionado",
    "Troca de fluido de freio",
    "Troca de fluido de direção hidráulica",
    "Troca de correia dentada",
    "Troca de filtro de combustível",
    "Troca de termostato",
    "Regulagem de válvulas",
    "Troca de bomba de combustível",
    "Troca de junta do cabeçote",
    "Reparo no alternador",
    "Troca de motor de arranque",
    "Troca de lâmpadas automotivas",
    "Polimento de faróis",
    "Troca de rolamentos de roda",
    "Reparo em sistema de injeção eletrônica",
    "Reparo em vazamento de óleo",
    "Substituição de sensores do motor",
    "Reparo na caixa de direção",
    "Recarga e manutenção de bateria",
    "Reparo no sistema de transmissão",
    "Instalação de acessórios automotivos",
    "Descarbonização do motor",
    "Reparo no sistema de tração",
    "Reparo no sistema de embreagem",
    "Troca de palhetas do limpador de para-brisa",
    "Instalação de películas automotivas",
    "Reparo em chicote elétrico",
    "Troca de radiador",
    "Troca de ventoinha do radiador",
    "Troca de coxins do motor",
    "Regulagem do freio de mão",
    "Troca de diferencial",
    "Limpeza do TBI (corpo de borboleta)",
    "Troca de bomba d’água",
    "Manutenção no sistema de suspensão a ar",
    "Revisão do sistema de câmbio automático",
    "Troca do óleo do câmbio automático",
    "Reparo no sistema de escapamento",
    "Teste de estanqueidade no sistema de arrefecimento"
    ]

    for descricao in servicos_mecanica:
        preco = round(random.uniform(50, 500), 2)
        servico = Servico(descricao=descricao, preco=preco)
        session.add(servico)

    session.commit()
inicializar_servicos()
inicializar_estoque()
# Buscar todos os serviços do banco antes de gerar as ordens
todos_servicos = session.query(Servico).all()
todos_estoque = session.query(Estoque).all()

 
for _ in range(0):  # Criar 10 clientes
    cliente = gerar_cliente()
    for _ in range(3):  # Para cada cliente, gerar 3 ordens de serviço
        ordem_servico = gerar_ordem_servico(cliente)

        # Selecionar aleatoriamente 2 serviços para a ordem
        servicos_selecionados = random.sample(todos_servicos, 2)  
        
        for servico in servicos_selecionados:
            ordem_servico_servico = OrdemServicoServico(
                ordem_servico_id=ordem_servico.id, 
                servico_id=servico.id
            )
            session.add(ordem_servico_servico)

        gerar_conta_receber(ordem_servico)

        # Selecionar aleatoriamente 2 produtos do estoque
        produtos_selecionados = random.sample(todos_estoque, 2)

        for produto in produtos_selecionados:
            gerar_item_ordem_servico(ordem_servico, produto)

session.commit()

gerar_contas_pagar()

# Commit para salvar as alterações
session.commit()

print("Dados gerados e tabelas criadas com sucesso!")
