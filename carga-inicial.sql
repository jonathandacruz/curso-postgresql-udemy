CREATE SEQUENCE unidade_unidade_id_seq;

CREATE TABLE UNIDADE (
                UNIDADE_ID INTEGER NOT NULL DEFAULT nextval('unidade_unidade_id_seq'),
                SEGMENTO VARCHAR(100) NOT NULL,
                ENDERECO VARCHAR(400) NOT NULL,
                NOME VARCHAR(100) NOT NULL,
                CONSTRAINT unidade_id_pk PRIMARY KEY (UNIDADE_ID)
);


ALTER SEQUENCE unidade_unidade_id_seq OWNED BY UNIDADE.UNIDADE_ID;

CREATE SEQUENCE cardapio_cardapio_id_seq;

CREATE TABLE CARDAPIO (
                CARDAPIO_ID INTEGER NOT NULL DEFAULT nextval('cardapio_cardapio_id_seq'),
                NOME VARCHAR(150) NOT NULL,
                VLR_PREPARO DOUBLE PRECISION NOT NULL,
                TEMPO_PREPARO INTEGER NOT NULL,
                UNIDADE_ID INTEGER NOT NULL,
                CONSTRAINT cardapio_id_pk PRIMARY KEY (CARDAPIO_ID)
);


ALTER SEQUENCE cardapio_cardapio_id_seq OWNED BY CARDAPIO.CARDAPIO_ID;

CREATE SEQUENCE item_item_id_seq;

CREATE TABLE ITEM (
                ITEM_ID INTEGER NOT NULL DEFAULT nextval('item_item_id_seq'),
                CD INTEGER NOT NULL,
                DESCRICAO VARCHAR(100) NOT NULL,
                UNIDADE_MEDIDA VARCHAR(5) NOT NULL,
                VLR DOUBLE PRECISION NOT NULL,
                FORNECEDOR_ID INTEGER NOT NULL,
                CONSTRAINT item_id_pk PRIMARY KEY (ITEM_ID)
);


ALTER SEQUENCE item_item_id_seq OWNED BY ITEM.ITEM_ID;

CREATE SEQUENCE estoque_estoque_id_seq;

CREATE TABLE ESTOQUE (
                ESTOQUE_ID INTEGER NOT NULL DEFAULT nextval('estoque_estoque_id_seq'),
                QTDE NUMERIC(5,2) NOT NULL,
                QTDE_MINIMA NUMERIC(5,2),
                DT_ATUALIZACAO TIMESTAMP NOT NULL,
                ITEM_ID INTEGER NOT NULL,
                CONSTRAINT estoque_id_pk PRIMARY KEY (ESTOQUE_ID)
);

CREATE TABLE ESTOQUE_CARDAPIO (
                ESTOQUE_CARDAPIO_ID SERIAL,
                ESTOQUE_ID INTEGER NOT NULL,
                CARDAPIO_ID INTEGER NOT NULL,
                QTDE NUMERIC(5,2) NOT NULL,
                CONSTRAINT estoque_cardapio_id_pk PRIMARY KEY (ESTOQUE_CARDAPIO_ID),
		CONSTRAINT estoque_cardapio_id_uk UNIQUE (ESTOQUE_ID, CARDAPIO_ID ),
                CONSTRAINT estoque_estoque_cardapio_fk FOREIGN KEY (ESTOQUE_ID) REFERENCES ESTOQUE,
                CONSTRAINT cardapio_estoque_cardapio_fk FOREIGN KEY (CARDAPIO_ID) REFERENCES CARDAPIO
);



CREATE SEQUENCE fornecedor_fornecedor_id_seq;

CREATE TABLE FORNECEDOR (
                FORNECEDOR_ID INTEGER NOT NULL DEFAULT nextval('fornecedor_fornecedor_id_seq'),
                NOME_FANTASIA VARCHAR(300) NOT NULL,
                RESPONSAVEL VARCHAR(200) NOT NULL,
                DT_INCL DATE NOT NULL,
                CNPJ VARCHAR(14) NOT NULL,
                INSCRICAO_ESTADUAL VARCHAR(10),
                SITUACAO INTEGER NOT NULL,
                CONSTRAINT fornecedor_id_pk PRIMARY KEY (FORNECEDOR_ID)
);
COMMENT ON COLUMN FORNECEDOR.SITUACAO IS '1 - ATIVO
0 - INATIVO';


ALTER SEQUENCE fornecedor_fornecedor_id_seq OWNED BY FORNECEDOR.FORNECEDOR_ID;

CREATE SEQUENCE tipopessoa_tppessoa_seq;

CREATE TABLE TIPO_PESSOA (
                TPPESSOA_ID INTEGER NOT NULL DEFAULT nextval('tipopessoa_tppessoa_seq'),
                DESCRICAO VARCHAR(50) NOT NULL,
                CONSTRAINT tppessoa_id_pk PRIMARY KEY (TPPESSOA_ID)
);


ALTER SEQUENCE tipopessoa_tppessoa_seq OWNED BY TIPO_PESSOA.TPPESSOA_ID;

CREATE SEQUENCE pessoa_pessoa_seq;

CREATE TABLE USUARIO (
                USUARIO_ID INTEGER NOT NULL DEFAULT nextval('pessoa_pessoa_seq'),
                NOME VARCHAR NOT NULL,
                CPF VARCHAR(11) NOT NULL,
                TPPESSOA_ID INTEGER NOT NULL,
                ENDERECO VARCHAR(400) NOT NULL,
                TELEFONE VARCHAR(14),
                EMAIL VARCHAR(50),
                SENHA VARCHAR(150) NOT NULL,
                CONSTRAINT usuario_id_pk PRIMARY KEY (USUARIO_ID)
);
COMMENT ON COLUMN USUARIO.CPF IS 'IRÁ GRAVAR A INFORMAÇÃO DE IDENTIFICAÇÃO DA PESSOA, CASO SEJA FISICA O CPF , CASO JURIDICA O CNPJ';


ALTER SEQUENCE pessoa_pessoa_seq OWNED BY USUARIO.USUARIO_ID;

CREATE SEQUENCE comanda_comanda_id_seq;

CREATE TABLE COMANDA (
                COMANDA_ID INTEGER NOT NULL DEFAULT nextval('comanda_comanda_id_seq'),
                DT_INIC TIMESTAMP NOT NULL,
                DT_ENCERRAMENTO TIMESTAMP,
                VLR_TOTAL DOUBLE PRECISION,
                USUARIO_ID INTEGER NOT NULL,
                CONSTRAINT comanda_id_pk PRIMARY KEY (COMANDA_ID)
);


ALTER SEQUENCE comanda_comanda_id_seq OWNED BY COMANDA.COMANDA_ID;

CREATE SEQUENCE pedido_pedido_id_seq;

CREATE TABLE PEDIDO (
                PEDIDO_ID INTEGER NOT NULL DEFAULT nextval('pedido_pedido_id_seq'),
                DT_INIC TIMESTAMP,
                APROVADO INTEGER NOT NULL,
                DT_FIM TIMESTAMP,
                COMANDA_ID INTEGER NOT NULL,
                USUARIO_ID_CLIENTE INTEGER NOT NULL,
                USUARIO_ID_FUNCIONARIO INTEGER NOT NULL,
                CONSTRAINT pedido_id_pk PRIMARY KEY (PEDIDO_ID)
);

CREATE TABLE CARDAPIO_PEDIDO (
                CARDAPIO_PEDIDO_ID SERIAL,
                CARDAPIO_ID INTEGER NOT NULL,
                PEDIDO_ID INTEGER NOT NULL,
                QTDE INTEGER NOT NULL,
                CONSTRAINT cardapio_pedido_id_pk PRIMARY KEY (CARDAPIO_PEDIDO_ID),
		CONSTRAINT cardapio_pedido_id_uk UNIQUE(CARDAPIO_ID, PEDIDO_ID ),
                CONSTRAINT cardapio_cardapio_pedido_fk FOREIGN KEY (CARDAPIO_ID) REFERENCES CARDAPIO,
                CONSTRAINT pedido_cardapio_pedido_fk FOREIGN KEY (PEDIDO_ID) REFERENCES PEDIDO
);


ALTER TABLE CARDAPIO ADD CONSTRAINT unidade_cardapio_fk
FOREIGN KEY (UNIDADE_ID)
REFERENCES UNIDADE (UNIDADE_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE ESTOQUE ADD CONSTRAINT item_estoque_fk
FOREIGN KEY (ITEM_ID)
REFERENCES ITEM (ITEM_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE USUARIO ADD CONSTRAINT tipo_pessoa_pessoa_fk
FOREIGN KEY (TPPESSOA_ID)
REFERENCES TIPO_PESSOA (TPPESSOA_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE ITEM ADD CONSTRAINT fornecedor_item_fk
FOREIGN KEY (FORNECEDOR_ID)
REFERENCES FORNECEDOR (FORNECEDOR_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE PEDIDO ADD CONSTRAINT usuario_pedido_fk
FOREIGN KEY (USUARIO_ID_CLIENTE)
REFERENCES USUARIO (USUARIO_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE PEDIDO ADD CONSTRAINT usuario_pedido_fk1
FOREIGN KEY (USUARIO_ID_FUNCIONARIO)
REFERENCES USUARIO (USUARIO_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE COMANDA ADD CONSTRAINT usuario_comanda_fk
FOREIGN KEY (USUARIO_ID)
REFERENCES USUARIO (USUARIO_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE PEDIDO ADD CONSTRAINT comanda_pedido_fk
FOREIGN KEY (COMANDA_ID)
REFERENCES COMANDA (COMANDA_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

INSERT INTO unidade (segmento, nome, endereco)
VALUES
    ('Shopping', 'Barzim do shops', 'Shopping da barra, Avenida Beria Rio, Florianópolis SC'),
    ('Tradicional', 'Restaurante do zé', 'Avenida Getulio Dorneles, Chapeco SC');

INSERT INTO cardapio (nome, vlr_preparo, tempo_preparo, unidade_id)
VALUES
    ('Coca cola 350 ml', 0, 0 , 1),
    ('Coca cola 350 ml', 0, 0 , 2);

INSERT INTO cardapio (nome, vlr_preparo, tempo_preparo, unidade_id)
VALUES
    ('Coca cola 600 ml', 0, 0 , 1),
    ('Coca cola 600 ml', 0, 0 , 2);

INSERT INTO cardapio (nome, vlr_preparo, tempo_preparo, unidade_id)
VALUES
    ('Hamburguer da Casa', 5, 15 , 1),
    ('Porção de petiscos', 10, 20 , 2);

INSERT INTO tipo_pessoa (descricao) VALUES ('USUARIO'), ('FUNCIONARIO');

INSERT INTO usuario (nome, cpf, tppessoa_id, endereco, telefone, email, senha)
VALUES
    ('Jonathan da Cruz', '42720955019', 1, 'Avenida Beria Rio, Florianópolis SC', '049999763242', 'jonathan@jonathan.com.br', '$2a$12$MwYkus57CQgP0tCqHHuscOME1/Bg6axpXmVtmAiUiEu5egekNX6jS'),
    ('Joao Paulo', '64249420094', 2, 'Avenida Getulio Dorneles, Chapeco SC', '049899763242', 'joaopaulo@gmail.com', '$2a$12$uCwp8gfpl7BvPBfoBKqVUucRvjUGvKqWsGVm1LxaEJ1S7bjrwvPg2');

INSERT INTO fornecedor (nome_fantasia, responsavel, cnpj, dt_incl, inscricao_estadual, situacao)
VALUES
    ('Ambev', 'Joao Paulo', '71137756000125', NOW(), '7037800117', 1),
    ('Seara', 'Joao Paulo', '49319580000173', NOW(), '7477434051', 1);

INSERT INTO item (cd, descricao, unidade_medida, vlr, FORNECEDOR_ID)
VALUES
    (8744, 'Hamburguer Artesanal', 'UN', 6.5, 2),
    (8745, 'Coca cola 350 ml', 'UN', 2.5, 1);

INSERT INTO estoque (qtde, qtde_minima, dt_atualizacao, item_id)
VALUES
    (100, 80, now(), 1),
    (200, 150, now(), 2);

INSERT INTO estoque_cardapio (estoque_id, cardapio_id, qtde)  VALUES (2, 1, 1), (2, 2, 1);

INSERT INTO COMANDA (DT_INIC , dt_encerramento, vlr_total, usuario_id) VALUES (NOW() , NULL, NULL, 1);

INSERT INTO pedido (dt_inic, aprovado, dt_fim, comanda_id, usuario_id_cliente, usuario_id_funcionario)
VALUES (now(), 0, NULL, 1, 1, 2);

INSERT INTO cardapio_pedido (cardapio_id, pedido_id, qtde) values  (1, 1, 2);
